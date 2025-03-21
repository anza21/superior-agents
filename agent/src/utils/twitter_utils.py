import os
import random
from dotenv import load_dotenv

load_dotenv()

def load_random_twitter_account():
    index = random.randint(1, 11)

    def get_env(key_base):
        return os.getenv(f"{key_base}_{index}")

    return {
        "index": index,
        "key": get_env("TWITTER_API_KEY"),
        "secret": get_env("TWITTER_API_SECRET"),
        "access_token": get_env("TWITTER_ACCESS_TOKEN"),
        "access_token_secret": get_env("TWITTER_ACCESS_TOKEN_SECRET"),
        "proxy": os.getenv(f"PROXY_{index}", "NO_PROXY")
    }
