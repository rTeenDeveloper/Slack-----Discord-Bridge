"""
Slack.py

This is the handler for Slack that posts to Discord.
"""

# Imports.

from slackclient import SlackClient
import sys
import logging
import requests
import json
from config import *

# Set up Logging.
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

handler = logging.FileHandler(log_file)
handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)

# Check if Api Key are supplied. Else the bridge won't be able to start at all.

if SlackApiKey == "":
	logger.error("There wasn't an API key for Slack specified. Quitting...")
	sys.exit(1)
elif SlackApiKey == "":  
	SlackApiKey = os.environ['SlackApiKey']
else:
	pass

if DiscordApiKey == "":
	logger.error("There wasn't an API key for Discord specified. Quitting...")
	sys.exit(1)
elif DiscordApiKey == "":  
	DiscordApiKey = os.environ['DiscordApiKey']
else:
	pass

# Connect to Slack.
sc = SlackClient(SlackApiKey)
sc.rtm_connect()

# Set up URL's and headers for Discord.
headers = { "Authorization":"Bot {}".format(DiscordApiKey),
			"User-Agent":"DiscordSlackBridge (http://reddit.com/r/teendeveloper, v0.1)",
"Content-Type":"application/json", }

fullMessage = ''

# Run the Bridge 

# We have to query all users in slack to map their id to their names later. Querying every message
# does not have sense, so we will just do it now and then flush the cache when someone will
# enter the slack. Easy enough

try:
	usersList = sc.api_call(
		"users.list",
		channel = userListChannel
	)['members'] 
except:
	logger.error('[Slack] Failed to fetch users list! Converting mentions won\'t be available.')

while True:
	try:
		for slack_message in sc.rtm_read():
			event = slack_message.get("type")
			message = slack_message.get("text")
			author = slack_message.get("user")
			channel = slack_message.get("channel")

			if not message or not author or author == SlackBotUserID or event != "message":
				continue

			# Handle Channels
			discordChannel = ""

			if channel in channels:
				discordChannel = channels.get(channel)
			else:
				pass	

			# Message formatting section

			# Mentions. Valid mention in slack looks like this: <@username>
			if "@" in message: 
				# Split message to a spaces and then detect which of the expressions starts with <@ and ends with >
				expressions = message.split(' ')
				for expression in expressions:
					if expression[:2] == '<@' and expression[-1:] == '>':
						userId = expression[2:-1]
						# Now lets map it to username (if usersList exists)
						if (usersList):
							for user in usersList: 
								if (user['id'] == userId):
									userName = user['profile']['display_name']
							if (not userName):
								continue 
							message = message.replace(userId, userName)

			# If there is a message send it via Discord
			baseURL = "https://discordapp.com/api/channels/{}/messages".format(discordChannel)
			username = sc.api_call("users.info", user=author)
			full_message = "[Slack]({}) {}".format(username["user"]["profile"]["display_name"], message)
			if full_message != lastMessage:
				logger.info(full_message)
				POSTedJSON = json.dumps ({"content":full_message})
				r = requests.post(baseURL, headers = headers, data = POSTedJSON)
				lastMessage = full_message
				
	except KeyboardInterrupt:
		logger.info("[Slack] Exitting..")
		break
		sys.exit(1)
		
	"""
	Todo: Set up More Error Handlers!
	"""	
	#except: 
	#	logger.error("[Slack] RTM read failed! Check internet connection and restart script.")



