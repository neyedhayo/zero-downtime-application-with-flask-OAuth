import os
import tweepy
from flask import Flask
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)  # Corrected this line

@app.route('/')
def hello_world():
    return 'Hello, World from v1!'

@app.route('/login')
def login():
    consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
    consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

    if not (consumer_key and consumer_secret and access_token and access_token_secret):
        return 'Environment variables are not set correctly.'

    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, access_token, access_token_secret
    )
    api = tweepy.API(auth)

    try:
        user = api.verify_credentials()
        return f'Hello, {user.screen_name}!'
    except tweepy.TweepError as e:
        return f'Failed to authenticate: {str(e)}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
