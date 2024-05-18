import os
from bot import bot
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    bot.run(os.getenv('TOKEN'))  # Letzte Zeile