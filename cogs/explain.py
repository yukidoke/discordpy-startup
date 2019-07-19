from discord.ext import commands

# コグとして用いるクラスを定義。
class Explain(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def swds(self, ctx):
        await ctx.send('''Sword World Diceroll System
        略称SWDSです。ソーズ(Swords)とお呼び下さい。
        `-r`で2d6を振ります。`-sr`で1d6を振ります。
        ダイスロールに関する詳細は`-dice`
        能力値の更新などに関する詳細は`-stat`
        その他のコマンドに関する詳細は`-cmds`で参照できます。''')

    @commands.command()
    async def dice(self, ctx):
        await ctx.send('''【ダイスロール関係について】
        `-r`で2d6を振ります。`-sr`で1d6を振ります。
        nをダイスの数、Nを面の数として、`-r ndN`で指定された通りにダイスを振ります。
        nを0から100までの整数として、`-dmg n`で威力表nのダメージを算出します。
        出目の補正値Nがある場合は、`-dmg n N`でそれを反映します。
        上記のコマンドには末尾にセリフを入れることも出来ます。
        例：`-r 5d6 名誉点決定`
        行使判定を命中力判定などと区別しておきたい場合は`-mp`が有効です。
        ダメージを伴う魔法の場合は、威力をnとして、`-mp n`でダメージまで同時に算出します。''')

    @commands.command()
    async def stat(self, ctx):
        await ctx.send('''【能力値関係について】
        `-regi character_name (status)`で冒険者の情報を登録します。
        指輪・腕輪込の能力値とその成長（dex,agi,str,phy,int,menの順）、経験点、冒険者レベル、各種判定パッケージ基礎値（tec,mov,obs,wisの順）、命中力、追加ダメージ、回避力、防護点、魔力、HP、MPの合計25の数値が必須です。
        `-deregi`で登録情報を削除します。
        `-status`で登録した情報を参照します。
        `-ref status`で任意のステータスを参照します。
        nを整数として、`-change status n`で任意のステータスにnを加えます。
        目標値をNとして、`-tec N`で技巧判定、`-mov N`で運動判定、`-obs N`で観察判定、`-wis N`で知識判定、`-hit N`で命中力判定、`-dog N`で回避力判定、`-pr N`で生命抵抗力判定、`-mr N`で精神抵抗力判定が行えます。
        `-grow (status)`で任意の能力値を成長させられます。''')

    @commands.command()
    async def cmds(self, ctx):
        await ctx.send('''【その他のコマンドについて】
        技能Lvを1上げてnにするために必要な経験点は`-exp n`で参照できます。
        また、よく使われるであろうアイテムや魔法は別のコマンドで代替できます。
        `-q`で＜救命草＞を使用します。`-m`で＜魔香草＞を使用します。
        `-h`で＜ヒーリングポーション＞を使用します。
        `-t`で＜トリートポーション＞を使用します。
        `-cw`で【キュア・ウーンズ】を行使します。''')

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Explain(bot))
