from discord.ext import commands
import shelve

# コグとして用いるクラスを定義。
class Register(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    #能力値の登録
    @commands.command()
    async def regi(self, ctx, name, arg):
        status = arg.split(',')
        if len(status) != 25:
            await ctx.send('ERROR:ステータス値が不足または超過しています')
        else:
            chara = shelve.open('character.db')
            chara[str(ctx.author.id)] = { 'id' : ctx.author.id, 'name' : name, 'dex' : int(status[0]), 'dex_plus' : int(status[1]), 'agi' : int(status[2]), 'agi_plus' : int(status[3]), 'str' : int(status[4]), 'str_plus' : int(status[5]), 'phy' : int(status[6]), 'phy_plus' : int(status[7]), 'int' : int(status[8]), 'int_plus' : int(status[9]), 'men' : int(status[10]), 'men_plus' : int(status[11]), 'exp' : int(status[12]), 'lv' : int(status[13]), 'tec' : int(status[14]), 'mov' : int(status[15]), 'obs' : int(status[16]), 'wis' : int(status[17]), 'hit' : int(status[18]), 'atk' : int(status[19]), 'dog' : int(status[20]), 'def' : int(status[21]), 'mag' : int(status[22]), 'hp' : int(status[23]), 'mp' : int(status[24]) }
            chara.close()
            await ctx.send(f'''以下の情報を保存しました。
            キャラクター名：{name}
            器用度：{status[0]}+{status[1]}
            敏捷度：{status[2]}+{status[3]}
            筋力：{status[4]}+{status[5]}
            生命力：{status[6]}+{status[7]}
            知力：{status[8]}+{status[9]}
            精神力：{status[10]}+{status[11]}
            経験点：{status[12]}
            冒険者レベル：{status[13]}
            技巧判定基礎値：{status[14]}
            運動判定基礎値：{status[15]}
            観察判定基礎値：{status[16]}
            知識判定基礎値：{status[17]}
            命中力：{status[18]}
            追加ダメージ：{status[19]}
            回避力：{status[20]}
            防護点：{status[21]}
            魔力：{status[22]}
            HP：{status[23]}
            MP：{status[24]}''')

    #能力値の登録解除
    @commands.command()
    async def deregi(self, ctx):
        chara = shelve.open('character.db')
        del chara[str(ctx.author.id)]
        chara.close()
        await ctx.send('登録された情報を削除しました。')

    #能力値すべての参照
    @commands.command()
    async def status(self, ctx):
        chara = shelve.open('character.db')
        dict = chara[str(ctx.author.id)]
        chara.close()
        await ctx.send(f'''キャラクター情報を参照します。
        キャラクター名：{dict['name']}
        器用度：{dict['dex']}+{dict['dex_plus']}
        敏捷度：{dict['agi']}+{dict['agi_plus']}
        筋力：{dict['str']}+{dict['str_plus']}
        生命力：{dict['phy']}+{dict['phy_plus']}
        知力：{dict['int']}+{dict['int_plus']}
        精神力：{dict['men']}+{dict['men_plus']}
        経験点：{dict['exp']}
        冒険者レベル：{dict['lv']}
        技巧判定基礎値：{dict['tec']}
        運動判定基礎値：{dict['mov']}
        観察判定基礎値：{dict['obs']}
        知識判定基礎値：{dict['wis']}
        命中力：{dict['hit']}
        追加ダメージ：{dict['atk']}
        回避力：{dict['dog']}
        防護点：{dict['def']}
        魔力：{dict['mag']}
        HP：{dict['hp']}
        MP：{dict['mp']}''')

    #能力値ひとつの参照
    @commands.command()
    async def ref(self, ctx, arg):
        chara = shelve.open('character.db')
        dict = chara[str(ctx.author.id)]
        try:
            status = dict[f'{arg}']
            chara.close()
            await ctx.send(f'{arg}：{status}')
        except:
            await ctx.send(f'ERROR:{arg}に相当するステータスが存在しません')

    #能力値変更
    @commands.command()
    async def change(self, ctx, arg, num):
        chara = shelve.open('character.db')
        dict = chara[str(ctx.author.id)]
        try:
            dict[f'{arg}'] += int(num)
            chara[str(ctx.author.id)] = dict
            chara.close()
            await ctx.send(f'{arg}の値に{num}を加えました。')
        except:
            await ctx.send(f'ERROR:{arg}に相当するステータスが存在しません')


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Register(bot)) # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
