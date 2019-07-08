from discord.ext import commands
from parse import *
import os
import traceback
import random

bot = commands.Bot(command_prefix='-')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(str(error))

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
    if bot.user != ctx.author:
        info = parse('-r {}d{}', ctx.message.content)
    if info[1].isdecimal() and info[0].isdecimal():
        dice_num = int(info[0])
        dice_size = int(info[1])
        await ctx.send(f'{msg}')
    else:
        if c == 2:
            await ctx.send(f'{a} + {b} = {c} fumble...')
        elif c == 12:
            await ctx.send(f'{a} + {b} = {c} CRITICAL!!')
        else:
            await ctx.send(f'{a} + {b} = {c}')


bot.run(token)
