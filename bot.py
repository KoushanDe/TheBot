import discord, asyncio, youtube_dl
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()


def get_prefix(bot, msg):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    prefixes = ['.']  # Your bot prefix(s)

    return commands.when_mentioned_or(*prefixes)(bot, msg)


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=get_prefix, description='A Music bot', intents=intents)

exts = ['music']  # Add your Cog extensions here


@bot.event
async def on_ready():
    song_name = 'yt and .help'
    activity_type = discord.ActivityType.listening
    await bot.change_presence(activity=discord.Activity(type=activity_type, name=song_name))
    print(f'We have logged in as {bot.user}')
    print("Bot ready.")


@bot.command(name='ping', help='Returns the latency')
async def ping(ctx):
    await ctx.send(f'**Pong!** latency: {round(bot.latency * 1000)} ms')


@bot.command(name='credit', aliases=["dev"], help='developer info')
async def dev(ctx):
    await ctx.send('Developed with love by HumanExtreme#8178')


@bot.command(name='num', help='total number of server this bot is in')
async def num(ctx):
    await ctx.send(f"I'm in {len(bot.guilds)} servers!")


# @bot.command()
# async def egg(ctx):
#     await ctx.send('Fun games cooking in wizard kitchen!')


@bot.event
async def shutdown():
    print("Closing connection to Discord...")


@bot.event
async def close():
    print("Closing on keyboard interrupt...")


@bot.event
async def on_connect():
    print(f" Connected to Discord (latency: {bot.latency * 1000:,.0f} ms).")


for i in exts:
    bot.load_extension(i)

print("Running bot...")
bot.run(OS.environ[TOKEN], reconnect=True)

# os.environ['TOKEN']
