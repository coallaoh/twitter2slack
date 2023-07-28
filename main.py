from datetime import datetime
from datetime import timedelta
import os

import gspread
import pytz
from slack import WebClient
from slack_bolt import App

SLACK_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")
TIME_ZONE = os.getenv("TIME_ZONE")
GSPREAD_PRIVATE_KEY = os.getenv("GSPREAD_PRIVATE_KEY")
GSPREAD_CLIENT_EMAIL = os.getenv("GSPREAD_CLIENT_EMAIL")


def set_time_zone(datetime_object):
    timezone = pytz.timezone(TIME_ZONE)
    return timezone.localize(datetime_object)


def filter_list_of_rows(list_of_rows):
    for row in list_of_rows:
        today = set_time_zone(datetime.today()).date()
        tweet_date = set_time_zone(datetime.strptime(row[0], '%B %d, %Y at %I:%M%p')).date()
        if tweet_date == today - timedelta(days=1):
            yield row


class Twitter2Slack(object):
    def __init__(self):
        gc = gspread.service_account_from_dict({
            "private_key": GSPREAD_PRIVATE_KEY.replace("\\n", "\n"),
            "client_email": GSPREAD_CLIENT_EMAIL,
            "token_uri": "https://oauth2.googleapis.com/token",
        })
        self.sheet = gc.open("coallaoh's tweet DB")
        self.app = App(token=SLACK_TOKEN)
        self.slack = WebClient(token=SLACK_TOKEN)

    def send_slack_message(self, text):
        self.slack.chat_postMessage(channel=SLACK_CHANNEL_ID, text=text)

    def scan_gspread_and_send_slack(self):
        self.slack.chat_postMessage(channel=SLACK_CHANNEL_ID,
                                    text=f"===== {datetime.today().date().strftime('%d %B %Y')} ====="
                                         f"Hello from your bot! :robot_face: \n"
                                         f"Here's today's AI news roundup from @Joon \n")
        list_of_rows = self.sheet.sheet1.get_values()
        for row in filter_list_of_rows(list_of_rows):
            self.send_slack_message(row[2])
            print(row)


def main():
    twitter2slack = Twitter2Slack()
    twitter2slack.scan_gspread_and_send_slack()


if __name__ == "__main__":
    main()
