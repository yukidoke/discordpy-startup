from discord.ext import commands
import random

# コグとして用いるクラスを定義。
class Dice(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    #1個だけ6面ダイスを振るコマンド
    @commands.command()
    async def sr(self, ctx):
        if bot.user != ctx.author:
            a = random.randint(1,6)
            await ctx.send(f'{a}')

    #たくさんダイスを振るコマンド
    @commands.command()
    async def r(self, ctx, arg1 = 'dflt', arg2 = 'dflt'):
        if bot.user != ctx.author:
            pips = [random.randint(1, 6) for _ in range(2)]
            sum_pips = sum(pips)
            if arg1 != 'dflt' and arg2 != 'dflt':
                splited_dice = arg1.split('d')
                if len(splited_dice) == 2:
                    count = int(splited_dice[0])
                    face = int(splited_dice[1])
                    pips = [random.randint(1, face) for _ in range(count)]
                    sum_pips = sum(pips)
                    await ctx.send(f'「{arg2}」 {pips} = {sum_pips}')
                else:
                    await ctx.send('ERROR:「-r ndN comment」の形式でお願いします。')
            elif arg1 != 'dflt' and arg2 == 'dflt':
                splited_dice = arg1.split('d')
                if len(splited_dice) == 2:
                    count = int(splited_dice[0])
                    face = int(splited_dice[1])
                    pips = [random.randint(1, face) for _ in range(count)]
                    sum_pips = sum(pips)
                    await ctx.send(f'{pips} = {sum_pips}')
                else:
                    if sum_pips == 2:
                        await ctx.send(f'「{arg1}」 {pips} = {sum_pips} fumble...')
                    elif sum_pips == 12:
                        await ctx.send(f'「{arg1}」 {pips} = {sum_pips} CRITICAL!!')
                    else:
                        await ctx.send(f'「{arg1}」 {pips} = {sum_pips}')
            elif arg1 == 'dflt' and arg2 == 'dflt':
                if sum_pips == 2:
                    await ctx.send(f'{pips} = {sum_pips} fumble...')
                elif sum_pips == 12:
                    await ctx.send(f'{pips} = {sum_pips} CRITICAL!!')
                else:
                    await ctx.send(f'{pips} = {sum_pips}')
            else:
                await ctx.send('ERROR:「-r ndN comment」の形式でお願いします。')

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Dice(bot))
