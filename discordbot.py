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
    '-r'で2d6を振ります。'-sr'で1d6を振ります。
    nをダイスの数、Nを面の数として、'-r ndN'で指定された通りにダイスを振ります。
    nを0から80までの整数として、'-dmg n'で威力表nのダメージを算出します。
    よく使われるであろうアイテムや魔法は別のコマンドで代替できます。
    '-q'で＜救命草＞を使用します。'-m'で＜魔香草＞・＜魔香水＞を使用します。
    '-h'で＜ヒーリングポーション＞を使用します。
    '-cw'で【キュア・ウーンズ】を行使します。''')

#諸々の定義
damage_table = [[-7,0,-1,0,0,0,1,2,2,3,3,4,4],[-7,1,-1,0,0,0,1,2,3,3,3,4,4],[-7,2,-1,0,0,0,1,2,3,4,4,4,4],[-7,3,-1,0,0,1,1,2,3,4,4,4,5],[-7,4,-1,0,0,1,2,2,3,4,4,5,5],[-7,5,-1,0,1,1,2,2,3,4,5,5,5],[-7,6,-1,0,1,1,2,3,3,4,5,5,5],[-7,7,-1,0,1,1,2,3,4,4,5,5,6],[-7,8,-1,0,1,2,2,3,4,4,5,6,6],[-7,9,-1,0,1,2,3,3,4,4,5,6,7],[-7,10,-1,1,1,2,3,3,4,5,5,6,7],[-7,11,-1,1,2,2,3,3,4,5,6,6,7],[-7,12,-1,1,2,2,3,4,4,5,6,6,7],[-7,13,-1,1,2,3,3,4,4,5,6,7,7],[-7,14,-1,1,2,3,4,4,4,5,6,7,8],[-7,15,-1,1,2,3,4,4,5,5,6,7,8],[-7,16,-1,1,2,3,4,4,5,6,7,7,8],[-7,17,-1,1,2,3,4,5,5,6,7,7,8],[-7,18,-1,1,2,3,4,5,6,6,7,7,8],[-7,19,-1,1,2,3,4,5,6,7,7,8,9],[-7,20,-1,1,2,3,4,5,6,7,8,9,10],[-7,21,-1,1,2,3,4,6,6,7,8,9,10],[-7,22,-1,1,2,3,5,6,6,7,8,9,10],[-7,23,-1,2,2,3,5,6,7,7,8,9,10],[-7,24,-1,2,3,4,5,6,7,7,8,9,10],[-7,25,-1,2,3,4,5,6,7,8,8,9,10],[-7,26,-1,2,3,4,5,6,8,8,9,9,10],[-7,27,-1,2,3,4,6,6,8,8,9,9,10],[-7,28,-1,2,3,4,6,6,8,9,9,10,10],[-7,29,-1,2,3,4,6,7,8,9,9,10,10],[-7,30,-1,2,4,4,6,7,8,9,10,10,10],[-7,31,-1,2,4,5,6,7,8,9,10,10,11],[-7,32,-1,3,4,5,6,7,8,10,10,10,11],[-7,33,-1,3,4,5,6,8,8,10,10,10,11],[-7,34,-1,3,4,5,6,8,9,10,10,11,11],[-7,35,-1,3,4,5,7,8,9,10,10,11,12],[-7,36,-1,3,5,5,7,8,9,10,11,11,12],[-7,37,-1,3,5,6,7,8,9,10,11,12,12],[-7,38,-1,3,5,6,7,8,10,10,11,12,13],[-7,39,-1,4,5,6,7,8,10,11,11,12,13],[-7,40,-1,4,5,6,7,9,10,11,11,12,13],[-7,41,-1,4,6,6,7,9,10,11,12,12,13],[-7,42,-1,4,6,7,7,9,10,11,12,13,13],[-7,43,-1,4,6,7,8,9,10,11,12,13,14],[-7,44,-1,4,6,7,8,10,10,11,12,13,14],[-7,45,-1,4,6,7,9,10,10,11,12,13,14],[-7,46,-1,4,6,7,9,10,10,12,13,13,14],[-7,47,-1,4,6,7,9,10,11,12,13,13,15],[-7,48,-1,4,6,7,9,10,12,12,13,13,15],[-7,49,-1,4,6,7,10,10,12,12,13,14,15],[-7,50,-1,4,6,8,10,10,12,12,13,15,15],[-7,51,-1,5,7,8,10,10,12,12,13,15,15],[-7,52,-1,5,7,8,10,11,12,12,13,15,15],[-7,53,-1,5,7,9,10,11,12,12,14,15,15],[-7,54,-1,5,7,9,10,11,12,13,14,15,16],[-7,55,-1,5,7,10,10,11,12,13,14,16,16],[-7,56,-1,5,8,10,11,12,12,13,15,16,17],[-7,57,-1,5,8,10,11,11,12,13,15,16,17],[-7,58,-1,5,8,10,11,12,12,13,15,16,17],[-7,59,-1,5,9,10,11,12,12,14,15,16,17],[-7,60,-1,5,9,10,11,12,13,14,15,16,18],[-7,61,-1,5,9,10,11,12,13,14,16,17,18],[-7,62,-1,5,9,10,11,13,13,14,16,17,18],[-7,63,-1,5,9,10,11,13,13,15,17,17,18],[-7,64,-1,5,9,10,11,13,14,15,17,17,18],[-7,65,-1,5,9,10,12,13,14,15,17,18,18],[-7,66,-1,5,9,10,12,13,15,15,17,18,19],[-7,67,-1,5,9,10,12,13,15,16,17,18,19],[-7,68,-1,5,9,10,12,14,15,16,17,19,19],[-7,69,-1,5,9,10,12,14,16,17,18,19,19],[-7,70,-1,5,9,10,13,14,16,17,18,19,20],[-7,71,-1,5,9,10,13,15,16,17,18,19,20],[-7,72,-1,5,9,10,13,15,16,17,18,19,20],[-7,73,-1,5,9,10,13,15,16,17,19,20,21],[-7,74,-1,6,9,10,13,15,16,18,19,20,21],[-7,75,-1,6,9,10,13,16,16,18,19,20,21],[-7,76,-1,6,9,10,13,16,17,18,19,20,21],[-7,77,-1,6,9,10,13,16,17,18,20,21,22],[-7,78,-1,6,9,10,13,16,17,19,20,22,23],[-7,79,-1,6,9,10,13,16,18,19,20,22,23],[-7,80,-1,6,9,10,13,16,18,20,21,22,23]]
a = random.randint(1,6)

#1個だけ6面ダイスを振るコマンド
@bot.command()
async def sr(ctx):
    if bot.user != ctx.author:
        await ctx.send(f'{a}')
#たくさんダイスを振るコマンド
@bot.command()
async def r(ctx, dice: str, serif: str):
    print('dice: ', dice)
    print('serif: ', serif)
    if bot.user != ctx.author:
        if dice is None and serif is None:
            pips = [random.randint(1, 6) for _ in range(2)]
            sum_pips = sum(pips)
            await ctx.send(f'{pips} = {sum_pips}')
        elif serif is None:
            pips = [random.randint(1,6) for _ in range(2)]
            sum_pips = sum(pips)
            await ctx.send(f'「{dice}」 {pips} = {sum_pips}')
        else:
            splited_dice = dice.split('d')
            count = int(splited_dice[0])
            face = int(splited_dice[1])
            pips = [random.randint(1, face) for _ in range(count)]
            sum_pips = sum(pips)
            await ctx.send(f'「{serif}」 {pips} = {sum_pips}')

#ダメージ計算
@bot.command()
async def dmg(ctx,arg):
    if arg.isdecimal():
        pips = [random.randint(1, 6) for _ in range(2)]
        sum_pips = sum(pips)
        if sum_pips == 2:
            await ctx.send(f'{pips} = {sum_pips} fumble...')
        else:
            damage = damage_table[int(arg)][sum_pips]
            await ctx.send(f'{pips} = {sum_pips} 「{damage}」点のダメージ')

@bot.command()
async def q(ctx):
    pips = [random.randint(1, 6) for _ in range(2)]
    sum_pips = sum(pips)
    if sum_pips == 2:
        await ctx.send(f'HPを威力10で回復：{pips} = {sum_pips} fumble...')
    else:
        damage = damage_table[10][sum_pips]
        await ctx.send(f'HPを威力10で回復：{pips} = {sum_pips} 基礎回復量：「{damage}」点')

@bot.command()
async def h(ctx):
    pips = [random.randint(1, 6) for _ in range(2)]
    sum_pips = sum(pips)
    if sum_pips == 2:
        await ctx.send(f'HPを威力20で回復：{pips} = {sum_pips} fumble...')
    else:
        damage = damage_table[20][sum_pips]
        await ctx.send(f'HPを威力20で回復：{pips} = {sum_pips} 基礎回復量：「{damage}」点')

@bot.command()
async def m(ctx):
    pips = [random.randint(1, 6) for _ in range(2)]
    sum_pips = sum(pips)
    if sum_pips == 2:
        await ctx.send(f'MPを威力0で回復：{pips} = {sum_pips} fumble...')
    else:
        damage = damage_table[0][sum_pips]
        await ctx.send(f'MPを威力0で回復：{pips} = {sum_pips} 基礎回復量：「{damage}」点')

@bot.command()
async def cw(ctx):
    pips = [random.randint(1, 6) for _ in range(2)]
    sum_pips = sum(pips)
    if sum_pips == 2:
        await ctx.send(f'【キュア・ウーンズ】を行使：{pips} = {sum_pips} fumble...')
    else:
        damage = damage_table[20][sum_pips]
        await ctx.send(f'【キュア・ウーンズ】を行使：{pips} = {sum_pips} 行使成功')
        pips2 = [random.randint(1, 6) for _2 in range(2)]
        sum_pips2 = sum(pips2)
        if sum_pips == 2:
            await ctx.send(f'HPを威力10で回復：{pips2} = {sum_pips2} fumble...')
        else:
            damage = damage_table[10][sum_pips2]
            await ctx.send(f'HPを威力10で回復：{pips2} = {sum_pips2} 基礎回復量：「{damage}」点')


bot.run(token)
