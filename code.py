import discord 
import os
import requests
import json
import random

client = discord.Client()

words_in = []
words_starts=[]

words_change = os.environ["wordschange"]
boring = ["boring", "i am bored","i'am bored","bored"]
intro_words = ["hi", "hello"]
exit_words = ["bye","I'm out","i am out","i'm out", "I am out"]

def get_joke():
  callback = requests.get("https://v2.jokeapi.dev/joke/any?/format=json&blacklistFlags=nsfw&type=single&lang=en") #("http://api.icndb.com/jokes/random")
  json_data = json.loads(callback.text)
  # joke = json_data["value"]["joke"]
  joke = str(json_data["joke"])+"\n"+"Joke Category: "+str(json_data["category"])
  return(joke)

def get_comic():
  callback = requests.get("https://xkcd.com/"+str(num)+"/info.0.json")
  json_data = json.loads(callback.text)
  comic = str(json_data["safe_title"])+"\n\n"+str(json_data["transcript"])
  return(comic)
def get_comicimg():
  callback = requests.get("https://xkcd.com/"+str(num)+"/info.0.json")
  json_data = json.loads(callback.text)
  comicimg = str(json_data["img"])+"  "+str(json_data["num"])
  return(comicimg)

def get_meme():
  callback = requests.get("https://meme-api.herokuapp.com/gimme/itsaunixsystem")
  json_data = json.loads(callback.text)
  meme = str(json_data["title"])+"\n"+str(json_data["url"])
  return(meme)

def update_wordin(wordin_message):
  if "wordin" in db.keys():
    wordin = db["wordin"]
    wordin.append(wordin_message)
    db["wordin"] = wordin
  else:
    db["wordin"] = [wordin_message]

def delete_wordin(index):
  wordin = db["wordin"]
  if len(wordin) > index:
    del wordin[index]
    db["wordin"] = wordin

def update_wordstarts(wordstarts_message):
  if "wordstarts" in db.keys():
    wordstarts = db["wordstarts"]
    wordstarts.append(wordstarts_message)
    db["wordstarts"] = wordstarts
  else:
    db["wordstarts"] = [wordstarts_message]

def delete_wordstarts(index):
  wordstarts = db["wordstarts"]
  if len(wordstarts) > index:
    del wordstarts[index]
    db["wordstarts"] = wordstarts

@client.event
async def on_ready():
  print("we have logged in as {0.user}".format(client))
  h = discord.Activity(type=discord.ActivityType.watching,name="at Discorders who type ' help.' ")
  
  await client.change_presence(status= discord.Status.online,activity=h)
  
  @client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith(tuple(intro_words)):
    joke = get_joke()
    await message.channel.send("Hello, then! Whats up??. 😀 " + """```"""+ str(joke) +" - Enjoy The Joke"+"""```""")

  # if message.content.startswith(tuple(exit_words)):
  if any(word in message.content for word in exit_words):
    await message.channel.send("okay bye 👋 ")

  if any(word in message.content for word in boring):
    def get_boring():
      callback = requests.get("https://www.boredapi.com/api/activity")
      json_data = json.loads(callback.text)
      act = str(json_data["activity"])
      return(act)
    await message.channel.send("If you are bored, "+get_boring())

  if message.content.startswith("comic."):
    global num
    num = random.randrange(2000)
    comic = get_comic()
    comicimg = get_comicimg()
    await message.channel.send("""```yaml\n"""+comic+"""\n```"""+ "\n"+comicimg)

  if message.content.startswith("meme."):
    meme = get_meme()
    await message.channel.send(meme)

  if message.content.startswith("help."):
    manual_help = ("""```elm\n                        \n |  |   |‾‾‾   |      |‾‾|\n |‾‾|   |‾‾‾   |      |‾‾\n         ‾‾‾    ‾‾‾     \n\nUSAGE:\n\nhelp.  -- for commands\n\nsearch.  \b some query to search web \b\n\ncomic. -- shows some random comic\n\nmeme. -- shows some random meme\n```""")
    await message.channel.send(manual_help)

  if message.content.startswith("search."):
    def splited():
      a_list = message.content.split(".")
      splited = a_list[1]
      return(splited)
    def get_search():
      spliteded = splited()
      answers = requests.get("https://api.duckduckgo.com/?q="+str(spliteded)+"&format=json")
      json_data = json.loads(answers.text)
      answer = str(json_data["AbstractText"])#+"\n"+str(json_data["RelatedTopics"][0]["Text"])
      return(answer)
    def get_url():
      spliteded = splited()
      answers = requests.get("https://api.duckduckgo.com/?q="+str(spliteded)+"&format=json")
      json_data = json.loads(answers.text)
      url = json_data["AbstractURL"]
      return(url)
    answer = get_search()
    url = get_url()
    if answer == "":
      await message.channel.send("Please, Search your query in a different way or refer link below if any")
    else:
      await message.channel.send("""```"""+answer+"""```""")
    await message.channel.send(str(url))

# word in
  options = words_in
  if "wordin" in db.keys():
    options.extend(db["wordin"])
    # options = options + db["wordin"]

  if message.content.startswith(",/add."):
    wordin_message = message.content.split(".")[1]
    update_wordin(wordin_message)
    await message.channel.send("ok, its added")

  if message.content.startswith(",/del"):
    wordin = []
    if "wordin" in db.keys():
      index = int(message.content.split(",/del",1)[1])
      delete_wordin(index)
      wordin_message = db["wordin"]
    await message.channel.send(wordin)
    
  if any(word in message.content for word in options):
    await message.channel.send(words_change)
# word startswith
  optionstarts = words_starts
  if "wordstarts" in db.keys():
    optionstarts.extend(db["wordstarts"])
    # options = options + db["wordin"]

  if message.content.startswith("//add."):
    wordstarts_message = message.content.split(".")[1]
    update_wordstarts(wordstarts_message)
    await message.channel.send("ok, its added")

  if message.content.startswith("//del"):
    wordstarts = []
    if "wordstarts" in db.keys():
      index = int(message.content.split("//del",1)[1])
      delete_wordstarts(index)
      wordstarts_message = db["wordstarts"]
    await message.channel.send(wordstarts)
    
  if message.content.startswith(tuple(optionstarts)):
    await message.channel.send(words_change)


client.run(os.environ['TOKEN'])
