import json
import os
from datetime import datetime

import requests
from discord.ext import commands

import wiki

# ------ api url ------
api_url_auth = "https://api.wikiwiki.jp/restapitest/auth"
api_url_page = "https://api.wikiwiki.jp/restapitest/page/外部ニュース"

# ------ api value ------
pwd = os.environ["pwd"]
notice_category = [1003571877182193745]

# ------ global value ------
api_token = ""

# ------ setup method ------
def setup(bot):
    bot.add_cog(cmd(bot))

# ------ command method ------
class cmd(commands.Cog):
    def __init__(self, bot):
        global api_token
        api_token = wiki.api_auth(api_url_auth, pwd)['token']
        self.bot = bot

    # ------ コマンド ------
    @commands.command() # 生存確認
    async def ping(self, ctx):
        await ctx.send('pong!')

    # ------ 読み取り ------
    @commands.Cog.listener()
    async def on_message(self, message):
        global api_token
        if message.channel.category_id not in notice_category: # 指定したカテゴリー外なら無視する
            return
        with open("texts/text01.txt", "r", encoding="utf-8") as f: # ヘッダー部分
            text = f.read()
        for channel in self.bot.get_channel(message.channel.category_id).channels:
            text += ("\n**"+channel.name+"\n")
            history = await channel.history(limit=5).flatten()
            for message in reversed(history):
                text += ((message.created_at+datetime.timedelta(hours=9)).strftime('%Y/%m/%d %H:%M')+"\n"+message.content+"\n----\n")
        with open("texts/text02.txt", "r", encoding="utf-8") as f: # フッター部分
            text += f.read()
        print(wiki.api_put(api_url_page, api_token, text))






