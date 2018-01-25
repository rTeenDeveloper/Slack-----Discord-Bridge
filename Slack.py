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

baseURL = "https://discordapp.com/api/channels/{}/messages".format('405081669368807426')
headers = { "Authorization":"Bot {}".format(DiscordApiToken),
			"User-Agent":"myBotThing (http://some.url, v0.1)",
"Content-Type":"application/json", }

while True:
	for slack_message in sc.rtm_read():
		message = slack_message.get("text")
		user = slack_message.get("user")
		full_message = "[Slack]({}) {}".format(user,message)
		print(full_message)
		if not message or not user:
			continue
		# If message send it via Discord	
		POSTedJSON = json.dumps ( {"content":full_message} )
		r = requests.post(baseURL, headers = headers, data = POSTedJSON)

