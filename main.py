import asyncio
import cmd
import os
import traceback

import discord
from discord.ext import commands
from dotenv import load_dotenv

# ------ .envファイルからロードするかデフォルトの環境変数を利用 ------
try:
    load_dotenv()
except Exception:
    print("using default environ")

TOKEN = os.getenv('token')

INITIAL_EXTENSIONS = [
    'cmd'
]

bot = commands.Bot(command_prefix="-", help_command=None, intents=discord.Intents.all())

for cog in INITIAL_EXTENSIONS:
    try:
        bot.load_extension(cog)
    except Exception:
        traceback.print_exc()

@bot.event
async def on_ready():
    print('Ready')

bot.run(TOKEN)
