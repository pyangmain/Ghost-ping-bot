#this class allows the bot to be constantly pinged so the replit server, and therefore the bot, never goes down
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return "Server is still up"

def run():
  app.run(host='0.0.0.0', port=8080)

def pingBot():
  t = Thread(target=run)
  t.start()