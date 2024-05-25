import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    print(f'Bot: {bot.user} online')


@bot.event
async def on_message(message):
    import bot_functions
    await bot_functions.process_message(message, bot)


@bot.command()
async def init(ctx):
    import bot_functions
    await bot_functions.init_command(ctx)


@bot.command()
async def add(ctx, *, member_name):
    import bot_functions
    await bot_functions.add_command(ctx, member_name)


@bot.command()
async def start(ctx):
    import bot_functions
    await bot_functions.start_command(ctx)


@bot.command()
async def rundenzahl(ctx, *, round_count):
    import bot_functions
    await bot_functions.rundenzahl_command(ctx, round_count)


@bot.command()
async def namen(ctx):
    import bot_functions
    await bot_functions.namen_command(ctx)


@bot.command()
async def befehle(ctx):
    import bot_functions
    await bot_functions.befehle_command(ctx)
