import discord
from discord.ext import commands, tasks
import time
import os
import random
import openai
import requests

AUTHORIZED_USER_ID = [] 

bot = commands.Bot(command_prefix="!", help_command=None, self_bot=True, chunk_guilds_at_startup=True)
token = ""

def fetch_Response(prompt,link):
    data = {
        "model" : "llama3.2", #or any model of the server's downloaded models
        "prompt" : prompt,
        "stream" : False
    }
    answer = requests.post(link,json=data)
    if answer.status_code == 200:
        return (answer.json()).get('response')
    else:
        return 'AN ERROR HAS OCCURED WITHIN OLLAMA!'

def fetch_Joke(url):
    joke = (requests.get(url)).json()['joke']
    return joke


@bot.event
async def on_ready():
    os.system('cls')
    print(f"Logged in as {bot.user}")
    print('type !help to get started')
    autoBeg.start()
    autoDep.start()
    autoCollect.start()

@bot.event
async def on_message(message):
    if (message.author.id in AUTHORIZED_USER_ID) and message.content == "yoru give me my balance":
        async with message.channel.typing():
            time.sleep(1)
            await message.channel.send('YES MASTER RIGHT AWAY!')
            time.sleep(1)
            async with message.channel.typing():
                await message.channel.send(f'-bal {message.author.mention}')
    elif (message.author.id in AUTHORIZED_USER_ID) and message.content == "!help":
           async with message.channel.typing():
                time.sleep(0.4) 
           await message.channel.send('''```ini
[COMMANDS:]
    ["yoru give me my balance":] returns the balance of the master's id!
    ["!help":] sends these messages
    ["!jump <userid>":] basically robs the userid, the userid will be prompted as the second arg
    ["!exit":] terminates the python program!
    ["!gpt <prompt>":] uses the ollama LLM
    ["yoru give me a joke"]: self explanatory
    ["!whitelist <userid>"]: whitelists the user id to use yoru, however it will be temporary   
                                   
[BACKGROUND_TASKS:]
    [Auto_deposit] = True --Automatically deposits all cash every one hour
    [Auto_collect] = True --Automatically collects cash every six hours
    [Auto_beg] = True --Automatically runs the beg command once every two minutes
    ``` 
''')  
    elif (message.author.id in AUTHORIZED_USER_ID) and message.content.startswith("!jump"):
           try:         
                user = message.content.split()[1] #1
                if user.isdigit() or not user.isdigit():
                    async with message.channel.typing():
                        time.sleep(0.4)
                        await message.channel.send(f'-withdraw 10000')
                        time.sleep(0.4)
                        await message.channel.send(f'-rob {user}')
                else:
                    print('not a known datatype')
           except IndexError as i:
                print('INDEX ERROR!!')
    elif (message.author.id in AUTHORIZED_USER_ID) and message.content == "!exit":
        async with message.channel.typing():
            time.sleep(0.4)
            await message.channel.send("Exiting!")
        os._exit(0)
    elif (message.author.id in AUTHORIZED_USER_ID) and message.content.startswith("!gpt"):
        prompt = message.content.split(' ', 1)[1]
        link = "http://localhost:11434/api/generate"
        async with message.channel.typing():
            try:
                await message.channel.send(f'{message.author.mention} {fetch_Response(prompt,link)}')
            except requests.exceptions.ConnectionError as e:
                await message.channel.send(f'yo gng you gotta power up ollama to make ts shit work')
    elif (message.author.id in AUTHORIZED_USER_ID) and message.content.startswith('!whitelist'):
        userid = message.content.split(' ',1)[1]
        AUTHORIZED_USER_ID.append(int(userid))
        await message.channel.send(f"SUCCESSFULLY ADDED USERID('s): {userid}")
    elif (message.author.id in AUTHORIZED_USER_ID) and message.content == "yoru give me a joke":
        try:      
            joke = fetch_Joke("https://v2.jokeapi.dev/joke/Any?type=single")
            async with message.channel.typing():
                time.sleep(0.4)
                await message.channel.send(f'{message.author.mention} {joke}')
        except Exception as e:
            if isinstance(e,requests.ConnectionError):
                await message.channel.send(f'A CONNECTION ERROR HAS OCCURED')
                print(e)
            else:
                await message.channel.send(f'AN UNKOWN ERROR HAS OCCURED')
                print(e)
    await bot.process_commands(message)


@tasks.loop(hours=6)
async def autoCollect():
    channel = bot.get_channel(1257634691918598186) #change channel id incase the channel got deleted
    await channel.send("-collect")

@tasks.loop(hours=1)
async def autoDep():
    channel = bot.get_channel(1257634691918598186)
    await channel.send("-deposit all")

@tasks.loop(minutes=2,seconds=3)
async def autoBeg():
    channel = bot.get_channel(1257634691918598186)
    await channel.send("-beg")
    time.sleep(0.3)


bot.run(token)

