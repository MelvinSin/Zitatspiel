import os
from bot import bot
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":

    token = os.getenv('TOKEN')
    bot.run(token)  # Letzte Zeile