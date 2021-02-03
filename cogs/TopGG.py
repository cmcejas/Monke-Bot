from discord.ext import commands, tasks
import dbl

class TopGG(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc3ODQyNDk0NTYwNzcwNDU3NiIsImJvdCI6dHJ1ZSwiaWF0IjoxNjA4NzYzODQ4fQ.MIHiKZw3YcDKwzOri9jKOI2tEVFCbzv7RlbJ8EXDY8o'  # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True)

    @commands.Cog.listener()
    async def on_guild_post(self):
        print("Server count posted successfully")

def setup(bot):
    bot.add_cog(TopGG(bot))