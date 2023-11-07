import datetime
import json
import os
import re

import requests
from discord.ext import commands
from urllib.parse import urlparse
import wiki

# ------ api url ------
api_url_auth = "https://api.wikiwiki.jp/wotblitz/auth"
api_url_page = "https://api.wikiwiki.jp/wotblitz/page/外部ニュース"

# ------ api value ------
pwd = os.getenv('pwd')
notice_category = 1003571877182193745

# ------ global value ------
api_token = ""

# ------ setup method ------
def setup(bot):
    bot.add_cog(cmd(bot))

# ------ other method ------
def opt_txt(text):
    text = text.replace('**',"''") # 太字の構文変更(**->'')
    text = text.replace('*', "'''") # 斜字の構文変更(**->''')
    text = text.replace('__',"%%%") # 下線の構文変更(__->%%%)
    text = re.sub('<#(.*?)>|<:(.*?)> ','',text) # メンションと(サ－バー)絵文字の除去
    return text

# ------ command method ------
class cmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ------ コマンド ------
    @commands.command() # 生存確認
    async def ping(self, ctx):
        await ctx.send('pong!')

    # ------ 読み取り ------
    @commands.Cog.listener()
    async def on_message(self, message):
        global api_token
        api_token = wiki.api_auth(api_url_auth, pwd)['token'] # ログイン処理
        with open("texts/text01.txt", "r", encoding="utf-8") as f: # ヘッダー部分
            text = f.read()
        for channel in self.bot.get_channel(notice_category).channels:
            text += ("\n**"+channel.name+"\n")
            history = await channel.history(limit=5).flatten()
            for message in reversed(history):
                text_tmp = opt_txt(message.content)
                text += ("***"+(message.created_at+datetime.timedelta(hours=9)).strftime('%Y/%m/%d %H:%M')+"\n") # 見出し
                for attachment in message.attachments: # 画像
                    _url = urlparse(attachment.url)
                    url = f"{_url.scheme}://{_url.netloc}{_url.path}"
                    text += ("&attachref("+url+",zoom,200x360);\n")
                text += (text_tmp+"\n----\n") # 本文
            # print(text)
        with open("texts/text02.txt", "r", encoding="utf-8") as f: # フッター部分
            text += f.read()
        print(wiki.api_put(api_url_page, api_token, text))