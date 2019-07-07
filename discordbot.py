from discord.ext import commands
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
    -rで2d6が振れます。''')

#2d6を振るコマンド
@bot.command()
async def r(ctx):
    a = random.randint(1,6)
    b = random.randint(1,6)
    c = a + b
    if c == 2:
        await ctx.send(f'{a} + {b} = {c} fumble...')
    elif c == 12:
        await ctx.send(f'{a} + {b} = {c} CRITICAL!!')
    else:
        await ctx.send(f'{a} + {b} = {c}')
        


bot.run(token)
