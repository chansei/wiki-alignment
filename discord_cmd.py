import datetime
import json
import os
import re

import requests
from discord.ext import commands
from urllib.parse import urlparse
from googletrans import Translator

from wiki import Wiki

# ------ api url ------
wiki_id = "restapitest"
page_name = "外部ニュース"

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
    text = text.replace('**', "''")  # 太字の構文変更(**->'')
    text = text.replace('__', "%%%")  # 下線の構文変更(__->%%%)
    text = re.sub('<#(.*?)>|<:(.*?)> ', '', text)  # メンションと(サ－バー)絵文字の除去
    text = text.replace('@here', '').replace('@everyone', '')  # "@here"と"@everyone"の除去
    return text


def extract_links(text):
    rtn = ""
    youtube_pattern = r'https?://(?:www\.)?(?:youtu\.be|youtube\.com)/[^\s]+'
    x_pattern = r'https?://(?:www\.)?x\.com/[^\s]+'

    # 各ドメインのリンクを抽出
    youtube_links = re.findall(youtube_pattern, text)
    x_links = re.findall(x_pattern, text)

    for link in youtube_links:
        if "=" in link:
            rtn += f"#youtube({link.split('=')[-1]})\n"
        else:
            rtn += f"#youtube({link.split('/')[-1]})\n"

    for link in x_links:
        rtn += f"#twitter_tweet({link.split('/')[-1]})\n"

    return rtn


async def translate_text(text, retries=3):
    translator = Translator()
    for _ in range(retries):
        try:
            result = await translator.translate(text, dest='ja')
            return result.text
        except Exception:
            pass
    return None

# ------ command method ------


class cmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ------ コマンド ------
    @commands.command()  # 生存確認
    async def ping(self, ctx):
        await ctx.send('pong!')

    # ------ 読み取り ------
    @commands.Cog.listener()
    async def on_message(self, message):
        global api_token
        wiki = Wiki(wiki_id, os.getenv('api_id'), os.getenv('secret'))
        with open("texts/text01.txt", "r", encoding="utf-8") as f:  # ヘッダー部分
            text = f.read()
        for channel in self.bot.get_channel(notice_category).channels:
            text += ("\n**"+channel.name+"\n")
            history = await channel.history(limit=5).flatten()
            for message in reversed(history):
                text_tmp = opt_txt(message.content)
                text += ("***"+(message.created_at+datetime.timedelta(hours=9)).strftime('%Y/%m/%d %H:%M')+"\n")  # 見出し
                for i, attachment in enumerate(message.attachments):
                    # 進行状況を表示
                    print(f"Processing upload images({i+1}/{len(message.attachments)})")
                    file_name = urlparse(attachment.url).path.split('/')[-1]
                    # ファイルをダウンロード
                    r = requests.get(attachment.url)
                    with open(file_name, "wb") as f:
                        f.write(r.content)
                    # ファイルをアップロード
                    wiki.put_file(page_name, file_name, file_name)
                    # ファイルを削除
                    os.remove(file_name)
                    text += ("&ref("+file_name+",nolink,50%);\n")
                text += (text_tmp+"\n")  # 本文
                text_ja = await translate_text(text_tmp)  # 翻訳
                if text_ja:
                    text += ("(自動翻訳)\n"+text_ja+"\n")
                text += extract_links(text_tmp)
                text += ("\n----\n")

            # print(text)
        with open("texts/text02.txt", "r", encoding="utf-8") as f:  # フッター部分
            text += f.read()
        print(wiki.put_page(page_name, text))
