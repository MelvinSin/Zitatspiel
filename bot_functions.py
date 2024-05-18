import config
from discord.ext import commands
async def process_message(message, bot):

    if message.author == bot.user:
        return
    else:
        print(f'Message from {message.author}: {message.content}')
        await bot.process_commands(message)

async def initialize_game(ctx):

    if config.game_state == 'ready':
        await ctx.send('Beginne das Spiel. Bitte füge mit $add Spieler hinzu: ')
        config.game_state = 'add_players'
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
        member = await commands.MemberConverter().convert(ctx, member_name)
    except commands.MemberNotFound:
        await ctx.send('Ungültiges Mitglied. Bitte verwende @Name.')
        return

    # Füge das Mitglied zur Liste der Spieler hinzu
    config.players.append(member)
    await ctx.send(f'{member.mention} wurde als Spieler hinzugefügt.')

async def start(ctx):
    if config.game_state != 'add_players':
        await ctx.send('Aktuell kann nicht gestartet werden.')
        return
    if len(config.players) == 0:
        await ctx.send('Mindestens 1 Spieler erforderlich')
        return
    await ctx.send('Spiel wurde gestartet.')
    config.game_state = 'started'
