import asyncio
import time
import discord
from bot import bot

import config
from discord.ext import commands
import random


async def process_message(message, bot):
    if message.author == bot.user:
        return
    if isinstance(message.channel, discord.DMChannel) and config.game_state == 'wait_for_dm':

        for msg in config.answer_msgs:
            if msg.author == message.author:
                await message.channel.send('Du hast bereits geantwortet. Bitte geduld.')
                return
        if message.content == '$namen':
            await name(message.channel)
            return
        if message.content not in config.names:
            await message.channel.send('Ungültige Eingabe.')
            return
        config.answer_msgs.append(message)

    else:
        print(f'Message from {message.author}: {message.content}')
        await bot.process_commands(message)


async def initialize_game(ctx):
    global zitat_count

    if config.game_state == 'ready':
        config.msgs_send.append(await ctx.send('Beginne das Spiel. Bitte füge mit $add Spieler hinzu und setze die Rundenzahl mit @rundenzahl x'))
        await name(ctx)
        await befehle(ctx)
        config.game_state = 'add_players'

        with open('zitate.txt', 'r', encoding='utf-8') as file:
            zitat_count = sum(1 for line in file)

    else:
        await ctx.send('Initialisierung aktuell nicht möglich')


async def add_player(ctx, member_name):
    if config.game_state != 'add_players':
        await ctx.send('Aktuell können keine Spieler hinzugefügt werden.')
        return

    if member_name == '':
        await ctx.send('Bitte verwende @Name.')

    # Überprüfe, ob das übergebene Argument ein Mitglied des Servers ist
    try:
        player = await commands.MemberConverter().convert(ctx, member_name)

    except commands.MemberNotFound:
        await ctx.send('Ungültiges Mitglied. Bitte verwende @Name.')
        return

    # Füge das Mitglied zur Liste der Spieler hinzu
    config.players.append(player)
    config.points.append(0)
    config.msgs_send.append(await ctx.send(f'{player.mention} wurde als Spieler hinzugefügt.'))


async def start(ctx):
    if config.game_state != 'add_players':
        await ctx.send('Aktuell kann nicht gestartet werden.')
        return
    if len(config.players) == 0:
        await ctx.send('Mindestens 1 Spieler erforderlich')
        return

    for msg in config.msgs_send:
        await msg.delete()
    config.msgs_send = []
    await ctx.send('Spiel wurde gestartet.\r\r')
    await ctx.send('--------------------------------------------------------------------------------------')
    config.game_state = 'started'
    await spielen(ctx)


async def spielen(ctx):
    while config.round_count >= 1:
        zeilennummer = random.randint(1, zitat_count)
        pair = zitate_auslesen(zeilennummer)
        await ctx.send(f'Zitat: \n {pair[0]}')
        await send_dm(f'Zitat: \n {pair[0]}', 0)

        dm = ''
        for msg in config.answer_msgs:
            dm += f'Spieler {msg.author} hat geantwortet: {msg.content}\n'

            for i in range(len(config.players)):
                if msg.author == config.players[i] and msg.content == pair[1]:
                    config.points[i] += 1

        await ctx.send(dm)
        await send_dm(dm, 0)

        await ctx.send(f'Richtig war: {pair[1]}\n')
        await send_dm(f'Richtig war: {pair[1]}\n', 0)

        for msg in config.msgs_send_delete_later:
            await msg.delete()
        config.msgs_send_delete_later = []

        #for i in range(len(config.players)):
        #   config.msgs_send_delete_later.append(await ctx.send(f'Spieler {config.players[i]} hat {config.points[i]} Punkte!'))
        #  await send_dm(f'Spieler {config.players[i]} hat {config.points[i]} Punkte!',1)

        await sort_ranking(ctx)

        if config.round_count == 2:
            await ctx.send(f'Noch 1 Runde verbleibend')
            await send_dm(f'Noch 1 Runde verbleibend', 1)

        elif config.round_count > 2:
            await ctx.send(f'Noch {config.round_count - 1} Runden verbleibend')
            await send_dm(f'Noch {config.round_count - 1} Runden verbleibend', 1)


        await ctx.send('--------------------------------------------------------------------------------------')

        await asyncio.sleep(3)

        for msg in config.msgs_send:
            await msg.delete()

        config.answer_msgs = []
        config.msgs_send = []
        config.round_count -= 1

    for msg in config.msgs_send_delete_later:
        await msg.delete()

    await sort_ranking(ctx)


async def send_dm(msg, later):
    for player_name in config.players:
        if later == 1:
            config.msgs_send_delete_later.append(await player_name.send(content=msg))
        else:
            config.msgs_send.append(await player_name.send(content=msg))
    config.game_state = 'wait_for_dm'
    while len(config.players) != len(config.answer_msgs):
        await asyncio.sleep(5)
    config.game_state = 'dm_done'


def zitate_auslesen(zeilennummer):
    with open('zitate.txt', 'r', encoding='utf-8') as file:
        quotes = file.readlines()[zeilennummer - 1].strip().strip('"')

    with open('zitierer.txt', 'r', encoding='utf-8') as file:
        authors = file.readlines()[zeilennummer - 1].strip().strip('"')

    pair = (quotes, authors)
    return pair


async def set_round_count(ctx, round_count):
    if config.game_state == 'add_players':
        config.round_count = int(round_count)
        await ctx.send(f'Es werden {round_count} Runden gespielt.')
    else:
        await ctx.send('Rundenzahl aktuell nicht setzbar.')


async def name(ctx):
    response = ('--------------------------------------------------------------------------------------\n'
                'Antwortmöglichkeiten:\n')
    if len(config.names) == 0:
        with open('zitierer.txt', 'r', encoding='utf-8') as file:
            for line in file:
                words = line.split()
                for word in words:
                    if word != 'und':
                        config.names.add(word)

    response += '\n'.join([f'- {name}' for name in config.names])
    response += '\n--------------------------------------------------------------------------------------'

    await ctx.send(response)

async def sort_ranking(ctx):
    rankings = sorted(zip(config.players, config.points), key=lambda x: x[1], reverse=True)
    ranking_message = "Rangliste:\n"
    for rank, (player, point) in enumerate(rankings, start=1):
        if point == 1:
            ranking_message += f"{rank}. {player}: {point} Punkt\n"
        else:
            ranking_message += f"{rank}. {player}: {point} Punkte\n"
    await ctx.send(ranking_message)
    await send_dm(ranking_message, 1)
async def befehle(ctx):
    command_list = [f'- {command.name}' for command in bot.commands]
    formatted_commands = '\n'.join(command_list)
    message = (f'--------------------------------------------------------------------------------------\n'
               f'Command Liste:\n{formatted_commands}\n'
               f'--------------------------------------------------------------------------------------')
    await ctx.send(message)