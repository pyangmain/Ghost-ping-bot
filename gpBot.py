#main bot
import discord
import os
from keep_alive import keep_alive

client = discord.Client()

@client.event
async def on_ready():
  print("Logged in as {0.user}".format(client))

@client.event
async def on_message_delete(message): 
  if message.author == client.user:
    return
  
  if message.content.find("@") != -1:
    await message.channel.send(message.author.display_name + "potentially just sent a ghost ping")

keep_alive()
client.run(os.environ['PASSWORD'])