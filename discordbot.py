from discord.ext import commands
import os
import traceback
import random
import shelve

bot = commands.Bot(command_prefix='-')
token = os.environ['DISCORD_BOT_TOKEN']

#既に使われているコマンド：r, sr, dmg, exp, q, m, h, t, cw

#概要を説明するコマンド
@bot.command()
async def swds(ctx):
    await ctx.send('''Sword World Diceroll System
    略称SWDSです。ソーズ(Swords)とお呼び下さい。
    `-r`で2d6を振ります。`-sr`で1d6を振ります。
    ダイスロールに関する詳細は`-dice`
    その他のコマンドに関する詳細は`-cmds`で参照できます。''')

@bot.command()
async def dice(ctx):
    await ctx.send('''【ダイスロール関係について】
    `-r`で2d6を振ります。`-sr`で1d6を振ります。
    nをダイスの数、Nを面の数として、`-r ndN`で指定された通りにダイスを振ります。
    nを0から100までの整数として、`-dmg n`で威力表nのダメージを算出します。
    出目の補正値Nがある場合は、`-dmg n N`でそれを反映します。
    上記のコマンドには末尾にセリフを入れることも出来ます。
    例：`-r 5d6 名誉点決定`
    行使判定を命中力判定などと区別しておきたい場合は`-mp`が有効です。
    ダメージを伴う魔法の場合は、威力をnとして、`-mp n`でダメージまで同時に算出します。''')

@bot.command()
async def cmds(ctx):
    await ctx.send('''技能Lvを1上げてnにするために必要な経験点は`-exp n`で参照できます。
    また、よく使われるであろうアイテムや魔法は別のコマンドで代替できます。
    `-q`で＜救命草＞を使用します。`-m`で＜魔香草＞・＜魔香水＞を使用します。
    `-h`で＜ヒーリングポーション＞を使用します。
    `-t`で＜トリートポーション＞を使用します。
    `-cw`で【キュア・ウーンズ】を行使します。''')

#諸々の定義
#0~11は指輪腕輪込の能力値とその成長、12は経験点、13は冒険者Lv、14~17は各種判定パッケージ、18,19は命中力と追加ダメージ、20,21は回避力と防護点、22は魔力、23,24はHPとMP
damage_table = [[-7,0,-1,0,0,0,1,2,2,3,3,4,4],[-7,1,-1,0,0,0,1,2,3,3,3,4,4],[-7,2,-1,0,0,0,1,2,3,4,4,4,4],[-7,3,-1,0,0,1,1,2,3,4,4,4,5],[-7,4,-1,0,0,1,2,2,3,4,4,5,5],[-7,5,-1,0,1,1,2,2,3,4,5,5,5],[-7,6,-1,0,1,1,2,3,3,4,5,5,5],[-7,7,-1,0,1,1,2,3,4,4,5,5,6],[-7,8,-1,0,1,2,2,3,4,4,5,6,6],[-7,9,-1,0,1,2,3,3,4,4,5,6,7],[-7,10,-1,1,1,2,3,3,4,5,5,6,7],[-7,11,-1,1,2,2,3,3,4,5,6,6,7],[-7,12,-1,1,2,2,3,4,4,5,6,6,7],[-7,13,-1,1,2,3,3,4,4,5,6,7,7],[-7,14,-1,1,2,3,4,4,4,5,6,7,8],[-7,15,-1,1,2,3,4,4,5,5,6,7,8],[-7,16,-1,1,2,3,4,4,5,6,7,7,8],[-7,17,-1,1,2,3,4,5,5,6,7,7,8],[-7,18,-1,1,2,3,4,5,6,6,7,7,8],[-7,19,-1,1,2,3,4,5,6,7,7,8,9],[-7,20,-1,1,2,3,4,5,6,7,8,9,10],[-7,21,-1,1,2,3,4,6,6,7,8,9,10],[-7,22,-1,1,2,3,5,6,6,7,8,9,10],[-7,23,-1,2,2,3,5,6,7,7,8,9,10],[-7,24,-1,2,3,4,5,6,7,7,8,9,10],[-7,25,-1,2,3,4,5,6,7,8,8,9,10],[-7,26,-1,2,3,4,5,6,8,8,9,9,10],[-7,27,-1,2,3,4,6,6,8,8,9,9,10],[-7,28,-1,2,3,4,6,6,8,9,9,10,10],[-7,29,-1,2,3,4,6,7,8,9,9,10,10],[-7,30,-1,2,4,4,6,7,8,9,10,10,10],[-7,31,-1,2,4,5,6,7,8,9,10,10,11],[-7,32,-1,3,4,5,6,7,8,10,10,10,11],[-7,33,-1,3,4,5,6,8,8,10,10,10,11],[-7,34,-1,3,4,5,6,8,9,10,10,11,11],[-7,35,-1,3,4,5,7,8,9,10,10,11,12],[-7,36,-1,3,5,5,7,8,9,10,11,11,12],[-7,37,-1,3,5,6,7,8,9,10,11,12,12],[-7,38,-1,3,5,6,7,8,10,10,11,12,13],[-7,39,-1,4,5,6,7,8,10,11,11,12,13],[-7,40,-1,4,5,6,7,9,10,11,11,12,13],[-7,41,-1,4,6,6,7,9,10,11,12,12,13],[-7,42,-1,4,6,7,7,9,10,11,12,13,13],[-7,43,-1,4,6,7,8,9,10,11,12,13,14],[-7,44,-1,4,6,7,8,10,10,11,12,13,14],[-7,45,-1,4,6,7,9,10,10,11,12,13,14],[-7,46,-1,4,6,7,9,10,10,12,13,13,14],[-7,47,-1,4,6,7,9,10,11,12,13,13,15],[-7,48,-1,4,6,7,9,10,12,12,13,13,15],[-7,49,-1,4,6,7,10,10,12,12,13,14,15],[-7,50,-1,4,6,8,10,10,12,12,13,15,15],[-7,51,-1,5,7,8,10,10,12,12,13,15,15],[-7,52,-1,5,7,8,10,11,12,12,13,15,15],[-7,53,-1,5,7,9,10,11,12,12,14,15,15],[-7,54,-1,5,7,9,10,11,12,13,14,15,16],[-7,55,-1,5,7,10,10,11,12,13,14,16,16],[-7,56,-1,5,8,10,11,12,12,13,15,16,17],[-7,57,-1,5,8,10,11,11,12,13,15,16,17],[-7,58,-1,5,8,10,11,12,12,13,15,16,17],[-7,59,-1,5,9,10,11,12,12,14,15,16,17],[-7,60,-1,5,9,10,11,12,13,14,15,16,18],[-7,61,-1,5,9,10,11,12,13,14,16,17,18],[-7,62,-1,5,9,10,11,13,13,14,16,17,18],[-7,63,-1,5,9,10,11,13,13,15,17,17,18],[-7,64,-1,5,9,10,11,13,14,15,17,17,18],[-7,65,-1,5,9,10,12,13,14,15,17,18,18],[-7,66,-1,5,9,10,12,13,15,15,17,18,19],[-7,67,-1,5,9,10,12,13,15,16,17,18,19],[-7,68,-1,5,9,10,12,14,15,16,17,19,19],[-7,69,-1,5,9,10,12,14,16,17,18,19,19],[-7,70,-1,5,9,10,13,14,16,17,18,19,20],[-7,71,-1,5,9,10,13,15,16,17,18,19,20],[-7,72,-1,5,9,10,13,15,16,17,18,19,20],[-7,73,-1,5,9,10,13,15,16,17,19,20,21],[-7,74,-1,6,9,10,13,15,16,18,19,20,21],[-7,75,-1,6,9,10,13,16,16,18,19,20,21],[-7,76,-1,6,9,10,13,16,17,18,19,20,21],[-7,77,-1,6,9,10,13,16,17,18,20,21,22],[-7,78,-1,6,9,10,13,16,17,19,20,22,23],[-7,79,-1,6,9,10,13,16,18,19,20,22,23],[-7,80,-1,6,9,10,13,16,18,20,21,22,23],[-7,81,-1,6,9,10,13,17,18,20,21,22,23],[-7,82,-1,6,9,10,14,17,18,20,21,22,24],[-7,83,-1,6,9,11,14,17,18,20,21,23,24],[-7,84,-1,6,9,11,14,17,19,20,21,23,24],[-7,85,-1,6,9,11,14,17,19,21,22,23,24],[-7,86,-1,7,10,11,14,17,19,21,22,23,25],[-7,87,-1,7,10,12,14,17,19,21,22,24,25],[-7,88,-1,7,10,12,14,18,19,21,22,24,25],[-7,89,-1,7,10,12,15,18,19,21,22,24,26],[-7,90,-1,7,10,12,15,18,19,21,23,25,26],[-7,91,-1,7,11,13,15,18,19,21,23,25,26],[-7,92,-1,7,11,13,15,18,20,21,23,25,27],[-7,93,-1,8,11,13,15,18,20,22,23,25,27],[-7,94,-1,8,11,13,16,18,20,22,23,25,28],[-7,95,-1,8,11,14,16,18,20,22,23,26,28],[-7,96,-1,8,11,14,16,19,20,22,23,26,28],[-7,97,-1,8,12,14,16,19,20,22,24,26,28],[-7,98,-1,8,12,15,16,19,20,22,24,27,28],[-7,99,-1,8,12,15,17,19,20,22,24,27,29],[-7,100,-1,8,12,15,18,19,20,22,24,27,30]]
exp_table = ['0','A:1000 B:500','A:1000 B:1000','A:1500 B:1000','A:1500 B:1500','A:2000 B:1500','A:2500 B:2000','A:3000 B:2500','A:4000 B:3000','A:5000 B:4000','A:6000 B:5000','A:7500 B:6000','A:9000 B:7500','A:10500 B:9000','A:12000 B:10500','A:13500 B:12000']
a = random.randint(1,6)

#能力値の登録
@bot.command()
async def regi(ctx, name, arg):
    status = arg.split(',')
    if len(status) != 25:
        await ctx.send('ERROR:ステータス値が不足または超過しています')
    else:
        chara = shelve.open('character.db')
        chara[str(ctx.author.id)] = { 'name' : name, 'dex' : int(status[0]), 'dex_plus' : int(status[1]), 'agi' : int(status[2]), 'agi_plus' : int(status[3]), 'str' : int(status[4]), 'str_plus' : int(status[5]), 'phy' : int(status[6]), 'phy_plus' : int(status[7]), 'int' : int(status[8]), 'int_plus' : int(status[9]), 'men' : int(status[10]), 'men_plus' : int(status[11]), 'exp' : int(status[12]), 'lv' : int(status[13]), 'tec_pack' : int(status[14]), 'mov_pack' : int(status[15]), 'obs_pack' : int(status[16]), 'wis_pack' : int(status[17]), 'hit' : int(status[18]), 'atk' : int(status[19]), 'dog' : int(status[20]), 'def' : int(status[21]), 'mag' : int(status[22]), 'hp' : int(status[23]), 'mp' : int(status[24]) }
        chara.close()
        await ctx.send(f'''以下の情報を保存しました。
        キャラクター名：{name}
        器用度：{status[0]}+{status[1]}
        敏捷度：{status[2]}+{status[3]}
        筋力：{status[4]}+{status[5]}
        生命力：{status[6]}+{status[7]}
        知力：{status[8]}+{status[9]}
        精神力：{status[10]}+{status[11]}
        経験点：{status[12]}
        冒険者レベル：{status[13]}
        技巧判定基礎値：{status[14]}
        運動判定基礎値：{status[15]}
        観察判定基礎値：{status[16]}
        知識判定基礎値：{status[17]}
        命中力：{status[18]}
        追加ダメージ：{status[19]}
        回避力：{status[20]}
        防護点：{status[21]}
        魔力：{status[22]}
        HP：{status[23]}
        MP：{status[24]}''')

#能力値の登録解除
@bot.command()
async def deregi(ctx, name):
    chara = shelve.open('character.db')
    del chara[name]
    chara.close()
    await ctx.send('登録された情報を削除しました。')

#1個だけ6面ダイスを振るコマンド
@bot.command()
async def sr(ctx):
    if bot.user != ctx.author:
        await ctx.send(f'{a}')

#たくさんダイスを振るコマンド
@bot.command()
async def r(ctx, arg1 = 'dflt', arg2 = 'dflt'):
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

#ダメージ計算
@bot.command()
async def dmg(ctx, arg1 = 'dflt', arg2 = 'dflt', arg3 = 'dflt'):
    pips = [random.randint(1, 6) for _ in range(2)]
    sum_pips = sum(pips)
    if arg1.isdecimal() and arg2.isdecimal() and arg3 != 'dflt':
        fixed_pips = sum_pips + int(arg2)
        if fixed_pips >= 13:
            fixed_pips = 12
        else:
            pass
        if sum_pips == 2:
            await ctx.send(f'「{arg3}」 {pips} = {sum_pips} fumble...')
        else:
            damage = damage_table[int(arg1)][fixed_pips]
            await ctx.send(f'「{arg3}」 {pips} = {sum_pips} 出目補正+{arg2} 威力表{arg1}で「{damage}」点のダメージ')
    elif arg1.isdecimal() and arg2.isdecimal() and arg3 == 'dflt':
        fixed_pips = sum_pips + int(arg2)
        if fixed_pips >= 13:
            fixed_pips = 12
        else:
            pass
        if sum_pips == 2:
            await ctx.send(f'{pips} = {sum_pips} fumble...')
        else:
            damage = damage_table[int(arg1)][fixed_pips]
            await ctx.send(f'{pips} = {sum_pips} 出目補正+{arg2} 威力表{arg1}で「{damage}」点のダメージ')
    elif arg1.isdecimal() and arg2 != 'dflt' and arg3 == 'dflt':
        if sum_pips == 2:
            await ctx.send(f'「{arg2}」 {pips} = {sum_pips} fumble...')
        else:
            damage = damage_table[int(arg1)][sum_pips]
            await ctx.send(f'「{arg2}」 {pips} = {sum_pips} 威力表{arg1}で「{damage}」点のダメージ')
    elif arg1.isdecimal() and arg2 == 'dflt' and arg3 == 'dflt':
        if sum_pips == 2:
            await ctx.send(f'{pips} = {sum_pips} fumble...')
        else:
            damage = damage_table[int(arg1)][sum_pips]
            await ctx.send(f'{pips} = {sum_pips} 威力表{arg1}で「{damage}」点のダメージ')
    else:
        await ctx.send('ERROR:威力が適切に入力されていません')

#経験点参照コマンド
@bot.command()
async def exp(ctx, arg):
    if arg.isdecimal():
        level = int(arg)
        await ctx.send(f'技能Lv{level}への上昇に必要な経験点は {exp_table[level]} です。')
    else:
        await ctx.send('ERROR:対象となるLvが適切に入力されていません')

#行使判定
@bot.command()
async def mp(ctx, arg='default'):
    if arg.isdecimal():
        pips = [random.randint(1, 6) for _ in range(2)]
        sum_pips = sum(pips)
        if sum_pips == 2:
            await ctx.send(f'行使判定：{pips} = {sum_pips} fumble...')
        else:
            await ctx.send(f'行使判定：{pips} = {sum_pips} 行使成功')
            pips2 = [random.randint(1, 6) for _2 in range(2)]
            sum_pips2 = sum(pips2)
            if sum_pips == 2:
                await ctx.send(f'{pips2} = {sum_pips2} fumble...')
            else:
                damage = damage_table[int(arg)][sum_pips]
                await ctx.send(f'{pips2} = {sum_pips2} 威力表{arg}で「{damage}」点のダメージ')
    else:
        pips = [random.randint(1, 6) for _ in range(2)]
        sum_pips = sum(pips)
        if sum_pips == 2:
            await ctx.send(f'行使判定：{pips} = {sum_pips} fumble...')
        else:
            await ctx.send(f'行使判定：{pips} = {sum_pips} 行使成功')

#その他汎用コマンド
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
async def t(ctx):
    pips = [random.randint(1, 6) for _ in range(2)]
    sum_pips = sum(pips)
    if sum_pips == 2:
        await ctx.send(f'HPを威力30で回復：{pips} = {sum_pips} fumble...')
    else:
        damage = damage_table[30][sum_pips]
        await ctx.send(f'HPを威力30で回復：{pips} = {sum_pips} 基礎回復量：「{damage}」点')

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
        await ctx.send(f'【キュア・ウーンズ】を行使：{pips} = {sum_pips} 行使成功')
        pips2 = [random.randint(1, 6) for _2 in range(2)]
        sum_pips2 = sum(pips2)
        if sum_pips == 2:
            await ctx.send(f'HPを威力10で回復：{pips2} = {sum_pips2} fumble...')
        else:
            damage = damage_table[10][sum_pips2]
            await ctx.send(f'HPを威力10で回復：{pips2} = {sum_pips2} 基礎回復量：「{damage}」点')

#生命抵抗力判定
@bot.command()
async def lr(ctx, arg: int, plus=0: int):
    chara = shelve.open('character.db')
    dict = chara[ctx.author.id]
    bonus = (dict['phy']+dict['phy_plus']) // 6
    phy = dict['lv'] + bonus
    pips = [random.randint(1, 6) for _ in range(2)]
    sum_pips = sum(pips)
    reached = phy + sum_pips + plus
    if arg <= reached:
        await ctx.send(f'{pips} = {sum_pips} + {phy} (+ {plus}) ≧ {arg} 成功')
    else:
        await ctx.send(f'{pips} = {sum_pips} + {phy} (+ {plus}) ＜ {arg} 失敗')


bot.run(token)
