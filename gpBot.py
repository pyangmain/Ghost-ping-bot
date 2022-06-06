#main bot
import discord
import os
from ping import pingBot

client = discord.Client()

@client.event
async def on_ready():
  print("Logged in as {0.user}".format(client))

@client.event
async def on_message_delete(message): 
  if message.author == client.user:
    return
  
  if (message.content.find("@") != -1) and (message.content.find("<") != -1) and message.content.find(">") != -1:
    await message.channel.send("<@" + str(message.author.id) + "> potentially just sent a ghost ping")

pingBot()
try:
  client.run(os.environ['PASSWORD'])
except:
  os.system("kill 1")
