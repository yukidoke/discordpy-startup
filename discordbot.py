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
def dice(face):
    count = random.randint(1, int(face))
    return count
def simple_dice(face, count):
    dice_val = []
    for i in range(count):
        dice_val.append(dice(face))
    msg = str(dice_val) + ' = ' + str(sum(dice_val))
    return msg

#1個だけ6面ダイスを振るコマンド
@bot.command()
async def sr(ctx):
    if bot.user != ctx.author:
        await ctx.send(f'{a}')
#たくさんダイスを振るコマンド
@bot.command()
async def r(ctx):
    print("content: ", ctx.message.content)
    if bot.user != ctx.author:
        info = parse('-r {}{}{}{}', ctx.message.content)
        print("info:", info)
        if info is None:
            count = 2
            face = 6
            await ctx.send(f'{simple_dice(face, count)}')
        elif info[0].isdecimal() and info[1] == 'd' and info[2].isdecimal():
            count = int(info[0])
            face = int(info[2])
            await ctx.send(f'「{info[3]}」 {simple_dice(face, count)}')
        else:
            count = 2
            face = 6
            await ctx.send(f'{simple_dice(face, count)}')

#ダメージ計算
#@bot.command()
#async def dmg(ctx,arg):
#    if 
#    [int(arg)][]
#    await ctx.send(f'{simple_dice(face, count)}')


bot.run(token)
