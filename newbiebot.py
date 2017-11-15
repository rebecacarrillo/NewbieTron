import os
import bot_constants
import logging
import time
import random
from configparser import ConfigParser
from slackclient import SlackClient


# Constants
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
BOT_NAME = conf.get(BOT_NAME)
BOT_ID = conf.get(BOT_ID)
AT_BOT = "<@" + BOT_ID + ">"


# Instantiate Slack Client
slack_client = SlackClient(SLACK_BOT_TOKEN)
bc = bot_constants

def list_channels(self):
    channels_call = slack_client.api_call("channels.list")
    if channels_call.get('ok'):
        return channels_call['channels']
    else:
        return None


def channel_info(channel_id):
    channel_info = slack_client.api_call("channels.info",
            channel=channel_id)
    if channel_info:
        return channel_info['channel']
    else:
        return None

def send_message(channel_id, message):
    slack_client.api_call("chat.postMessage",
            channel=channel_id,
            text=message,
            username='newbiebot',
            icon_emoji=':robot_face:')

def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                        output['channel']
    return None, None


def test_response(message, channel_id):
    message = message.lower()
    response = "Hi! Good question. Not sure I know the answer."

    if message in bc.GREETING_KEYWORDS:
        response = random.choice(bc.GREETING_RESPONSES)
    if message in bc.RUDE_INPUT:
        response = random.choice(bc.RUDE_RESPONSES)
    if message.startswith(bc.JOKE_COMMAND):
        response = random.choice(bc.JOKE_RESPONSES)

    message_clean = message.replace("?", "")
    message_words = message_clean.split(' ')
    for word in message_words:
        if word in bc.GENERAL_KEYWORDS:
            response = select_keyword_response(word)
            #response = "I know that! Stay tuned."

    slack_client.api_call('chat.postMessage', channel=channel,
            text=response, as_user=True)

def select_keyword_response(word):
    bc_keys = bc.GENERAL_KEYWORDS
    bc_responses = bc.KEYWORD_RESPONSES
    if word in bc_keys:
        response = bc_responses[word]
        return response
    else:
        response = "select_keyword_response error: input is gross"

if __name__=="__main__":
    WS_DELAY = 1
    if slack_client.rtm_connect():
        print("Bot up and running")
        while True:
            message, channel = parse_slack_output(slack_client.rtm_read())
            if message and channel:
                test_response(message, channel)
            time.sleep(WS_DELAY)
    else:
        print("Connection failed. Invalid slack token or bot id")




