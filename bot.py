from pathlib import Path
from random import choice
import discord
from discord.ext import commands, tasks

status = ['sad songs for sad niBBas', 'with your waifu', 'with your hair :)']
welcome = ['Hello there!', 'Heyyyyyyyy!', "Stfu i'm trying to concentrate", 'Konnichiwa!', 'Hello']


class MusicBot(commands.Bot):
    def __init__(self):
        self._cogs = [p.stem for p in Path(".").glob("./bot/cogs/*.py")]
        super().__init__(command_prefix=self.prefix, case_insensitive=True)

    def setup(self):
        print("Running setup...")

        for cog in self._cogs:
            self.load_extension(f"bot.cogs.{cog}")
            print(f" Loaded `{cog}` cog.")

        print("Setup complete.")

    def run(self):
        self.setup()

        print("Running bot...")
        super().run(TOKEN, reconnect=True)

    async def shutdown(self):
        print("Closing connection to Discord...")
        await super().close()

    async def close(self):
        print("Closing on keyboard interrupt...")
        await self.shutdown()

    async def on_connect(self):
        print(f" Connected to Discord (latency: {self.latency * 1000:,.0f} ms).")

    async def on_resumed(self):
        print("Bot resumed.")

    async def on_disconnect(self):
        print("Bot disconnected.")

    @tasks.loop(seconds=900)
    async def change_status(self):
        # sets status of the bot
        await self.change_presence(activity=discord.Game(choice(status)))
        

    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        self.change_status.start()
        print('We have logged in as {0.user}'.format(self))
        print("Bot ready.")

    async def prefix(self, bot, msg):
        return commands.when_mentioned_or(".")(bot, msg)

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)

        if ctx.command is not None:
            await self.invoke(ctx)

    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)

    '''@commands.command(name="ping", help='Returns the latency')
    async def ping(self, ctx):
        await ctx.send(f'**Pong!** latency:{round(self.latency * 1000)} ms')'''

    @commands.command(name='hello', help='Returns the welcome message')
    async def hello(ctx):
        await ctx.send(choice(welcome))

    @commands.command(name='credits', help='Returns the credits')
    async def hello(ctx):
        await ctx.send('Developed with love by dbj & HumanExtreme')
