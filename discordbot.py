from discord.ext import commands
from parse import *
import os
import traceback
import random

bot = commands.Bot(command_prefix='-')
token = os.environ['DISCORD_BOT_TOKEN']

#概要を説明するコマンド
@bot.command()
async def swds(ctx):
    await ctx.send('''Sword World droll System
    略称SWDSです。ソーズ(Swords)とお呼び下さい。
    '-r'で2d6を振ります。'-sr'で1d6を振ります。
    '-r'の後にnをダイスの数、Nを面の数として'-r ndN'として頂ければ、そのようにダイスを振ります。''')

#諸々の定義
a = random.randint(1,6)
def d(size):
    num = random.randint(1, int(size))
    return num
def sd(size, num):
    def value(size, num):
        val = []
        for i in range(num):
            val.append(d(size))
        return sum(val)
    msg = str(val) + ' = ' + str(sum(val))
    return msg

#ダイスを振るコマンド
@bot.command()
async def sr(ctx):
    if bot.user != ctx.author:
        await ctx.send(f'{a}')

@bot.command()
async def r(ctx):
    print("content: ", ctx.message.content)
    if bot.user != ctx.author:
        info = parse('-r {}{}{}{}', ctx.message.content)
        print("info:", info)
        if info is None:
            num = 2
            size = 6
            await ctx.send(f'{sd(size, num)}')
        elif info[0].isdecimal() and info[1] == 'd' and info[2].isdecimal():
            num = int(info[0])
            size = int(info[2])
            await ctx.send(f'「{info[3]}」 {sd(size, num)}')
        else:
            num = 2
            size = 6
            await ctx.send(f'{sd(size, num)}')

#ダメージ計算
#@bot.command()
#async def dmg(ctx,arg):
#    [int(arg)][]
#    await ctx.send(f'{sd(size, num)}')


bot.run(token)
