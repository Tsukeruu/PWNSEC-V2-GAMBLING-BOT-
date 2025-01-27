import discord
from discord.ext import commands, tasks
import time
import os

AUTHORIZED_USER_ID = [] #input the user ids you want that listen to the bot (important)


bot = commands.Bot(command_prefix="!", help_command=None, self_bot=True, chunk_guilds_at_startup=True)

token = "" #input token here

@bot.event
async def on_ready():
    os.system('cls')
    print(f"Logged in as {bot.user}")
    print('type !help to get started')
    autoCollect.start()
    time.sleep(3)
    autoDep.start()

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

[BACKGROUND_TASKS:]
    [Auto_deposit] = True --Automatically deposits all cash every 1 hour
    [Auto_collect] = True --Automatically collects cash every 6 hours
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
    elif (message.author.id in AUTHORIZED_USER_ID) and message.content.startswith("!exit"):
        async with message.channel.typing():
            time.sleep(0.4)
            await message.channel.send("Exiting!")
        os._exit(0)
    await bot.process_commands(message)


@tasks.loop(hours=6)
async def autoCollect():
    channel = bot.get_channel(1333438695948288030) #change channel id incase the channel got deleted
    await channel.send("-collect")

@tasks.loop(hours=1)
async def autoDep():
    channel = bot.get_channel(1333438695948288030)
    await channel.send("-deposit all")


bot.run(token)

