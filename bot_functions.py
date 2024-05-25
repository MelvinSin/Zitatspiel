import asyncio
import discord
from bot import bot
from game_state import GameState, GameStateEnum
import config
from discord.ext import commands
from game import ZitateSpiel
from state_checker import check_state


async def process_message(message, bot):
    if message.author == bot.user:
        return
    if isinstance(message.channel, discord.DMChannel) and config.game_state == 'wait_for_dm':
        await process_dm(message)
    else:
        await bot.process_commands(message)


async def process_dm(message):
    for msg in config.answer_msgs:
        if msg.author == message.author:
            await message.channel.send('Du hast bereits geantwortet. Bitte geduld.')
            return
    if message.content == '$namen':
        await namen_command(message.channel)
        return
    if message.content not in config.names:
        await message.channel.send('Ungültige Eingabe.')
        return
    config.answer_msgs.append(message)


@check_state(GameStateEnum.NOT_INITIALISED)
async def init_command(ctx):
    global game

    config.msgs_send.append(await ctx.send(
        'Beginne das Spiel. Bitte füge mit $add Spieler hinzu und setze die Rundenzahl mit @rundenzahl x'))
    await namen_command(ctx)
    await befehle_command(ctx)

    with open('zitate.txt', 'r', encoding='utf-8') as file:
        zitat_count = len(file.readlines())
        game = ZitateSpiel(ctx, zitat_count)
    GameState().set_state(GameStateEnum.SETUP)


@check_state(GameStateEnum.SETUP)
async def add_command(ctx, member_name):
    if member_name == '':
        await ctx.send('Bitte verwende @Name.')

    # Überprüfe, ob das übergebene Argument ein Mitglied des Servers ist
    try:
        player = await commands.MemberConverter().convert(ctx, member_name)
    except commands.MemberNotFound:
        await ctx.send('Ungültiges Mitglied. Bitte verwende @Name.')
        return

    # Füge das Mitglied zur Liste der Spieler hinzu
    await game.add_player(player)
    config.msgs_send.append(await ctx.send(f'{player.mention} wurde als Spieler hinzugefügt.'))


@check_state(GameStateEnum.SETUP)
async def start_command(ctx):
    if len(game.players) == 0:
        await ctx.send('Mindestens 1 Spieler erforderlich')
        return

    for msg in config.msgs_send:
        await msg.delete()
    config.msgs_send = []
    await ctx.send('Spiel wurde gestartet.\r\r')
    await ctx.send(config.SEPERATOR)
    GameState().set_state(GameStateEnum.STARTED)
    await ZitateSpiel.spielen(game)


def zitate_auslesen(zeilennummer):
    with open('zitate.txt', 'r', encoding='utf-8') as file:
        quotes = file.readlines()[zeilennummer - 1].strip().strip('"')

    with open('zitierer.txt', 'r', encoding='utf-8') as file:
        authors = file.readlines()[zeilennummer - 1].strip().strip('"')

    pair = (quotes, authors)
    return pair


async def rundenzahl_command(ctx, round_count):
    if config.game_state == 'add_players':
        config.round_count = int(round_count)
        await ctx.send(f'Es werden {round_count} Runden gespielt.')
    else:
        await ctx.send('Rundenzahl aktuell nicht setzbar.')


async def namen_command(ctx):
    response = 'Antwortmöglichkeiten:\n'
    await load_names()
    response += '\n'.join([f'- {name}' for name in config.names])
    await send_formatted(ctx, response + '\n')


async def load_names():
    if len(config.names) == 0:
        with open('zitierer.txt', 'r', encoding='utf-8') as file:
            for line in file:
                words = line.split()
                for word in words:
                    if word != 'und':
                        config.names.add(word)


async def befehle_command(ctx):
    command_list = [f'- {command.name}' for command in bot.commands]
    formatted_commands = '\n'.join(command_list)
    response = f'Command Liste:\n{formatted_commands}\n'
    await send_formatted(ctx, response)


async def send_formatted(ctx, msg):
    formatted_msg = f'{config.SEPERATOR}\n{msg}{config.SEPERATOR}'
    await ctx.send(formatted_msg)


async def send_dm(msg, later):
    for player_name in game.players:
        if later == 1:
            config.msgs_send_delete_later.append(await player_name.send(content=msg))
        else:
            config.msgs_send.append(await player_name.send(content=msg))
    config.game_state = 'wait_for_dm'
    while len(game.players) != len(config.answer_msgs):
        await asyncio.sleep(5)
    config.game_state = 'dm_done'
