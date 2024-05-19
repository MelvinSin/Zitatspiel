import asyncio
import time
import discord

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

        config.answer_msgs.append(message)
        await message.channel.send('Danke für deine Antwort! ')

    else:
        print(f'Message from {message.author}: {message.content}')
        await bot.process_commands(message)

async def initialize_game(ctx):
    global zitat_count

    if config.game_state == 'ready':
        await ctx.send('Beginne das Spiel. Bitte füge mit $add Spieler hinzu: ')
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
    await ctx.send(f'{player.mention} wurde als Spieler hinzugefügt.')

async def start(ctx):
    if config.game_state != 'add_players':
        await ctx.send('Aktuell kann nicht gestartet werden.')
        return
    if len(config.players) == 0:
        await ctx.send(ctx,'Mindestens 1 Spieler erforderlich')
        return
    await ctx.send('Spiel wurde gestartet.\n\n')
    config.game_state = 'started'
    await spielen(ctx)

async def spielen(ctx):

    while True:
        zeilennummer = random.randint(1, zitat_count)
        pair = zitate_auslesen(zeilennummer)
        await ctx.send(pair[0],delete_after=config.delete_after)

        await send_dm('Bitte gebe deine Lösung an: ')

        for msg in config.answer_msgs:
            await ctx.send(f'Spieler {msg.author} hat geantwortet: {msg.content}', delete_after=config.delete_after)
            for i in range(len(config.players)):
                if msg.author == config.players[i] and msg.content == pair[1]:
                    config.points[i] += 1

        await ctx.send(f'Richtig war: {pair[1]}\n', delete_after=config.delete_after)
        for i in range(len(config.players)):
            await ctx.send(f'Spieler {config.players[i]} hat {config.points[i]} Punkte!', delete_after=config.delete_after)

        config.answer_msgs = []

async def send_dm(msg):

    for player_name in config.players:
        await player_name.send(content=msg,delete_after=600)
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