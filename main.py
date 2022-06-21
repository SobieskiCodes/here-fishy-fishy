from discord.ext import commands
import discord
import json
import os


intents = discord.Intents.default()
with open('here_fishy_fishy/config.json', 'r') as file:
    config = json.load(file)
bot = commands.Bot(command_prefix=config.get('guild').get('prefix'), intents=intents)
path_dir = config.get('paths').get('main_dir')
bot.config = config


@bot.event
async def on_ready():
    print('logged in')


def load_extensions():
    f = []
    for (dir_path, dir_names, filenames) in os.walk(f"{path_dir}cogs"):
        f.extend(filenames)
        break
    for extension in f:
        try:
            bot.load_extension(f"cogs.{extension[:-3]}")
            print(f"Loaded {extension}")
        except Exception as e:
            exc = f'{type(e).__name__}: {e}'
            print(f'Failed to load extension {extension}\n{exc}')


load_extensions()
bot.run(bot.config.get('keys').get('discord'))
