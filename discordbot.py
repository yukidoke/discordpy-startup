from discord.ext import commands
import os
import traceback

extensions = [
    'cogs.explain',
    'cogs.register',
    'cogs.dice',
    'cogs.damage',
    'cogs.shortcuts'
    'cogs.judge'
    'cogs.rewards'
]

# クラスの定義。ClientのサブクラスであるBotクラスを継承。
class MyBot(commands.Bot):
    # MyBotのコンストラクタ。
    def __init__(self, command_prefix):
        # スーパークラスのコンストラクタに値を渡して実行。
        super().__init__(command_prefix)
        # INITIAL_COGSに格納されている名前から、コグを読み込む。
        # エラーが発生した場合は、エラー内容を表示。
        for cog in extensions:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    async def on_ready(self):
        print('剣の加護があらんことを。')

# MyBotのインスタンス化及び起動処理。
if __name__ == '__main__':
    bot = MyBot(command_prefix='-')
    token = os.environ['DISCORD_BOT_TOKEN']
    bot.run(token)
