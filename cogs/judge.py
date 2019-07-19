from discord.ext import commands
import random
import shelve

# コグとして用いるクラスを定義。
class Judge(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    #生命抵抗力判定
    @commands.command()
    async def pr(self, ctx, arg):
        chara = shelve.open('character.db')
        dict = chara[str(ctx.author.id)]
        chara.close()
        bonus = (dict['phy']+dict['phy_plus']) // 6
        phy = dict['lv'] + bonus
        pips = [random.randint(1, 6) for _ in range(2)]
        sum_pips = sum(pips)
        reached = phy + sum_pips
        if sum_pips == 2:
            await ctx.send(f'生命抵抗力判定：{pips} = {sum_pips} fumble...')
        elif sum_pips == 12:
            await ctx.send(f'生命抵抗力判定：{pips} = {sum_pips} CRITICAL!!')
        else:
            if int(arg) <= reached:
                await ctx.send(f'生命抵抗力判定：{pips} = {sum_pips} + {phy} ≧ {arg} 成功')
            else:
                await ctx.send(f'生命抵抗力判定：{pips} = {sum_pips} + {phy} ＜ {arg} 失敗')

    #精神抵抗力判定
    @commands.command()
    async def mr(self, ctx, arg):
        chara = shelve.open('character.db')
        dict = chara[str(ctx.author.id)]
        chara.close()
        bonus = (dict['men']+dict['men_plus']) // 6
        men = dict['lv'] + bonus
        pips = [random.randint(1, 6) for _ in range(2)]
        sum_pips = sum(pips)
        reached = men + sum_pips
        if sum_pips == 2:
            await ctx.send(f'精神抵抗力判定：{pips} = {sum_pips} fumble...')
        elif sum_pips == 12:
            await ctx.send(f'精神抵抗力判定：{pips} = {sum_pips} CRITICAL!!')
        else:
            if int(arg) <= reached:
                await ctx.send(f'精神抵抗力判定：{pips} = {sum_pips} + {men} ≧ {arg} 成功')
            else:
                await ctx.send(f'精神抵抗力判定：{pips} = {sum_pips} + {men} ＜ {arg} 失敗')

    #パッケージ判定
    @commands.command()
    async def tec(self, ctx, arg):
        chara = shelve.open('character.db')
        dict = chara[str(ctx.author.id)]
        chara.close()
        tec = dict['tec']
        pips = [random.randint(1, 6) for _ in range(2)]
        sum_pips = sum(pips)
        reached = tec + sum_pips
        if sum_pips == 2:
            await ctx.send(f'技巧判定：{pips} = {sum_pips} fumble...')
        elif sum_pips == 12:
            await ctx.send(f'技巧判定：{pips} = {sum_pips} CRITICAL!!')
        else:
            if int(arg) <= reached:
                await ctx.send(f'技巧判定：{pips} = {sum_pips} + {tec} ≧ {arg} 成功')
            else:
                await ctx.send(f'技巧判定：{pips} = {sum_pips} + {tec} ＜ {arg} 失敗')

    @commands.command()
    async def mov(self, ctx, arg):
        chara = shelve.open('character.db')
        dict = chara[str(ctx.author.id)]
        chara.close()
        mov = dict['mov']
        pips = [random.randint(1, 6) for _ in range(2)]
        sum_pips = sum(pips)
        reached = mov + sum_pips
        if sum_pips == 2:
            await ctx.send(f'運動判定：{pips} = {sum_pips} fumble...')
        elif sum_pips == 12:
            await ctx.send(f'運動判定：{pips} = {sum_pips} CRITICAL!!')
        else:
            if int(arg) <= reached:
                await ctx.send(f'運動判定：{pips} = {sum_pips} + {mov} ≧ {arg} 成功')
            else:
                await ctx.send(f'運動判定：{pips} = {sum_pips} + {mov} ＜ {arg} 失敗')

    @commands.command()
    async def obs(self, ctx, arg):
        chara = shelve.open('character.db')
        dict = chara[str(ctx.author.id)]
        chara.close()
        obs = dict['obs']
        pips = [random.randint(1, 6) for _ in range(2)]
        sum_pips = sum(pips)
        reached = obs + sum_pips
        if sum_pips == 2:
            await ctx.send(f'観察判定：{pips} = {sum_pips} fumble...')
        elif sum_pips == 12:
            await ctx.send(f'観察判定：{pips} = {sum_pips} CRITICAL!!')
        else:
            if int(arg) <= reached:
                await ctx.send(f'観察判定：{pips} = {sum_pips} + {obs} ≧ {arg} 成功')
            else:
                await ctx.send(f'観察判定：{pips} = {sum_pips} + {obs} ＜ {arg} 失敗')

    @commands.command()
    async def wis(self, ctx, arg):
        chara = shelve.open('character.db')
        dict = chara[str(ctx.author.id)]
        chara.close()
        wis = dict['wis']
        pips = [random.randint(1, 6) for _ in range(2)]
        sum_pips = sum(pips)
        reached = wis + sum_pips
        if sum_pips == 2:
            await ctx.send(f'知識判定：{pips} = {sum_pips} fumble...')
        elif sum_pips == 12:
            await ctx.send(f'知識判定：{pips} = {sum_pips} CRITICAL!!')
        else:
            if int(arg) <= reached:
                await ctx.send(f'知識判定：{pips} = {sum_pips} + {wis} ≧ {arg} 成功')
            else:
                await ctx.send(f'知識判定：{pips} = {sum_pips} + {wis} ＜ {arg} 失敗')

    #命中と回避
    @commands.command()
    async def hit(self, ctx, arg):
        chara = shelve.open('character.db')
        dict = chara[str(ctx.author.id)]
        chara.close()
        hit = dict['hit']
        pips = [random.randint(1, 6) for _ in range(2)]
        sum_pips = sum(pips)
        reached = hit + sum_pips
        if sum_pips == 2:
            await ctx.send(f'命中力判定：{pips} = {sum_pips} fumble...')
        elif sum_pips == 12:
            await ctx.send(f'命中力判定：{pips} = {sum_pips} CRITICAL!!')
        else:
            if int(arg) < reached:
                await ctx.send(f'命中力判定：{pips} = {sum_pips} + {hit} ＞ {arg} 成功')
            else:
                await ctx.send(f'命中力判定：{pips} = {sum_pips} + {hit} ≦ {arg} 失敗')

    @commands.command()
    async def dog(self, ctx, arg):
        chara = shelve.open('character.db')
        dict = chara[str(ctx.author.id)]
        chara.close()
        dog = dict['dog']
        pips = [random.randint(1, 6) for _ in range(2)]
        sum_pips = sum(pips)
        reached = dog + sum_pips
        if sum_pips == 2:
            await ctx.send(f'回避力判定：{pips} = {sum_pips} fumble...')
        elif sum_pips == 12:
            await ctx.send(f'回避力判定：{pips} = {sum_pips} CRITICAL!!')
        else:
            if int(arg) <= reached:
                await ctx.send(f'回避力判定：{pips} = {sum_pips} + {dog} ≧ {arg} 成功')
            else:
                await ctx.send(f'回避力判定：{pips} = {sum_pips} + {dog} ＜ {arg} 失敗')

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Judge(bot))
