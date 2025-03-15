import os
import random
import time
import tweepy
import requests
from dotenv import load_dotenv

load_dotenv()

class MarketingAgent:
    def __init__(self):
        self.accounts = [1, 2, 3]
        self.base_prompt = "Create engaging AI-related tweet in English. Include 1-2 relevant hashtags and emojis. Keep it under 280 characters."
        print("🔄 Marketing Agent Initialized")

    def get_twitter_client(self, account_num: int):
        return tweepy.Client(
            consumer_key=os.getenv(f"TWITTER_API_KEY_{account_num}"),
            consumer_secret=os.getenv(f"TWITTER_API_SECRET_{account_num}"),
            access_token=os.getenv(f"TWITTER_ACCESS_TOKEN_{account_num}"),
            access_token_secret=os.getenv(f"TWITTER_ACCESS_TOKEN_SECRET_{account_num}")
        )

    def generate_content(self):
        try:
            headers = {
                "Authorization": f"Bearer {os.getenv('DEEPSEEK_OPENROUTER_API_KEY')}",
                "HTTP-Referer": "https://superior-agents.com",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": self.base_prompt}]
                },
                timeout=10
            )
            return response.json()['choices'][0]['message']['content']
            
        except Exception as e:
            print(f"Content generation error: {str(e)}")
            return "Exploring the future of AI! 🤖 #AI #Technology"

    def post_tweet(self):
        try:
            account_num = random.choice(self.accounts)
            client = self.get_twitter_client(account_num)
            content = self.generate_content()
            
            client.create_tweet(text=content)
            print(f"✅ Tweet posted from Account {account_num}: {content}")
            return True
            
        except Exception as e:
            print(f"🚨 Posting error: {str(e)}")
            return False

    def run(self):
        while True:
            success = self.post_tweet()
            wait_time = 3600 if success else 300  # 1 hour or 5 minutes
            print(f"⏳ Next post in {wait_time//60} minutes")
            time.sleep(wait_time)

if __name__ == "__main__":
    MarketingAgent().run()
