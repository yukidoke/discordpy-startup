from discord.ext import commands
import os
import traceback
import random

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(str(error))


@bot.command()
async def r(ctx):
    a = random.randint(1,6)
    b = random.randint(1,6)
    c = a + b
    await ctx.send(f'{a} + {b} = {c}')


bot.run(token)
