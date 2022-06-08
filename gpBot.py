import discord
import os
from ping import pingBot
from discord.ext import commands

intents = discord.Intents().all()
client = commands.Bot(command_prefix=',', intents=intents)

@client.event
async def on_ready():
  print("Logged in as {0.user}".format(client))

@client.event
async def on_message_delete(message): 
  #if the deleted message was the bot itself, return
  if message.author == client.user:
    return
  #if the message content has an "@", "<", and ">"(all of these are contained in an @ tag) check to see if it's a ghost ping
  if (message.content.find("@") != -1) and (message.content.find("<") != -1) and message.content.find(">") != -1:
    ghostPinged = False
    ghostPingMessage = message.content
    ghostPingMessageCopy = message.content
    while(ghostPingMessageCopy.find("@") != -1):
      ghostPingMessageCopy = ghostPingMessageCopy[ghostPingMessage.index('@') + 1:]
      if ghostPingMessageCopy.find(">") != -1:
        userID = ghostPingMessageCopy[:ghostPingMessageCopy.index('>')]
        #checking that the userID string is parsable to an int(i.e., is valid)
        if(userID.isdigit()):
          #for all members in the author's guild(server)
          for member in message.author.guild.members:
            if int(userID) == member.id:
              ghostPinged = True
              #replace the actual ping in the message to a dummy ping 
              ghostPingMessage = ghostPingMessage.replace("<@" + userID + ">", "@" + member.name)
        #checking if the inner id is a role ping
        else:
          if(userID.find("&") != -1):
            userID = userID[userID.index('&') + 1:]
            if not userID.isdigit(): 
              break
            for role in message.author.guild.roles:
              if(role.id == int(userID)):
                ghostPinged = True
                #replace the actual ping in the message to a dummy ping 
                ghostPingMessage = ghostPingMessage.replace("<@&" + userID + ">", "@" + role.name)
      else: 
        break
    if(ghostPinged):
      await message.channel.send("<@" + str(message.author.id) + "> just sent a ghost ping with message:\n" + ghostPingMessage)
  if message.reference:
    if message.reference.resolved:
      ghostPingMessage = message.content
      ghostPingMessageCopy = message.content
      while(ghostPingMessageCopy.find("@") != -1):
        ghostPingMessageCopy = ghostPingMessageCopy[ghostPingMessage.index('@') + 1:]
        if ghostPingMessageCopy.find(">") != -1:
          userID = ghostPingMessageCopy[:ghostPingMessageCopy.index('>')]
          #checking that the userID string is parsable to an int(i.e., is valid)
          if(not userID.isdigit()):
            continue
          #for all members in the author's guild(server)
          for member in message.author.guild.members:
            if int(userID) == member.id:
              #replace the actual ping in the message to a dummy ping 
              ghostPingMessage = ghostPingMessage.replace("<@" + userID + ">", "@" + member.name)
        else: 
          break
      await message.channel.send("<@" + str(message.author.id) + "> just sent a ghost ping to @" + message.reference.resolved.author.name + " with message:\n"  + ghostPingMessage )
    
@client.event
async def on_message_edit(before, after):
  if len(before.mentions) != len(after.mentions):
    ghostPingMessage = before.content
    ghostPingMessageCopy = before.content
    while(ghostPingMessageCopy.find("@") != -1):
      ghostPingMessageCopy = ghostPingMessageCopy[ghostPingMessage.index('@') + 1:]
      if ghostPingMessageCopy.find(">") != -1:
        userID = ghostPingMessageCopy[:ghostPingMessageCopy.index('>')]
        #checking that the userID string is parsable to an int(i.e., is valid)
        if(not userID.isdigit()):
          continue
        #for all members in the author's guild(server)
        for member in before.author.guild.members:
          if int(userID) == member.id:
            #replace the actual ping in the message to a dummy ping 
            ghostPingMessage = ghostPingMessage.replace("<@" + userID + ">", "@" + member.name)
      else: 
        break
    await before.channel.send("<@" + str(before.author.id) + "> just sent a ghost ping with message:\n" + ghostPingMessage)
    
pingBot()
try:
  client.run(os.environ['PASSWORD'])
except:
  os.system("kill 1")
