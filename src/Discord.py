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

if SlackApiKey == "":
	logger.error("There wasn't an API key for Slack specified. Quitting...")
	sys.exit(1)

# Connect to Discord and Slack.
sc = SlackClient(SlackApiKey)
client = discord.Client()

# If logged in Log it.
@client.event
async def on_ready():
	logger.info('Logged in as')
	logger.info(client.user.name)
	logger.info(client.user.id)
	logger.info('------')

# If there is a message send it to Slack
@client.event
async def on_message(message):
	# We do not want the bot to reply to itself
	if message.author == client.user:
		return

	full_message = '[Discord]({}) {}'.format(message.author,message.content)
	logger.info(full_message)
	sc.api_call("chat.postMessage", channel='C3LURBNGZ', as_user=True, text=full_message)


client.run(DiscordApiKey)
