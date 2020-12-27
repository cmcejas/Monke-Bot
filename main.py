# sets up the bot
import discord
from discord.ext import commands, tasks
from discord.utils import get
from PIL import Image
from io import BytesIO
import random
from random import randint
import praw
import os
import dbl
import keep_alive

reddit = praw.Reddit(client_id="USa6HVfdOsI7ww",
                     client_secret="CG9D0387TRRbP41e7P6NrZQl5Q2ukQ",
                     username="cmcool_",
                     password="Ilikememes55",
                     user_agent="DiscordBot")

# allows intents
intents = discord.Intents.default()
discord.Intents.all = True
client = commands.Bot(command_prefix=".", intents = intents)
token = os.environ.get('DISCORD_BOT_SECRET')
client.remove_command('help') # removes default help command

# makes the bot start and changes activity say it's playing Killing Dank Memer
@client.event
async def on_ready():
    print("Bot is online")
    await client.change_presence(activity=discord.Game(name="in " + str(len(client.guilds)) + " Servers | .help", type=0))

# sends a meme when u write .meme REDDIT API YAY
@client.command()
async def meme (ctx):
    subreddit = reddit.subreddit("meme")
    all_subs = []

    hot = subreddit.hot(limit=125)
    for submission in hot:
        all_subs.append(submission)

    random_sub = random.choice(all_subs)

    name = random_sub.title
    url = random_sub.url

    em = discord.Embed(title = name)
    em.colour = random.randint(0x000000, 0XFFFFFE)
    em.set_image(url = url)
    await ctx.send(embed = em)

# -----------------------bot image editor commands-------------------------------------
# makes a person's pfp go on an image when %kill @wumpus is input
@client.command()
async def kill(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author

    kill = Image.open("kill.jpg")

    asset = user.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((109,109))

    kill.paste(pfp, (290,215))

    kill.save("kill pfp.jpg")

    await ctx.send(file = discord.File("kill pfp.jpg"))

# makes a person's pfp in front of thanos when .thanos @wumpus is input
@client.command()
async def thanos(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author

    thanos = Image.open("thanos snap.jpg")

    asset = user.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((310,310))

    thanos.paste(pfp, (612,50))

    thanos.save("thanos snap pfp.jpg")

    await ctx.send(file = discord.File("thanos snap pfp.jpg"))

# makes someones pfp on a trash can
@client.command()
async def trash(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author

    trash = Image.open("trash.png")

    asset = user.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((170,170))

    trash.paste(pfp, (215,147))

    trash.save("trash pfp.png")

    await ctx.send(file = discord.File("trash pfp.png"))
# makes a sniper crosshair on top of a persons pfp
@client.command()
async def snipe(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author

    snipe = Image.open("sniper.png")

    asset = user.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((156,156))

    snipe.paste(pfp, (340,346))

    snipe.save("sniper pfp.png")

    await ctx.send(file = discord.File("sniper pfp.png"))

# puts someone's pfp over biggiecheese's face
@client.command()
async def biggiecheese(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author

    biggiecheese = Image.open("biggiecheese.jpg")

    asset = user.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((186,115))

    biggiecheese.paste(pfp, (511,108))

    biggiecheese.save("biggiecheese pfp.jpg")

    await ctx.send(file = discord.File("biggiecheese pfp.jpg"))

# puts someone's pfp over a pile of poop
@client.command()
async def poop(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author

    poop = Image.open("poop.jpg")

    asset = user.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((111,108))

    poop.paste(pfp, (100,130))

    poop.save("poop pfp.jpg")

    await ctx.send(file = discord.File("poop pfp.jpg"))
# sends picture of drake nodding to spam
@client.command()
async def goodbot(ctx):
    open('good bot.jpg')
    await ctx.send(file = discord.File("good bot.jpg"))

#zach's easteregg image
@client.command()
async def zach_easteregg(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author

    zach_easteregg = Image.open("zach easteregg.jpg")

    asset = user.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((245,245))

    zach_easteregg.paste(pfp, (610,342))

    zach_easteregg.save("zach easteregg pfp.jpg")

    await ctx.send(file = discord.File("zach easteregg pfp.jpg"))

# kevin's easteregg image
@client.command()
async def kevin_easteregg(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author

    kevin_easteregg = Image.open("kevin_easteregg.png")

    asset = user.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((370,370))

    kevin_easteregg.paste(pfp, (555,73))

    kevin_easteregg.save("kevin pfp.jpg")

    await ctx.send(file = discord.File("kevin pfp.jpg"))

# sends a rickroll
@client.command()
async def rickroll(ctx):
    open('rick roll.gif')
    await ctx.send(file = discord.File("rick roll.gif"))
    await ctx.send("LOL GET RICK ROLLED")

# sends an uno reverse card
@client.command()
async def reverse(ctx):
    open('uno reverse card.png')
    await ctx.send(file = discord.File("uno reverse card.png"))

# ------------------------------sound effects--------------------------------------------
# sends bruh sound effect
@client.command()
async def bruh(ctx):
    open('bruh sound effect.mp3')
    await ctx.send(file = discord.File("bruh sound effect.mp3"))

# -----------------------------------TOP.GG API--------------------------------
class TopGG(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc3ODQyNDk0NTYwNzcwNDU3NiIsImJvdCI6dHJ1ZSwiaWF0IjoxNjA4NzYzODQ4fQ.MIHiKZw3YcDKwzOri9jKOI2tEVFCbzv7RlbJ8EXDY8o'
        self.dblpy = dbl.DBLClient(self.bot, self.token)
        self.update_stats.start()

    def cog_unload(self):
        self.update_stats.cancel()

    @tasks.loop(minutes=30)
    async def update_stats(self):
        await self.bot.wait_until_ready()
        try:
            server_count = len(self.bot.guilds)
            await self.dblpy.post_guild_count(server_count)
            print('Posted server count ({})'.format(server_count))
        except Exception as e:
            print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))


def setup(bot):
    bot.add_cog(TopGG(bot))
# ---------------------------------------------------INFO----------------------------------------------------------

# gives the current server ping
@client.command()
async def ping(ctx):
    await ctx.send(f'The current Spam Bot ping is: {round(client.latency * 1000)}ms!')

# gives help when u type ;help
@client.command()
async def help(ctx):
    with open("commands.txt", "r") as f:
        scores = f.read().splitlines()

    final = '\n'.join(scores[0:35])
    embed=discord.Embed(title="Commands", description=final,color = discord.Colour.orange())
    await ctx.send(embed = embed)

    with open('for mor help join script.txt', 'r') as f:
        file = [i.rstrip() for i in f.readlines()]
        for line in file:
            await ctx.send(line)

# gives info abt the bot when u type ;about
@client.command()
async def about(ctx):
    with open('about.txt', 'r') as f:
        scores = f.read().splitlines()

    final = '\n'.join(scores[0:3])
    embed=discord.Embed(title="Commands", description=final,color = discord.Colour.orange())
    await ctx.send(embed = embed)

    with open('invite link.txt', 'r') as f:
        file = [i.rstrip() for i in f.readlines()]
        for line in file:
            await ctx.send(line)

# connects bot to discord
keep_alive.keep_alive()
client.run(token)