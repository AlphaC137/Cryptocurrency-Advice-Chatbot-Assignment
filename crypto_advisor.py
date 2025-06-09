import random
import requests
import time

class CryptoAdvisor:
    def __init__(self, name="CryptoSage"):
        self.name = name
        self.greetings = [
            f"Hey there! I'm {name}, your eco-friendly crypto guide! 🌱",
            f"Welcome! {name} at your service for sustainable crypto advice! ♻️",
            f"Hi! Ready to explore green crypto options with {name}? 🚀"
        ]
        
        # Static database as fallback
        self.static_crypto_db = {
            "Bitcoin": {
                "price_trend": "rising",
                "market_cap": "high",
                "energy_use": "high",
                "sustainability_score": 3/10
            },
            "Ethereum": {
                "price_trend": "stable",
                "market_cap": "high",
                "energy_use": "medium",
                "sustainability_score": 6/10
            },
            "Cardano": {
                "price_trend": "rising",
                "market_cap": "medium",
                "energy_use": "low",
                "sustainability_score": 8/10
            },
            "Solana": {
                "price_trend": "rising",
                "market_cap": "medium",
                "energy_use": "low",
                "sustainability_score": 7.5/10
            },
            "Polkadot": {
                "price_trend": "stable",
                "market_cap": "medium",
                "energy_use": "low",
                "sustainability_score": 7/10
            },
            "Algorand": {
                "price_trend": "stable",
                "market_cap": "low",
                "energy_use": "very low",
                "sustainability_score": 9/10
            }
        }
        
        # Data not avaliable on the API, so we keep it static
        self.sustainability_data = {
            "bitcoin": {"energy_use": "high", "sustainability_score": 3/10},
            "ethereum": {"energy_use": "medium", "sustainability_score": 6/10},
            "cardano": {"energy_use": "low", "sustainability_score": 8/10},
            "solana": {"energy_use": "low", "sustainability_score": 7.5/10},
            "polkadot": {"energy_use": "low", "sustainability_score": 7/10},
            "algorand": {"energy_use": "very low", "sustainability_score": 9/10}
        }
        
        # Initialize API data
        self.crypto_db = {}
        self.update_crypto_data()
        
    def update_crypto_data(self):
        """Update crypto data from CoinGecko API"""
        try:
            # Get top coins by market cap
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 10,
                "page": 1,
                "sparkline": False
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                coins = response.json()
                
                for coin in coins:
                    coin_id = coin["id"]
                    price_change_24h = coin["price_change_percentage_24h"] or 0
                    
                    if price_change_24h > 1.5:
                        price_trend = "rising"
                    elif price_change_24h < -1.5:
                        price_trend = "falling"
                    else:
                        price_trend = "stable"
                    
                    market_cap = coin["market_cap"]
                    if market_cap > 50000000000:
                        market_cap_category = "high"
                    elif market_cap > 10000000000:
                        market_cap_category = "medium"
                    else:
                        market_cap_category = "low"
                    
                    # merge with sustainability data
                    self.crypto_db[coin["name"]] = {
                        "price_trend": price_trend,
                        "market_cap": market_cap_category,
                        "current_price": coin["current_price"],
                        "price_change_24h": coin["price_change_percentage_24h"],
                        "market_cap_value": coin["market_cap"],
                        "energy_use": self.sustainability_data.get(coin_id, {}).get("energy_use", "unknown"),
                        "sustainability_score": self.sustainability_data.get(coin_id, {}).get("sustainability_score", 5/10)
                    }
                
                print(f"Successfully updated data for {len(self.crypto_db)} cryptocurrencies from CoinGecko API")
                return True
                
            else:
                print(f"API request failed with status code {response.status_code}")
                self.crypto_db = self.static_crypto_db.copy()
                return False
                
        except Exception as e:
            print(f"Error updating crypto data: {e}")
            self.crypto_db = self.static_crypto_db.copy()
            return False
    
    def greet(self):
        return random.choice(self.greetings)
    
    def get_recommendation(self, query):
        query = query.lower()
        
        if any(word in query for word in ["refresh", "update", "latest"]):
            success = self.update_crypto_data()
            if success:
                return "I've updated my cryptocurrency data with the latest information from CoinGecko! 🔄"
            else:
                return "I couldn't update the data right now. Using my existing information instead."
        
        if any(word in query for word in ["sustainable", "green", "eco", "environment"]):
            return self.get_sustainable_recommendation()
            
        elif any(word in query for word in ["profit", "money", "gain", "return", "trending", "rising"]):
            return self.get_profitable_recommendation()
            
        elif any(crypto.lower() in query for crypto in self.crypto_db.keys()):
            for crypto in self.crypto_db.keys():
                if crypto.lower() in query.lower():
                    return self.get_crypto_info(crypto)
                    
        elif "price" in query:
            return self.get_price_info()
        
        elif any(word in query for word in ["recommend", "suggestion", "advice", "best", "should", "buy"]):
            return self.get_balanced_recommendation()
            
        # Help command
        elif any(word in query for word in ["help", "guide", "how", "what can you"]):
            return self.get_help_message()
            
        # Response to unrecognized queries
        else:
            return "I'm not sure what you're asking about. Try asking about sustainable cryptocurrencies, profitable options, or specific coins like Bitcoin!"
    
    def get_sustainable_recommendation(self):
        sustainable_crypto = max(self.crypto_db.items(), 
                                key=lambda x: x[1]["sustainability_score"])
        
        crypto_name = sustainable_crypto[0]
        score = sustainable_crypto[1]["sustainability_score"] * 10
        
        responses = [
            f"Looking for eco-friendly crypto? {crypto_name} is your best bet with a sustainability score of {score}/10! 🌱",
            f"For sustainability-focused investors, I recommend {crypto_name}. It scores {score}/10 on our green scale! 🌍",
            f"{crypto_name} leads the pack in sustainability with a score of {score}/10. It's the green choice! ♻️"
        ]
        
        return random.choice(responses)
    
    def get_profitable_recommendation(self):
        rising_cryptos = {name: data for name, data in self.crypto_db.items() 
                         if data["price_trend"] == "rising"}
        
        if not rising_cryptos:
            return "None of the cryptocurrencies are currently showing a rising trend based on my latest data."
        
        market_cap_priority = {"high": 3, "medium": 2, "low": 1}
        
        best_crypto = max(rising_cryptos.items(),
                         key=lambda x: market_cap_priority.get(x[1]["market_cap"], 0))
        
        crypto_name = best_crypto[0]
        market_cap = best_crypto[1]["market_cap"]
        price_change = best_crypto[1].get("price_change_24h", "unknown")
        
        if price_change != "unknown":
            price_info = f"with a 24h change of {price_change:.2f}%"
        else:
            price_info = ""
        
        responses = [
            f"For profit potential, check out {crypto_name}! It's trending upward {price_info} with a {market_cap} market cap. 📈",
            f"{crypto_name} is showing a rising trend {price_info} with {market_cap} market capitalization - looking promising! 🚀",
            f"My profit-focused pick is {crypto_name}. It's on an upward trend {price_info} in the {market_cap} market cap category. 💰"
        ]
        
        return random.choice(responses)
    
    def get_price_info(self):
        result = "Current cryptocurrency prices (USD):\n\n"
        
        for crypto, data in sorted(self.crypto_db.items(), key=lambda x: x[1].get("market_cap_value", 0), reverse=True):
            price = data.get("current_price", "N/A")
            change = data.get("price_change_24h", "N/A")
            
            if price != "N/A" and change != "N/A":
                change_emoji = "🟢" if change > 0 else "🔴" if change < 0 else "⚪"
                result += f"{crypto}: ${price:,.2f} {change_emoji} {change:.2f}%\n"
            else:
                result += f"{crypto}: Data not available\n"
                
        return result
    
    def get_balanced_recommendation(self):
        profitability_score = {
            "rising": 2, "stable": 1, "falling": 0
        }
        market_cap_score = {
            "high": 2, "medium": 1, "low": 0.5
        }
        
        # Calculate combined scores
        scores = {}
        for crypto, data in self.crypto_db.items():
            profit_component = (profitability_score.get(data["price_trend"], 0) * 0.6 + 
                               market_cap_score.get(data["market_cap"], 0) * 0.4)
            sustainability = data["sustainability_score"]
            
            # Balance between profit (60%) and sustainability (40%)
            scores[crypto] = profit_component * 0.6 + sustainability * 0.4
        
        best_crypto = max(scores.items(), key=lambda x: x[1])[0]
        crypto_data = self.crypto_db[best_crypto]
        
        price_info = ""
        if "current_price" in crypto_data:
            price_info = f" Current price: ${crypto_data['current_price']:,.2f}."
            
        return (f"Based on both profitability and sustainability, I recommend {best_crypto}. "
                f"It has a {crypto_data['price_trend']} price trend, {crypto_data['market_cap']} "
                f"market cap, and a sustainability score of {crypto_data['sustainability_score']*10}/10!{price_info} 🌟")
    
    def get_crypto_info(self, crypto):
        data = self.crypto_db[crypto]
        
        price_info = ""
        if "current_price" in data:
            price_info = f"💵 Current Price: ${data['current_price']:,.2f}\n"
            
        change_info = ""
        if "price_change_24h" in data and data['price_change_24h'] is not None:
            change_emoji = "🟢" if data['price_change_24h'] > 0 else "🔴" if data['price_change_24h'] < 0 else "⚪"
            change_info = f"📊 24h Change: {change_emoji} {data['price_change_24h']:.2f}%\n"
            
        return (f"{crypto} Info:\n"
                f"{price_info}"
                f"{change_info}"
                f"📈 Price Trend: {data['price_trend'].capitalize()}\n"
                f"💰 Market Cap: {data['market_cap'].capitalize()}\n"
                f"⚡ Energy Use: {data['energy_use'].capitalize()}\n"
                f"🌱 Sustainability Score: {data['sustainability_score']*10}/10\n")
    
    def get_help_message(self):
        return ("Here's how you can interact with me:\n"
                "- Ask about sustainable or eco-friendly cryptocurrencies\n"
                "- Ask which crypto is trending up or best for profits\n"
                "- Request information about specific coins like Bitcoin or Ethereum\n"
                "- Ask for current prices of top cryptocurrencies\n"
                "- Type 'refresh data' to get the latest information\n"
                "- Ask for general recommendations\n\n"
                "Example questions:\n"
                "\"What's the most sustainable cryptocurrency?\"\n"
                "\"Which crypto is trending up?\"\n"
                "\"Tell me about Cardano\"\n"
                "\"What are the current prices?\"\n"
                "\"What should I invest in?\"")

def main():
    bot = CryptoAdvisor("EcoCrypto")
    print(f"\n{bot.greet()}")
    print("Type 'exit' to quit.\n")
    print("DISCLAIMER: Cryptocurrency investments are risky. This bot provides educational information only. Always do your own research before investing! ⚠️\n")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ["exit", "quit", "bye"]:
            print(f"\n{bot.name}: Thanks for chatting! Stay green in your crypto journey! 🌿")
            break
            
        response = bot.get_recommendation(user_input)
        print(f"\n{bot.name}: {response}")

if __name__ == "__main__":
    main()
