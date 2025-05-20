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

@bot.event
async def on_ready():
    os.system('cls')
    print(f"Logged in as {bot.user}")
    print('type !help to get started')
    autoBeg.start()
    autoDep.start()
    #autoCollect.start()
    #time.sleep(3)

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
    ["!gpt":] this simply allows you to use chatgpt via discord, however you may need to input your api-key
    ["yoru give me a joke"]: self explanatory
                                      
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
            await message.channel.send(fetch_Response(prompt,link))

    elif (message.author.id in AUTHORIZED_USER_ID) and message.content == "yoru give me a joke":
        try:      
            jokes = [
                "Why don’t skeletons fight each other? They don’t have the guts!",
                "Why did the scarecrow win an award? Because he was outstanding in his field!",
                "Why did the bicycle fall over? Because it was two-tired!",
                "What’s orange and sounds like a parrot? A carrot!",
                "Why did the golfer bring two pairs of pants? In case he got a hole in one!",
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "Why was the JavaScript developer sad? Because he didn’t ‘null’ his feelings!",
                "I told my WiFi it was bad. Now it won’t talk to me!",
                "Why did the PowerPoint presentation cross the road? To get to the other slide!",
                "How do you comfort a JavaScript bug? You console it!",
                "Why don’t eggs tell jokes? They might crack up!",
                "I told my suitcase there will be no vacations this year. Now I’m dealing with emotional baggage!",
                "Why did the tomato blush? Because it saw the salad dressing!",
                "What did the sushi say to the bee? Wasabi!",
                "Why don’t bananas ever feel lonely? Because they hang out in bunches!",
                "What do you call a factory that makes good products? A satis-factory!",
                "Why did the duck get a promotion? Because he was a quack at his job!",
                "What do you call a pile of kittens? A meow-tain!",
                "Why do cows have hooves instead of feet? Because they lactose!",
                "Why don’t some fish play piano? Because you can’t tuna fish!",
                "Why did the chicken go to the seance? To talk to the other side!",
                "What do you call fake spaghetti? An impasta!",
                "How do you organize a space party? You planet!",
                "Why don’t oysters donate to charity? Because they are shellfish!",
                "What do you call a bear with no teeth? A gummy bear!",
                "Why couldn’t the leopard hide? Because he was always spotted!",
                "What happens when a frog’s car breaks down? It gets toad away!",
                "Why don’t secrets last in a bank? Because they always get leaked!",
                "Why did the music teacher go to jail? Because she got caught with a high note!",
                "Why do seagulls fly over the sea? Because if they flew over the bay, they’d be bagels!",
                "Why do vampires always seem sick? Because they’re always coffin!",
                "Why did the math book look sad? Because it had too many problems!",
                "What did one wall say to the other wall? 'I’ll meet you at the corner!'",
                "Why do elephants never use computers? They’re afraid of the mouse!",
                "Why did the belt get arrested? It was holding up a pair of pants!"
            ]
            #i sincerely apologize for these significantly unfunny jokes that chat-gpt have generated for me
            random_joke = random.choice(jokes)

            async with message.channel.typing():
                time.sleep(2)
                await message.channel.send(f'{message.author.mention} {random_joke}')

        except UnboundLocalError as c:
            print()
    

        
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

