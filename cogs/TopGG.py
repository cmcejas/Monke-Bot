from discord.ext import commands, tasks
import dbl

class TopGG(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.token = 'dbl_token'  # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True)

    @commands.Cog.listener()
    async def on_guild_post(self):
        print("Server count posted successfully")

def setup(bot):
    bot.add_cog(TopGG(bot))