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
    await ctx.send('''Sword World Diceroll System
    略称SWDSです。ソーズ(Swords)とお呼び下さい。
    -rで2d6が振れます。-srで1d6が振れます。''')

a = random.randint(1,6)
b = random.randint(1,6)
c = a + b

def dice(dice_size):
    num = random.randint(1, int(dice_size))
    return num
def simple_dice(dice_size, dice_num):
    dice_val = []
    for i in range(dice_num):
        dice_val.append(dice(dice_size))
    msg = str(dice_val) + ' = ' + str(sum(dice_val))
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
        info = parse('-r {}{}{}', ctx.message.content)
        print("info:", info)
        if info is None:
            dice_num = 2
            dice_size = 6
            await ctx.send(f'{simple_dice(dice_size, dice_num)}')
    elif info[0].isdecimal() and info[1] == 'd' and info[2].isdecimal():
        dice_num = int(info[0])
        dice_size = int(info[2])
        await ctx.send(f'{simple_dice(dice_size, dice_num)}')
    else:
        dice_num = 2
        dice_size = 6
        await ctx.send(f'{simple_dice(dice_size, dice_num)}')

bot.run(token)
