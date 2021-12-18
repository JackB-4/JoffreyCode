import discord, requests, json, random
from datetime import datetime
from commands import *
from variables import *
token = "OTE1Nzk1NTc4ODg0MDk2MDQx.YagzGA.n58O2SJKo4okdf5idZbbeUW-ZCo"
verifiedUsers = [376158252330647553,285231967048302594]

client = discord.Client()
client.anger = 0

#National Days
def getDay():
  current_datetime = datetime.now()
  currentMonth = current_datetime.month
  currentDay = current_datetime.day
  print(str(currentMonth) + "/" + str(currentDay))
  dayResponse = requests.get("https://national-api-day.herokuapp.com/api/date/" + str(currentMonth) + "/" + str(currentDay))
  dayData = dayResponse.json()
  daySeperator = "\n"
  days = dayData["holidays"]
  processedDays = daySeperator.join(days)
  print(processedDays)
  return(processedDays)


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

def angerRandomize():
  randomChange = random.randint(-3,3)
  tempAnger = client.anger + randomChange
  if tempAnger > 10:
    tempAnger = 10
  if tempAnger < 0:
    tempAnger = 0
  return tempAnger


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

#Day Chat
  for word in dayTriggers:
    if word in message.content.lower():
      await message.channel.send(getDay())


#Help Chat

  if message.content.startswith("$help") and authorId in verifiedUsers:
    await message.channel.send("Hello my liege. How may I serve you?")
  elif message.content.startswith("$help"):
    await message.channel.send("I live only to serve my master. Do be gone.")
#Joffrey Support Chat

  if message.content in supportTriggers and authorId in verifiedUsers:
    await message.channel.send(random.choice(supportiveResponse))
    angerDown(.35)
  elif message.content in supportTriggers and authorId not in verifiedUsers:
    await message.channel.send(unsupportiveResponse[angerRandomize()])


#Thank chat

  for word in joffreyThanks:
    if word in message.content.lower() and joffrey in message.content.lower() and authorId in verifiedUsers:
      await message.channel.send("Anything for you, my liege.")
      angerDown(1)
    elif word in message.content.lower() and joffrey in message.content.lower():
      await message.channel.send("Your appreciation means nothing to me.")

#Reprimand Chat

  for word in reprimands:
    if word in message.content.lower() and authorId in verifiedUsers:
      await message.channel.send(message.author.mention + " " + random.choice(positiveResponse))
      angerUp(.2)
    elif word in message.content.lower() and authorId not in verifiedUsers:
      await message.channel.send(message.author.mention + " " + negativeResponse[angerRandomize()])
      angerUp(.75)


#Inspiration Chat

  for word in needInspiration:
    if word in message.content.lower():
      quote = getQuote()
      await message.channel.send(quote)
      angerDown(.35)

#Nolwen Chat
  if "bruh" in message.content.lower():
    print("bruh")
    await message.channel.send("bruh")
  if "gay" in message.content.lower():
    await message.add_reaction("🇬")
    await message.add_reaction("🇦")
    await message.add_reaction("🇾")

#Tea Chat
  def wantsTea(m):
    return m.author == message.author and m.content.lower() in affirmative

  for word in desireTea:
    if word in message.content.lower() and authorId in verifiedUsers:
      await message.channel.send("Would you like some tea my lord?")
      await client.wait_for('message', check=wantsTea, timeout = 10)
      await message.channel.send("Here is your tea, sir.")
      angerDown(.5)
    elif word in message.content.lower() and authorId not in verifiedUsers:
      await message.channel.send(negativeTea[int(angerRandomize())])

#Sleep Chat

  for word in sleepTriggers:
    if word in message.content.lower() and authorId in verifiedUsers and "figg" not in message.content.lower():
      await message.channel.send(random.choice(positiveSleep))
    elif word in message.content.lower() and "figg" not in message.content.lower():
      await message.channel.send(negativeSleep[angerRandomize()])

#Swear Jar Chat

  if "whore"in message.content.lower() and authorId in verifiedUsers:
    await message.channel.send("Only for you, master.")
    await message.add_reaction("\N{THUMBS UP SIGN}")

  for word in badWords:
    if word in message.content.lower() and authorId not in verifiedUsers:
      await message.add_reaction("\N{THUMBS DOWN SIGN}")
      await message.channel.send(strangerResponse[angerRandomize()])
      angerUp(.5)
    elif  word in message.content.lower() and authorId in verifiedUsers and word != "whore":
      await message.add_reaction("\N{THUMBS UP SIGN}")
      await message.channel.send(random.choice(respectfulResponse)) 
      angerDown(.25)
#Anger Override

  def angerCheck(message):
    if int(message.content) >= 0 and int(message.content) <= 10 and message.author.id in verifiedUsers:
      angerSet(int(message.content))
      return True

  if "$anger" in message.content.lower() and authorId in verifiedUsers:
    await message.channel.send("Accepting anger input.")
    await client.wait_for('message', check=angerCheck, timeout = 10)
    await message.channel.send("Anger is now at: " + str(angerRandomize()))

  if message.content.lower() in resetTriggers and authorId in verifiedUsers:
    client.anger = 0
    print("Anger returned to: " + str(client.anger))
    await message.channel.send("Greetings, my liege. I apologize for any former... inconviences.")

  if message.content.lower() in angerInquiry:
    await message.channel.send("On a scale from 0 to 10, I am at " + str(client.anger) + ".")

client.run(token)
