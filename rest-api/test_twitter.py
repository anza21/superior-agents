from fastapi import FastAPI
import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/test_twitter")
def test_twitter():
    try:
        auth = tweepy.OAuth1UserHandler(
            os.getenv("TWITTER_API_KEY_1"),
            os.getenv("TWITTER_API_SECRET_1"),
            os.getenv("TWITTER_ACCESS_TOKEN_1"),
            os.getenv("TWITTER_ACCESS_TOKEN_SECRET_1")
        )
        api = tweepy.API(auth)
        user = api.verify_credentials()
        return {"status": "success", "username": user.screen_name}
    except Exception as e:
        return {"status": "error", "message": str(e)}
