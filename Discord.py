from slackclient import SlackClient
import sys
import discord
import asyncio
import logging
from config import *

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

handler = logging.FileHandler(log_file)
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


if DiscordApiKey == "":
	logger.error("There wasn't an API key for Discord specified. Quitting...")
	sys.exit(1)

if SlackApiKey == "":
	logger.error("There wasn't an API key for Slack specified. Quitting...")
	sys.exit(1)

sc = SlackClient(SlackApiKey)
client = discord.Client()

@client.event
async def on_ready():
	logger.info('Logged in as')
	logger.info(client.user.name)
	logger.info(client.user.id)
	logger.info('------')

@client.event
async def on_message(message):
	# we do not want the bot to reply to itself
	if message.author == client.user:
		return
	# If there is a message send it via Slack
	full_message = '[Discord]({}) {}'.format(message.author,message.content)
	logger.info(full_message)
	sc.api_call("chat.postMessage", channel='C3LURBNGZ', as_user=True, text=full_message)


client.run(DiscordApiKey)
