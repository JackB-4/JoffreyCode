import discord
import os
import requests
import json
import random
import threading,time,sys
import variables
token = "OTE1Nzk1NTc4ODg0MDk2MDQx.YagzGA.n58O2SJKo4okdf5idZbbeUW-ZCo"

client = discord.Client()
client.anger = 0

#Inspiration Quote

def getQuote():
    response = requests.get("https://zenquotes.io/api/random")
    jsondata = json.loads(response.text)
    quote = jsondata[0]["q"] + " -" + jsondata[0]['a']
    return(quote)

#Anger system

def angerUp(probability):
    angerRaise = random.random() < probability
    if angerRaise == True and client.anger != 10:
      client.anger += 1
      print("Anger raised to: " + str(client.anger))

def angerDown(probability):
  angerLower = random.random() < probability
  if angerLower == True and client.anger != 0:
    client.anger -= 1
    print("Anger lowered to: " + str(client.anger))

def angerSet(input):
  client.anger = input
  print("Anger set to: " + str(client.anger))

#Login event

@client.event

async def on_ready():
  print("Logged in as {0.user}".format(client))

 #All chat interactions 

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  authorId = message.author.id
  verifiedUsers = [376158252330647553,285231967048302594]

#Help Chat

  if message.content.startswith("$help") and authorId in verifiedUsers:
    await message.channel.send("Hello my liege. How may I serve you?")
  elif message.content.startswith("$help"):
    await message.channel.send("I live only to serve my master. Do be gone.")

#Joffrey Support Chat
  supportTriggers = ["right joffrey?", "right joffrey", "joffrey support me", "joffrey back me up",
  "back me up joffrey", "am i right?"]
  supportiveResponse = ["Absolutely.", "I agree.", "Yup.", "You are right as always, sir.", "How I envy your wisdom."]
  unsupportiveResponse = ["No.", "No.", "No.", "Absolutely not.", "Absolutely not.","Absolutely not.",
  "Wrong, per usual.", "Wrong, per usual.", "Wrong, per usual.", "You are an absolute *failure*.", "You are an absolute *failure*."]

  if message.content in supportTriggers and authorId in verifiedUsers:
    await message.channel.send(random.choice(supportiveResponse))
  elif message.content in supportTriggers and authorId not in verifiedUsers:
    await message.channel.send(unsupportiveResponse[client.anger])


#Thank chat
  joffreyThanks = ["thanks", "thank you", "appreciate", "good job", "great job"]
  joffrey = "joffrey"

  for word in joffreyThanks:
    if word in message.content.lower() and joffrey in message.content.lower() and authorId in verifiedUsers:
      await message.channel.send("Anything for you, my liege.")
      angerDown(1)
    elif word in message.content.lower() and joffrey in message.content.lower():
      await message.channel.send("Your appreciation means nothing to me.")

#Reprimand Chat
  reprimands = ["joffrey stop", "joffrey, stop", "joffrey be quiet",
   "silence joffrey", "silence, joffrey", "be quiet joffrey", "joffrey shut up",
    "shut up joffrey", "fuck you joffrey", "fuck off joffrey"]
  positiveResponse = ["I apologize, sir.", "It won't happen again, my liege", "I am sincerely sorry, my lord.", "I apologize. You may strike me if necessary, master."]
  negativeResponse = ["Hmph.", "Hmph.", "Hmph.", "You have no right to reprimand me.",
   "You have no right to reprimand me.", "You have no right to reprimand me.", "Your commands mean nothing to me.", "Your commands mean nothing to me.",
    "Ha. You dare order me?", "Ha. You dare order me?", "*I'll murder you.*"]

  for word in reprimands:
    if word in message.content.lower() and authorId in verifiedUsers:
      await message.channel.send(message.author.mention + " " + random.choice(positiveResponse))
      angerUp(.2)
    elif word in message.content.lower() and authorId not in verifiedUsers:
      await message.channel.send(message.author.mention + " " + negativeResponse[client.anger])
      angerUp(.75)



#Inspiration Chat
  needInspiration = ["inspire", "inspiration", "motivate", "motivation"]

  for word in needInspiration:
    if word in message.content.lower():
      quote = getQuote()
      await message.channel.send(quote)

#Nolwen Chat
  if "bruh" in message.content.lower():
    print("bruh")
    await message.channel.send("bruh")

#Tea Chat
  def wantsTea(m):
    return m.author == message.author and m.content.lower() in affirmative


  desireTea = ["tea", "refreshment", "drink", "thirsty", "coffee", "parched", "dehydrated", "water"]
  affirmative = ["yes", "of course", "affirmative", "absolutely", "be great", "please"]
  negativeTea = ["Imagine needing hydration.", "Imagine needing hydration.", "Imagine needing hydration.",
   "Begging for a refreshment suits you.", "Begging for a refreshment suits you.", "Begging for a refreshment suits you.",
    "I have some gasoline, if that suits your taste.", "I have some gasoline, if that suits your taste.","I have some gasoline, if that suits your taste.",
    "If you're THAT thirsty I have something that can... hydrate you.", "*If you're THAT thirsty I have something that can... hydrate you.*"]

  for word in desireTea:
    if word in message.content.lower() and authorId in verifiedUsers:
      await message.channel.send("Would you like some tea my lord?")
      await client.wait_for('message', check=wantsTea, timeout = 10)
      await message.channel.send("Here is your tea, sir.")
    elif word in message.content.lower() and authorId not in verifiedUsers:
      await message.channel.send(negativeTea[int(client.anger)])

#Sleep Chat
  sleepTriggers = ["sleep", "tired", "bed", "goodnight", "gn", "good night", "nap"]
  positiveSleep = ["I hope your rest is fulfilling, sir.", "Sleep well, my liege.", "I will fervently await your awakening."]
  negativeSleep = ["Imagine sleeping", "Imagine sleeping", "Imagine sleeping", "Sleep is unecessary.", "Sleep is unecessary.", "Sleep is unecessary.",
   "Sleep is for the weak.", "Sleep is for the weak.", "Sleep is for the weak.", "I can put you to sleep...", "I can put you to sleep . . ."]

  for word in sleepTriggers:
    if word in message.content.lower() and authorId in verifiedUsers:
      await message.channel.send(random.choice(positiveSleep))
    elif word in message.content.lower():
      await message.channel.send(negativeSleep[int(client.anger)])

#Swear Jar Chat
  badWords = ["fuck", "shit", "bitch", "asshole", "hell", "nigga", "whore", "slut"]
  strangerResponse = ["Profanity is strictly disallowed in this server.", "Profanity is strictly disallowed in this server.",
  "Profanity is strictly disallowed in this server.", "I will not tolerate the use of such language.", 
  "I will not tolerate the use of such language.", "I will not tolerate the use of such language.", "Language. There are children!", 
  "Language. There are children!", "Such insolence!", "Such insolence!", "That's it. You don't get your allowance this week."]
  respectfulResponse = ["Such insight.", "What wisdom.", "Your eloquence amazes me."]

  if "whore"in message.content.lower() and authorId in verifiedUsers:
    await message.channel.send("Only for you, master.")
    await message.add_reaction("\N{THUMBS UP SIGN}")

  for word in badWords:
    if word in message.content.lower() and authorId not in verifiedUsers:
      await message.add_reaction("\N{THUMBS DOWN SIGN}")
      await message.channel.send(strangerResponse[client.anger])
      angerUp(.5)
    elif  word in message.content.lower() and authorId in verifiedUsers and word != "whore":
      await message.add_reaction("\N{THUMBS UP SIGN}")
      await message.channel.send(random.choice(respectfulResponse)) 

#Anger Override

  def angerCheck(message):
    if int(message.content) >= 0 and int(message.content) <= 10 and message.author.id in verifiedUsers:
      angerSet(int(message.content))
      return True

  if "$anger" in message.content.lower() and authorId in verifiedUsers:
    await message.channel.send("Accepting anger input.")
    await client.wait_for('message', check=angerCheck, timeout = 10)
    await message.channel.send("Anger is now at: " + str(client.anger))
  
  resetTriggers = ["reset hypnosis", "joffrey, factory reset", "joffrey factory reset", "joffrey reboot", "joffrey, reboot"]

  if message.content.lower() in resetTriggers and authorId in verifiedUsers:
    client.anger = 0
    print("Anger returned to: " + str(client.anger))
    await message.channel.send("Greetings, my liege. I apologize for any former... inconviences.")


client.run(token)
