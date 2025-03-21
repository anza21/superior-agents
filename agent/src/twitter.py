import os
import tweepy
from dotenv import load_dotenv
from src.utils.twitter_utils import load_random_twitter_account
from dataclasses import dataclass

@dataclass
class TweetData:
    id: str | None = None
    text: str | None = None
    created_at: str | None = None
    author_id: str | None = None
    author_username: str | None = None
    thread_id: str | None = None

class TweepyTwitterClient:
    def __init__(self):
        load_dotenv()
        account = load_random_twitter_account()
        self.account_index = account["index"]

        rag_url = os.getenv("RAG_SERVICE_URL", "")

        # ✅ ΟΡΘΗ χρήση proxy — ΜΟΝΟ για εξωτερικά endpoints, ΟΧΙ για localhost
        if account["proxy"] and account["proxy"] != "NO_PROXY":
            if "localhost" not in rag_url and "127.0.0.1" not in rag_url:
                os.environ["HTTP_PROXY"] = account["proxy"]
                os.environ["HTTPS_PROXY"] = account["proxy"]
                print(f"🌐 Proxy enabled for external APIs: {account['proxy']}")
            else:
                print("🔒 Skipping proxy for localhost services (e.g. RAG API)")
        else:
            print("🌐 No proxy used.")

        self.client = tweepy.Client(
            consumer_key=account["key"],
            consumer_secret=account["secret"],
            access_token=account["access_token"],
            access_token_secret=account["access_token_secret"],
            wait_on_rate_limit=True
        )

        self.api_client = tweepy.API(
            auth=tweepy.OAuth1UserHandler(
                consumer_key=account["key"],
                consumer_secret=account["secret"],
                access_token=account["access_token"],
                access_token_secret=account["access_token_secret"]
            )
        )

        print(f"✅ Using TWITTER ACCOUNT #{account['index']}")
        print(f"📡 RAG API URL: {rag_url}")

    def get_count_of_followers(self):
        try:
            user = self.api_client.verify_credentials()
            return user.followers_count
        except Exception as e:
            print(f"❌ Error fetching follower count: {e}")
            return 0
