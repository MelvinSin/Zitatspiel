import asyncio

import config
import bot_functions
import random
import re

class ZitateSpiel:
    def __init__(self, ctx):
        self.ctx = ctx
        self.players = []
        self.points = []

    async def add_player(self, player):
        self.players.append(player)
        self.points.append(0)

    async def spielen(self):

        while config.round_count >= 1:
            #TODO: Aufräumen

            answer_names = await self.neues_zitat()

            if config.debug_mode:
                await self.ctx.send(f'Lösung: \n {config.pair[1]}')

            tmp_msg = self.format_quote()

            await self.ctx.send(tmp_msg)
            await bot_functions.send_dm(tmp_msg)

            dm = ''
            for msg in config.answer_msgs:
                dm += f'Spieler {msg.author} hat geantwortet: {msg.content}\n'

                for i in range(len(self.players)):
                    points_per_name = 1 / len(answer_names)
                    if msg.author == self.players[i]:
                        msg_contents = [name.strip() for name in msg.content.split(' und ')]
                        for x in range(len(msg_contents)):
                            if msg_contents[x] == answer_names[x]:
                                self.points[i] += points_per_name

            await self.ctx.send(dm)
            await bot_functions.send_dm(dm)

            await self.ctx.send(f'Richtig war: {config.pair[1]}\n\n')
            await bot_functions.send_dm(f'Richtig war: {config.pair[1]}\n')

            rankings = sorted(zip(self.players, self.points), key=lambda x: x[1], reverse=True)
            await self.ranking_sorted(rankings)

            if config.round_count == 2:
                await self.ctx.send(f'Noch 1 Runde verbleibend')
                await bot_functions.send_dm(f'Noch 1 Runde verbleibend')

            elif config.round_count > 2:
                await self.ctx.send(f'Noch {config.round_count - 1} Runden verbleibend')
                await bot_functions.send_dm(f'Noch {config.round_count - 1} Runden verbleibend')

            await self.ctx.send(config.SEPERATOR)
            await bot_functions.send_dm(config.SEPERATOR)

            await asyncio.sleep(3)

            config.answer_msgs = []
            config.msgs_send = []
            config.round_count -= 1

        rankings = sorted(zip(self.players, self.points), key=lambda x: x[1], reverse=True)
        await self.ranking_sorted(rankings)
        await self.stats(rankings)
        #TODO: Alles zurücksetzten um neue Runde möglich zu machen

    async def ranking_sorted(self, rankings):
        ranking_message = "Rangliste:\n"
        for rank, (player, point) in enumerate(rankings, start=1):
            if point == 1:
                ranking_message += f"{rank}. {player}: {point} Punkt\n"
            else:
                ranking_message += f"{rank}. {player}: {point} Punkte\n"
        await self.ctx.send(ranking_message)
        await bot_functions.send_dm(ranking_message)

    async def stats(self, rankings):
        if config.debug_mode:
            return
        else:
            stats = self.load_stats()
            self.update_stats(rankings, stats)
            self.save_stats(stats)
            await self.ctx.send('Statistiken wurden aktualisiert!')

    def load_stats(self):
        stats = {}
        with open('statistiken.txt', 'r', encoding='utf-8') as file:
            for line in file:
                player, points, rounds = line.strip().split(':')
                stats[player] = {
                    'global_points': float(points),
                    'global_rounds': int(rounds)
                }
        file.close()
        return stats

    def update_stats(self, rankings, stats):
        for rank, (player, point) in enumerate(rankings, start=1):
            if player in stats:
                stats[player]['global_points'] += point
                stats[player]['global_rounds'] += config.init_round_count
            else:
                stats[player] = {
                    'global_points': point,
                    'global_rounds': config.init_round_count
                }

    def save_stats(self, stats):
        with open('statistiken.txt', 'w', encoding='utf-8') as file:
            for player, data in stats.items():
                file.write(f"{player}:{data['global_points']}:{data['global_rounds']}\n")

    async def neues_zitat(self):

        used_zeilennummern = []
        zeilennummer = random.randint(1, config.zitat_count)

        while zeilennummer in used_zeilennummern:
            zeilennummer = random.randint(1, config.zitat_count)

        used_zeilennummern.append(zeilennummer)

        config.pair = bot_functions.zitate_auslesen(zeilennummer)
        answer_names = [name.strip() for name in config.pair[1].split(' und ')]
        return answer_names

    def format_quote(self):
        quote = config.pair[0]
        match = re.match(r'^(\d+)\sPersonen:', quote)
        if match:
            number = match.group(1)
            remaining_quote = quote.removeprefix(f'{number} Personen:')
            tmp_msg = f'Zitat({number}): \n {remaining_quote}'
        else:
            tmp_msg = f'Zitat: \n\n {quote}'
        return tmp_msg
