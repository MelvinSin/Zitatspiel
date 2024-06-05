import asyncio

import config
import bot_functions
import random

class ZitateSpiel:
    def __init__(self, ctx, zitat_count):
        self.ctx = ctx
        self.zitat_count = zitat_count
        self.players = []
        self.points = []
    async def add_player(self, player):
        self.players.append(player)
        self.points.append(0)

    async def spielen(self):

        while config.round_count >= 1:
            zeilennummer = random.randint(1, self.zitat_count)
            config.pair = bot_functions.zitate_auslesen(zeilennummer)
            answer_names = [name.strip() for name in config.pair[1].split(' und ')]

            if config.debug_mode:
                await self.ctx.send(f'Lösung: \n {config.pair[1]}')

            await self.ctx.send(f'Zitat: \n {config.pair[0]}')
            await bot_functions.send_dm(f'Zitat: \n {config.pair[0]}', 0)

            dm = ''
            for msg in config.answer_msgs:
                dm += f'Spieler {msg.author} hat geantwortet: {msg.content}\n'

                for i in range(len(self.players)):
                    if len(answer_names) == 1:
                        if msg.author == self.players[i] and msg.content == config.pair[1]:
                            self.points[i] += 1
                    else:
                        points_per_name = 1 / (len(answer_names) + 1)
                        if msg.author == self.players[i]:
                            msg_contents = [name.strip() for name in msg.content.split(' und ')]
                            for msg_content in msg_contents:
                                if msg_content in answer_names:
                                    self.points[i] += points_per_name
                            identisch = True
                            for x in range(len(msg_contents)):
                                if msg_contents[x] != answer_names[x]:
                                    identisch = False
                            if identisch:
                                self.points[i] += points_per_name

            await self.ctx.send(dm)
            await bot_functions.send_dm(dm, 0)

            await self.ctx.send(f'Richtig war: {config.pair[1]}\n')
            await bot_functions.send_dm(f'Richtig war: {config.pair[1]}\n', 0)

            for msg in config.msgs_send_delete_later:
                await msg.delete()
            config.msgs_send_delete_later = []

            await self.sort_ranking(self.ctx)

            if config.round_count == 2:
                await self.ctx.send(f'Noch 1 Runde verbleibend')
                await bot_functions.send_dm(f'Noch 1 Runde verbleibend', 1)

            elif config.round_count > 2:
                await self.ctx.send(f'Noch {config.round_count - 1} Runden verbleibend')
                await bot_functions.send_dm(f'Noch {config.round_count - 1} Runden verbleibend', 1)

            await self.ctx.send(config.SEPERATOR)

            await asyncio.sleep(3)

            for msg in config.msgs_send:
                await msg.delete()

            config.answer_msgs = []
            config.msgs_send = []
            config.round_count -= 1

        for msg in config.msgs_send_delete_later:
            await msg.delete()

        await self.sort_ranking(self.ctx)

    async def sort_ranking(self, ctx):
        rankings = sorted(zip(self.players, self.points), key=lambda x: x[1], reverse=True)
        ranking_message = "Rangliste:\n"
        for rank, (player, point) in enumerate(rankings, start=1):
            if point == 1:
                ranking_message += f"{rank}. {player}: {point} Punkt\n"
            else:
                ranking_message += f"{rank}. {player}: {point} Punkte\n"
        await ctx.send(ranking_message)
        await bot_functions.send_dm(ranking_message, 1)
