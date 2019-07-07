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
    -rで2d6が振れます。-srで1d6が振れます。''')

a = random.randint(1,6)
b = random.randint(1,6)
c = a + b

#ダイスを振るコマンド
@bot.command()
async def sr(ctx):
    await ctx.send(f'{a}')
@bot.command()
async def r(ctx):
    if c == 2:
        await ctx.send(f'{a} + {b} = {c} fumble...')
    elif c == 12:
        await ctx.send(f'{a} + {b} = {c} CRITICAL!!')
    else:
        await ctx.send(f'{a} + {b} = {c}')

#slapper
class Slapper(commands.Converter):
    async def convert(self, ctx, argument):
        to_slap = random.choice(ctx.guild.members)
        return '{0.author} slapped {1} because *{2}*'.format(ctx, to_slap, argument)

@bot.command()
async def slap(ctx, *, reason: Slapper):
    await ctx.send(reason)


bot.run(token)
