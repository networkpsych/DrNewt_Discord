import discord
import discord.utils
import logging
import random
from time import sleep
from typing import Optional
from discord.ext import commands, tasks
from youtubesearchpython import VideosSearch
from datetime import datetime



description = "I am a bot, beep boop"
intents = discord.Intents.default()
intents.members = True
drNewt = commands.Bot(command_prefix='~', description=description, intents=intents)


class DrNewt(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def get_members(self, ctx):
        # gets online members
        members = discord.utils.get(ctx.guild.members)
        await ctx.send(members)


    @commands.command()
    async def rollDice(self, ctx, dice_type: str, dice_amt: int):
        dice_list = []
        for i in range(dice_amt):
            match dice_type:
                case "d1": dice = 1
                case "d4": dice = random.randint(1, 4)
                case "d6": dice = random.randint(1, 6)
                case "d8": dice = random.randint(1, 8)
                case "d12": dice = random.randint(1, 12)
                case "d20": dice = random.randint(1, 20)
                case "d100": dice = random.randint(1, 100)
            if dice_amt > 1:
                dice_list.append(dice)
            else:
                break
        await ctx.send(f"ROLLING!!!!\n https://giphy.com/gifs/ThisIsMashed-animation-animated-mashed-iHcxDxXqOAC5o0639Q" )
        sleep(5) # 5 seconds seems like long enough to count dice.
        if dice_amt == 1:
            await ctx.send(f"You rolled {dice}")
        if dice_amt > 1:
            await ctx.send(f"You rolled {dice_amt} {dice_type} for a total of {sum(dice_list)}")
        if dice_amt > 100:
            # We really do not want some dingus rolling a lot of dice
            # just to crash the bot.
            await ctx.send(f"I can't roll that many!!")
        elif dice_amt <= 0:
            await ctx.send(f".... You didn't roll?")


    @commands.command()
    async def cool_kids(self, ctx, member: Optional[str]):
        # Get a guild member to see if they are cool.
        # Technically nobody is cool if they have to ask.
        if member:
            try:
                member = discord.utils.get(ctx.guild.members, name=member)
                await ctx.send(f"{member} is cool. {ctx.author.name} is not.")
            except commands.errors.MemberNotFound:
                await ctx.send(f"{member} is definitely not cool because they're not here.")
            finally:
                await ctx.send(f"Nobody will be as cool as Shrek though.")
        else:
            await ctx.send(f"{ctx.author.name} please don't ask me who the cool kids are.")


    @commands.command()
    async def search_YT(self, ctx, search: Optional[str] = None):
        if search:
            _yt_search = VideosSearch(search, limit=1)
            _yt_search = _yt_search.result()
            await ctx.send(_yt_search['result'][0]['link'])
            await ctx.send("This was the first result! I cannot be bothered to get anything else..")
        else:       
            await ctx.send(f"{ctx.author.name} you need to search for a video dummy..")





def start_logging(logger, level):
    date = datetime.strftime(datetime.today(), "%d-%m-%y")
    logging_start = logging.getLogger(logger)
    match level:
        case None: logging_start.setLevel(logging_start.NOTSET)
        case 'debug': logging_start.setLevel(logging_start.DEBUG)
        case 'info': logging_start.setLevel(logging_start.INFO)
        case 'warning': logging_start.setLevel(logging_start.WARNING)
        case 'error': logging_start.setLevel(logging_start.ERROR)
        case 'critical': logging_start.setLevel(logging_start.CRITICAL)

    handler = logging.basicConfig(
                        filename=f"discord_{date}.log",
                        encoding='utf-8',
                        filemode='w'
                        )
    logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(mesasage)s'
    )
    logging_start.addHandler(handler)



drNewt.add_cog(DrNewt(drNewt))

start_logging(logger='discord', level='DEBUG')

drNewt.run(token)

        
