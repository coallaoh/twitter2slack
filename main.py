import os
from twython import Twython
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

TWITTER_APP_KEY = os.getenv('TWITTER_APP_KEY')
TWITTER_APP_SECRET = os.getenv('TWITTER_APP_SECRET')
TWITTER_OAUTH_TOKEN = os.getenv('TWITTER_OAUTH_TOKEN')
TWITTER_OAUTH_TOKEN_SECRET = os.getenv('TWITTER_OAUTH_TOKEN_SECRET')
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
SLACK_TOKEN = os.getenv('SLACK_TOKEN')
SLACK_CHANNEL_ID = "test"

twitter = Twython(TWITTER_APP_KEY, TWITTER_APP_SECRET, TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_TOKEN_SECRET)

# Get the most recent tweet
tweets = twitter.get_user_timeline(screen_name=TWITTER_USERNAME, count=1)
latest_tweet = tweets[0]['text']

# Get the Slack API credentials

slack = WebClient(token=SLACK_TOKEN)

# Post the tweet to a Slack channel
try:
    response = slack.chat_postMessage(channel=SLACK_CHANNEL_ID, text=latest_tweet)
except SlackApiError as e:
    assert e.response["error"]
