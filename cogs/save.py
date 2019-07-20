from discord.ext import commands
import discord
import shelve

# コグとして用いるクラスを定義。
class Save(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return
        if ctx.content == 'save':
            character_sheet = []
            client = discord.Client()
            channel = client.get_channel(601095696082534410)
            guild = discord.Guild()
            member = discord.Member()
            await channel.send(f'{guild.members}')

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Save(bot))
