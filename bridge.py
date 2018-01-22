# Import modules
from slackclient import SlackClient
import logging
import sys
import discord
import asyncio
from config import *

# Set up Logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

handler = logging.FileHandler(log_file)
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

#configure Slack and Discord

if SlackApiKey == "":
	logger.error("There wasn't an API key for Slack specified. Quitting...")
	sys.exit(1)

if DiscordApiKey == "":
	logger.error("There wasn't an API key for Discord specified. Quitting...")
	sys.exit(1)


# Connect to Slack
sc = SlackClient(SlackApiKey)
sc.rtm_connect()

# Connect to Discord
client = discord.Client()
# Set a Realtime connection via Discord
	# If message pass it through Slack
# Set a Realtime connection via Slack
while True:
	for slack_message in sc.rtm_read():
		message = slack_message.get("text")
		user = slack_message.get("user")
		full_message = "<Slack>[{}] {}".format(user,message)
		print(full_message)
		if not message or not user:
			continue
		client.send_message('405081669368807426', full_message)

	# If message pass it through Discord

client.run(DiscordApiKey)
