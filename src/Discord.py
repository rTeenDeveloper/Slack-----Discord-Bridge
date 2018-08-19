"""
Discord.py

This is the handler for Discord that posts to Slack.
"""

# Imports
from slackclient import SlackClient
import sys
import discord
import asyncio
import logging
from config import *

# Set up Logging.
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

handler = logging.FileHandler(log_file)
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

# Check if Api Key are supplied. Else the bridge won't be able to start at all.
if DiscordApiKey == "":
	logger.error("There wasn't an API key for Discord specified. Quitting...")
	sys.exit(1)
elif DiscordApiKey == "":  
	DiscordApiKey = os.environ['DiscordApiKey']
else:
	pass

if SlackApiKey == "":
	logger.error("There wasn't an API key for Slack specified. Quitting...")
	sys.exit(1)
elif SlackApiKey == "":  
	SlackApiKey = os.environ['SlackApiKey']
else:
	pass

# Connect to Discord and Slack.
sc = SlackClient(SlackApiKey)
client = discord.Client()

lastMessage = ''

# If logged in Log it.
@client.event
async def on_ready():
	logger.info('[Discord] Logged in as {} ({})'.format(client.user.name, client.user.id))

# If there is a message send it to Slack
@client.event
async def on_message(message):
	# We do not want the bot to reply to itself
	if message.author == client.user:
		return

	# Handle Channel
	channel = ""
	for slackChan, discordChan in channels.items():
		if message.channel.id == discordChan:
			channel = slackChan

	# Handle File Uploads
	if message.attachments:
		fileURL = message.attachments[0]['url']
		sc.api_call("chat.postMessage", channel=channel, as_user=True, text=fileURL)

	print(channel)
	full_message = '[Discord]({}) {}'.format(message.author,message.content)
		
	if lastMessage != full_message:
		logger.info(full_message)
		sc.api_call("chat.postMessage", channel=channel, as_user=True, text=full_message)
		lastMessage = full_message
		
client.run(DiscordApiKey)
