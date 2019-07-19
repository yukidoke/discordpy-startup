from discord.ext import commands
import shelve

# コグとして用いるクラスを定義。
class Rewards(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    #経験点参照コマンド
    @bot.command()
    async def exp(ctx, arg):
        if arg.isdecimal():
            level = int(arg)
            exp_table = ['0','A:1000 B:500','A:1000 B:1000','A:1500 B:1000','A:1500 B:1500','A:2000 B:1500','A:2500 B:2000','A:3000 B:2500','A:4000 B:3000','A:5000 B:4000','A:6000 B:5000','A:7500 B:6000','A:9000 B:7500','A:10500 B:9000','A:12000 B:10500','A:13500 B:12000']
            await ctx.send(f'技能Lv{level}への上昇に必要な経験点は {exp_table[level]} です。')
        else:
            await ctx.send('ERROR:対象となるLvが適切に入力されていません')

    #成長
    @bot.command()
    async def grow(ctx, arg):
        chara = shelve.open('character.db')
        dict = chara[str(ctx.author.id)]
        try:
            dict[f'{arg}_plus'] += 1
            chara[str(ctx.author.id)] = dict
            sum = dict[f'{arg}_plus']
            new_status = dict[f'{arg}'] + dict[f'{arg}_plus']
            chara.close()
            await ctx.send(f'成長：{arg} +1 累計成長：{sum} 累計{arg}：{new_status}')
        except:
            await ctx.send(f'{arg}は能力値に設定されていません。dex,agi,str,phy,int,menが対応しています。')

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Rewards(bot))
