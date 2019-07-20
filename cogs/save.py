from discord.ext import commands
import discord
import shelve

# コグとして用いるクラスを定義。
class Save(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def save(self, ctx):
        character_sheet = []
        client = discord.Client()
        channel = client.get_channel(601095696082534410)
        await channel.send(f'{ctx.guild.members}')

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Save(bot))
