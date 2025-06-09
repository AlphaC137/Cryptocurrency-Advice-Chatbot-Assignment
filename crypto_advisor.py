import random
from datetime import datetime

class CryptoAdvisor:
    def __init__(self, name="CryptoSage"):
        self.name = name
        self.greetings = [
            f"Hey there! I'm {name}, your eco-friendly crypto guide! 🌱",
            f"Welcome! {name} at your service for sustainable crypto advice! ♻️",
            f"Hi! Ready to explore green crypto options with {name}? 🚀"
        ]
        
        # Sample dataset as provided in the assignment
        self.crypto_db = {
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
            }
        }
        
        # Add more cryptocurrencies for a better experience
        self.crypto_db.update({
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
        })
        
    def greet(self):
        return random.choice(self.greetings)
    
    def get_recommendation(self, query):
        query = query.lower()
        
        # Check for sustainability queries
        if any(word in query for word in ["sustainable", "green", "eco", "environment"]):
            return self.get_sustainable_recommendation()
            
        # Check for profitability queries
        elif any(word in query for word in ["profit", "money", "gain", "return", "trending", "rising"]):
            return self.get_profitable_recommendation()
            
        # Check for specific cryptocurrency information
        elif any(crypto.lower() in query for crypto in self.crypto_db.keys()):
            for crypto in self.crypto_db.keys():
                if crypto.lower() in query:
                    return self.get_crypto_info(crypto)
                    
        # General recommendation query
        elif any(word in query for word in ["recommend", "suggestion", "advice", "best", "should", "buy"]):
            return self.get_balanced_recommendation()
            
        # Help command
        elif any(word in query for word in ["help", "guide", "how", "what can you"]):
            return self.get_help_message()
            
        # Generic response for unrecognized queries
        else:
            return "I'm not sure what you're asking about. Try asking about sustainable cryptocurrencies, profitable options, or specific coins like Bitcoin!"
    
    def get_sustainable_recommendation(self):
        # Find the most sustainable cryptocurrency
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
        # Filter for rising cryptocurrencies
        rising_cryptos = {name: data for name, data in self.crypto_db.items() 
                         if data["price_trend"] == "rising"}
        
        if not rising_cryptos:
            return "None of the cryptocurrencies are currently showing a rising trend."
        
        # Prioritize by market cap (high > medium > low)
        market_cap_priority = {"high": 3, "medium": 2, "low": 1}
        
        best_crypto = max(rising_cryptos.items(),
                         key=lambda x: market_cap_priority.get(x[1]["market_cap"], 0))
        
        crypto_name = best_crypto[0]
        market_cap = best_crypto[1]["market_cap"]
        
        responses = [
            f"For profit potential, check out {crypto_name}! It's trending upward with a {market_cap} market cap. 📈",
            f"{crypto_name} is showing a rising trend with {market_cap} market capitalization - looking promising! 🚀",
            f"My profit-focused pick is {crypto_name}. It's on an upward trend in the {market_cap} market cap category. 💰"
        ]
        
        return random.choice(responses)
    
    def get_balanced_recommendation(self):
        # Calculate a balanced score considering both profitability and sustainability
        profitability_score = {
            "rising": 2, "stable": 1, "falling": 0  # Price trend
        }
        market_cap_score = {
            "high": 2, "medium": 1, "low": 0.5  # Market cap
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
        
        return (f"Based on both profitability and sustainability, I recommend {best_crypto}. "
                f"It has a {crypto_data['price_trend']} price trend, {crypto_data['market_cap']} "
                f"market cap, and a sustainability score of {crypto_data['sustainability_score']*10}/10! 🌟")
    
    def get_crypto_info(self, crypto):
        data = self.crypto_db[crypto]
        return (f"{crypto} Info:\n"
                f"📈 Price Trend: {data['price_trend'].capitalize()}\n"
                f"💰 Market Cap: {data['market_cap'].capitalize()}\n"
                f"⚡ Energy Use: {data['energy_use'].capitalize()}\n"
                f"🌱 Sustainability Score: {data['sustainability_score']*10}/10\n")
    
    def get_help_message(self):
        return ("Here's how you can interact with me:\n"
                "- Ask about sustainable or eco-friendly cryptocurrencies\n"
                "- Ask which crypto is trending up or best for profits\n"
                "- Request information about specific coins like Bitcoin or Ethereum\n"
                "- Ask for general recommendations\n\n"
                "Example questions:\n"
                "\"What's the most sustainable cryptocurrency?\"\n"
                "\"Which crypto is trending up?\"\n"
                "\"Tell me about Cardano\"\n"
                "\"What should I invest in?\"")

def main():
    bot = CryptoAdvisor("EcoCrypto")
    print(f"\n{bot.greet()}")
    print("Type 'exit' to quit.\n")
    print("⚠️ DISCLAIMER: Cryptocurrency investments are risky. This bot provides educational information only. Always do your own research before investing! ⚠️\n")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ["exit", "quit", "bye"]:
            print(f"\n{bot.name}: Thanks for chatting! Stay green in your crypto journey! 🌿")
            break
            
        response = bot.get_recommendation(user_input)
        print(f"\n{bot.name}: {response}")

if __name__ == "__main__":
    main()
