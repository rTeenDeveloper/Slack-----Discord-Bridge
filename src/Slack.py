from slackclient import SlackClient
import sys
import logging
import requests
import json
from config import *

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

handler = logging.FileHandler(log_file)
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

if SlackApiKey == "":
	logger.error("There wasn't an API key for Slack specified. Quitting...")
	sys.exit(1)

if DiscordApiKey == "":
	logger.error("There wasn't an API key for Discord specified. Quitting...")
	sys.exit(1)	

sc = SlackClient(SlackApiKey)
sc.rtm_connect()

baseURL = "https://discordapp.com/api/channels/{}/messages".format('405081669368807426')
headers = { "Authorization":"Bot {}".format(DiscordApiKey),
			"User-Agent":"DiscordSlackBridge (http://reddit.com/r/teendeveloper, v0.1)",
"Content-Type":"application/json", }

while True:
	for slack_message in sc.rtm_read():
		message = slack_message.get("text")
		author = slack_message.get("user")
		if not message or not author or author == SlackBotUserID:
			continue
		# If there is a message send it via Discord
		username = sc.api_call("users.info", user=author)
		full_message = "[Slack]({}) {}".format(username['user']['name'],message)
		logger.info(full_message)
		POSTedJSON = json.dumps ({"content":full_message})
		r = requests.post(baseURL, headers = headers, data = POSTedJSON)

