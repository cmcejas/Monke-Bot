# sets up the bot
import discord
from discord.ext import commands, tasks
from discord.utils import get
from PIL import Image
from io import BytesIO
import random
from random import randint
import asyncio
import apraw
import os
import dbl
import keep_alive
import json

os.chdir("/home/runner/Monke-Bot-Discord")

reddit = apraw.Reddit(client_id="USa6HVfdOsI7ww",
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
async def meme(ctx):
	subreddit = await reddit.subreddit("memes")
	hot = subreddit.hot
	async for submission in hot(limit=1):
		submission = await subreddit.random()
		embed = discord.Embed(title=submission.title, description=None)
		embed.colour = random.randint(0x000000, 0XFFFFFE)
		embed.url = submission.url
		embed.set_image(url=submission.url)
		embed.set_footer(
		    text=f'👍 {submission.score}  |  💬 {submission.num_comments}')
		await ctx.send(embed=embed)
#------------------------------Other Games-------------------------------------------   

# rock paper scissors
@client.command(help="Play with .rps [your choice]")
async def rps(ctx):
    rpsGame = ['rock', 'paper', 'scissors']
    await ctx.send(f"Rock, paper, or scissors? Choose wisely...")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in rpsGame

    user_choice = (await client.wait_for('message', check=check)).content

    comp_choice = random.choice(rpsGame)
    if user_choice == 'rock':
        if comp_choice == 'rock':
            await ctx.send(f'Well, {ctx.author.mention} that was weird. We tied.\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'paper':
            await ctx.send(f'LOL get destroyed {ctx.author.mention} you noob, I won that time!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'scissors':
            await ctx.send(f"WOW, {ctx.author.mention} you beat me. That was noob luck it won't happen again!\nYour choice: {user_choice}\nMy choice: {comp_choice}")

    elif user_choice == 'paper':
        if comp_choice == 'rock':
            await ctx.send(f'HAHA {ctx.author.mention}, you are so bad you lost!!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'paper':
            await ctx.send(f'Oh, what?{ctx.author.mention} we just tied. I call a rematch!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'scissors':
            await ctx.send(f"{ctx.author.mention}You only won because you are cheating smh.\nYour choice: {user_choice}\nMy choice: {comp_choice}")

    elif user_choice == 'scissors':
        if comp_choice == 'rock':
            await ctx.send(f'HAHA!! I JUST CRUSHED YOU, {ctx.author.mention}!! I rock!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'paper':
            await ctx.send(f'Bruh {ctx.author.mention}. How did you win???\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'scissors':
            await ctx.send(f"Oh well {ctx.author.mention}, we tied.\nYour choice: {user_choice}\nMy choice: {comp_choice}")
#-----------------------------Economy System-----------------------------------------

# balance command
@client.command(aliases = ["bal"])
async def balance(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author


    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title = f"{user}'s balance")
    em.add_field(name = "Wallet balance",value = wallet_amt)
    em.add_field(name = "Bank balance",value = bank_amt)
    em.colour = (0xFFFF00)
    await ctx.send(embed = em)

# beg command
@client.command()
@commands.cooldown(rate=1, per=3.0, type=commands.BucketType.member)
async def beg(ctx):

  await open_account(ctx.author)

  users = await get_bank_data()

  user = ctx.author

  earnings = random.randint(5, 50)

  await ctx.send(f"Monke gave {ctx.author.mention} {earnings} coins!")

  users[str(user.id)]["wallet"] += earnings

  with open("mainbank.json","w") as f:
    json.dump(users,f)

# lottery
@client.command(aliases = ["lot"])
@commands.cooldown(rate=1, per=18000.0, type=commands.BucketType.member)
async def LotteryTicket(ctx):
  await open_account(ctx.author)

  users = await get_bank_data()

  user = ctx.author

  if users[str(user.id)]["wallet"] < (300):
    await ctx.send('You do not have enough cash. Tickets costs 300 coins.')
    return
  else:
    await update_bank(ctx.author,-300)

  lotteryNumb= random.randint(0, 1000)

  if lotteryNumb == (1):
    users[str(user.id)]["bank"] + (10000)
    await ctx.send('CONGRATULATIONS! You just won the lottery! Here is 10,000 coins!')
  else:
    await ctx.send('Ah man, looks like you lost. You can try again in 5 hours.')

# withdraw command
@client.command(aliases = ["with"])
@commands.cooldown(rate=1, per=.0, type=commands.BucketType.member)
async def withdraw(ctx,amount = None):
  await open_account(ctx.author)
  
  if amount == None:
    await ctx.send("Bruh use the command correctly")
    return

  bal = await update_bank(ctx.author)
  if amount == "all":
    amount = bal[1]

  amount = int(amount)
  if amount>bal[1]:
    await ctx.send("You do not have that much money noob")
    return
  if amount<0:
    await ctx.send("Are you dumb? You cannot withdraw a negative amount of money")
    return

  await update_bank(ctx.author,amount)
  await update_bank(ctx.author,-1*amount,"bank")

  await ctx.send(f"You withdrew {amount} coins!")

# deposit command
@client.command(aliases = ["dep"])
async def deposit(ctx,amount = None):
  await open_account(ctx.author)
  
  if amount == None:
    await ctx.send("Bruh use the command correctly")
    return

  bal = await update_bank(ctx.author)
  if amount == "all":
    amount = bal[0]

  amount = int(amount)
  if amount>bal[0]:
    await ctx.send("You do not have that much money noob")
    return
  if amount<0:
    await ctx.send("Are you dumb? You cannot deposit a negative amount of money")
    return

  await update_bank(ctx.author,-1*amount)
  await update_bank(ctx.author,amount,"bank")

  await ctx.send(f"You deposited {amount} coins!")

# gift money with the gift command
@client.command()
async def gift(ctx,member:discord.Member,amount = None):
  await open_account(ctx.author)
  await open_account(member)

  if amount == None:
    await ctx.send("Bruh use the command correctly")
    return

  bal = await update_bank(ctx.author)
  if amount == "all":
    amount = bal[1]

  amount = int(amount)
  if amount>bal[1]:
    await ctx.send("You do not have that much money noob")
    return
  if amount<0:
    await ctx.send("Are you dumb? You cannot gift a negative amount of money")
    return

  await update_bank(ctx.author,-1*amount,"bank")
  await update_bank(member,amount,"bank")

  await ctx.send(f"{ctx.author.mention} gave {amount} coins to {member.mention}!")

# rob command
@client.command()
@commands.cooldown(rate=1, per=1800.0, type=commands.BucketType.member)
async def rob(ctx,member:discord.Member):
  await open_account(ctx.author)
  await open_account(member)

  bal = await update_bank(member)

  if bal[0]<100:
    await ctx.send("It's not worth robbing them they have less than 100 coins in there wallet. smh")
    return

  stolen_money = random.randrange(0, bal[0])

  await update_bank(ctx.author,stolen_money)
  await update_bank(member,-1*stolen_money)

  await ctx.send(f"{ctx.author.mention} robbed {member.mention} for {stolen_money} coins!")

#slots command
@client.command()
async def slots(ctx,amount = None):
  await open_account(ctx.author)
  
  if amount == None:
    await ctx.send("Bruh use the command correctly")
    return

  bal = await update_bank(ctx.author)

  amount = int(amount)
  if amount>bal[0]:
    await ctx.send("You do not have that much money noob")
    return
  if amount<0:
    await ctx.send("Are you dumb? You cannot deposit a negative amount of money")
    return

  final = []
  for i in range(3):
    a = random.choice(["`♠`","`♣`","`♦`"])

    final.append(a)
  await ctx.send(str(final))

  if final[0] == final[1] or final[0] == final[1] or final[0] == final[1]:
    await update_bank(ctx.author,2*amount)
    await ctx.send("Congrats you won!")
  else:
    await update_bank(ctx.author,-1*amount)
    await ctx.send("LOL what a noob you lost!")

# sets up the shop
mainshop = [{"name":"School_Chromebook","price":1,"description":"A.K.A. Garbage"},
            {"name":"cmcool's_PC","price":10000,"description":"1 million FPS"},
            {"name":"Almighty_Banana","price":9999999999,"description":"Monke Bot's banana"}]


@client.command()
async def shop(ctx):
    em = discord.Embed(title = "Monke Bot's Store")

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.colour = (0xFFFF00)
        em.add_field(name = name, value = f"${price} | {desc}", inline = False)

    await ctx.send(embed = em)
    await ctx.send('You can buy lottery tickets for 300 coins with the command .LotteryTicket')


@client.command()
async def buy(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
            return


    await ctx.send(f"You just bought {amount} {item}")


@client.command(aliases = ["inv"])
async def inventory(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    em = discord.Embed(title = "Inventory")
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = name, value = amount, inline = False)    
        em.colour = (0xFFFF00)

    await ctx.send(embed = em)

# buy items from the shop
async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"wallet")

    return [True,"Worked"]

# sell items
@client.command()
async def sell(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have {amount} {item} in your inventory.")
            return
        if res[1]==3:
            await ctx.send(f"You don't have {item} in your inventory.")
            return

    await ctx.send(f"You just sold {amount} {item}.")

async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.9* item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]    

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]

# economy leaderboard
@client.command(aliases = ["lb"])
async def leaderboard(ctx,x = 1):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total,reverse=True)    

    em = discord.Embed(title = f"Top {x} Richest People" , description = "This is decided on the basis of raw money in the bank and wallet",color = discord.Color(0xFFFF00))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        name = member.name
        em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed = em)

# hyper functions for opening an account
async def open_account(user):
   
  users = await get_bank_data()

  if str(user.id) in users:
    return False
  else:
    users[str(user.id)] = {}
    users[str(user.id)]["wallet"] = 0
    users[str(user.id)]["bank"] = 0

  with open("mainbank.json","w") as f:
    json.dump(users,f)
  return True

async def get_bank_data():
  with open("mainbank.json","r") as f:
    users = json.load(f)

  return users

async def update_bank(user,change = 0,mode = "wallet"):
  users = await get_bank_data()

  users[str(user.id)][mode] += change

  with open("mainbank.json","w") as f:
    json.dump(users,f)
  
    bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
    return bal

# -----------------------bot image editor commands-------------------------------------

# makes a person's pfp go on an image when .kill @wumpus is input
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

# sends moving pog head
@client.command()
async def pog(ctx):
    open('pog.gif')
    await ctx.send(file = discord.File("pog.gif"))

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

@client.command()
async def oof(ctx):
  open('oof.mp3')
  await ctx.send(file = discord.File("oof.mp3"))

# -----------------------------------TOP.GG API--------------------------------
client.load_extension('cogs.TopGG')
# --------------------------------------INFO----------------------------------

# gives the current server ping
@client.command()
async def ping(ctx):
    await ctx.send(f'The current Monke Bot ping is: {round(client.latency * 1000)}ms!')

# gives help when u type .help
@client.command()
async def help(ctx):
    with open("commands.txt", "r") as f:
        scores = f.read().splitlines()

    final = '\n'.join(scores[0:49])
    embed=discord.Embed(title="Commands", description=final)
    embed.colour = (0x964b00)
    await ctx.send(embed = embed)

    with open('for mor help join script.txt', 'r') as f:
        file = [i.rstrip() for i in f.readlines()]
        for line in file:
            await ctx.send(line)

# gives info abt the bot when u type .about
@client.command()
async def about(ctx):
    with open('about.txt', 'r') as f:
        scores = f.read().splitlines()

    final = '\n'.join(scores[0:3])
    embed=discord.Embed(title="Commands", description=final,)
    embed.colour = (0x964b00)
    await ctx.send(embed = embed)

    with open('invite link', 'r') as f:
        file = [i.rstrip() for i in f.readlines()]
        for line in file:
            await ctx.send(line)

#sends the bot invite link when .invite is input
@client.command()
async def invite(ctx):
  await ctx.send('Here is the bot invite link: https://discord.com/api/oauth2/authorize?client_id=778424945607704576&permissions=8&scope=bot')

#sends the help server invite when .srvinvite is input
@client.command()
async def srvinvite(ctx):
  await ctx.send('discord.gg/7rMg2txgyy')

# sends the bot's top.gg page when .upvote is input
@client.command()
async def upvote(ctx):
  await ctx.send('You can upvote the bot here: https://top.gg/bot/778424945607704576/vote')

# sends the bot's website link
@client.command()
async def website(ctx):
  await ctx.send('https://sites.google.com/view/monke-bot')

# error handeling
@client.event
async def on_command_error(ctx,error):
  if isinstance(error,commands.CommandOnCooldown):
    with open("cooldown", "r") as f:
        scores = f.read().splitlines()

    final = '\n'.join(scores[0:1])
    embed=discord.Embed(title="WAIT!  ⏰", description=final)
    embed.colour = (0xFF0000)
    await ctx.send(embed = embed)

# connects bot to discord
keep_alive.keep_alive()
client.run(token)
