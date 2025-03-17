import requests
import os
import time
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

class TradingAgent:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(
            f"https://mainnet.infura.io/v3/{os.getenv('INFURA_PROJECT_ID')}"
        ))
        self.address = os.getenv("ETHER_ADDRESS")
        
    def get_eth_price(self):
        url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
        response = requests.get(url)
        return response.json()["ethereum"]["usd"]
    
    def execute_strategy(self):
        eth_price = self.get_eth_price()
        print(f"📈 Τρέχουσα τιμή ETH: ${eth_price}")
        
        if eth_price < 2500:
            print("🚀 Εκτέλεση αγοράς...")
        elif eth_price > 3500:
            print("💰 Εκτέλεση πώλησης...")
        else:
            print("💤 Αναμονή για ευκαιρίες...")
    
    def run(self):
        while True:
            try:
                balance = self.w3.eth.get_balance(self.address)
                print(f"🏦 Υπόλοιπο: {Web3.from_wei(balance, 'ether')} ETH")
                self.execute_strategy()
            except Exception as e:
                print(f"🚨 Σφάλμα: {str(e)}")
            
            time.sleep(300)  # Έλεγχος κάθε 5 λεπτά

if __name__ == "__main__":
    agent = TradingAgent()
    agent.run()
