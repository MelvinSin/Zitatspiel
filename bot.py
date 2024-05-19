import discord
from discord.ext import commands
import config
import bot_functions

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot: {bot.user} online')

@bot.event
async def on_message(message):
    await bot_functions.process_message(message, bot)

@bot.command()
async def init(ctx):
    await bot_functions.initialize_game(ctx)

@bot.command()
async def add(ctx, *, member_name):
    await bot_functions.add_player(ctx, member_name)

@bot.command()
async def start(ctx):
    await bot_functions.start(ctx)

@bot.command()
async def rundenzahl(ctx, *, round_count):
    await bot_functions.set_round_count(ctx,round_count)

@bot.command()
async def namen(ctx):
    await bot_functions.name(ctx)