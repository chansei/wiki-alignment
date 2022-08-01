import asyncio
import cmd
import os
import traceback

import discord
from discord.ext import commands

TOKEN = os.getenv('token')

print(TOKEN)

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
