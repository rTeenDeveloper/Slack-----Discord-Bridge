# Slack<---->Discord Bridge 
A bridge we made for Slack to Discord. Bare in mind this is still work in progress.

### Requirements:
* Python3 
* Discord.py
* slack client

### Installation:
`pip install slackclient`

`python3 -m pip install -U discord.py`

### Getting Started:
* Get a Bot token from Slack and Discord
  * For Slack get it from: https://api.slack.com/apps?new_app=1
      * Add Bot as a Feature
      * Give it a name, username
      * Install it to your workspace
  * For Discord get it from: https://discordapp.com/developers/applications/me
      * Bundle a bot user
  * Invite it to your server using https://discordapp.com/oauth2/authorize?client_id=<CLIENT_ID_GOES_HERE>&scope=bot&permissions=0
* Fill out the config in the src folder.
* Run the Script either by running the scripts individually, using supervisor or using the bash script.

---
### Channels:
* For Slack Channel ID's can be found in the url: `https://rteendeveloper.slack.com/messages/C3LURBNGZ/`
In this case `C3LURBNGZ` is the Channel ID
* For Discord Channel ID's can be found by right click -> Copy ID. It should look something like this `391099113778970627`

Remember! The bot has to be in each of the channels so it can receive and send messages.


### Help:

For any Help feel free to open a issue our ask on our Slack :)
Link:  http://rteendeveloperslack.herokuapp.com/




