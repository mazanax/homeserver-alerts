import asyncio
import logging
import os.path
import sys
from os import getenv
from os.path import getmtime
from time import time

from dotenv import load_dotenv
from telegram import Bot
from telegram.constants import ParseMode

load_dotenv()
TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT = getenv("TELEGRAM_CHAT")

if not TELEGRAM_TOKEN:
    print("err: Telegram token required")
    exit(1)

if not TELEGRAM_CHAT:
    print("err: Telegram chat required")
    exit(1)


async def main() -> None:
    bot = Bot(TELEGRAM_TOKEN)
    if not os.path.exists("heartbeat"):
        return

    async with bot:
        with open("heartbeat", "r") as heartbeat:
            last_heartbeat = int(heartbeat.read())
            if last_heartbeat <= int(time() - 300):
                if not os.path.exists("lastalert"):
                    await bot.send_message(chat_id=TELEGRAM_CHAT,
                                           text="🔴 The <b>homeserver</b> has been unavailable for 5 minutes",
                                           parse_mode=ParseMode.HTML)
                    with open("lastalert", "w") as f:
                        f.write("")
                else:
                    with open("lastalert", "r+") as f:
                        if f.read() == "" and int(getmtime("lastalert")) <= int(time() - 300):
                            await bot.send_message(chat_id=TELEGRAM_CHAT,
                                                   text="🔴 The <b>homeserver</b> still unavailable",
                                                   parse_mode=ParseMode.HTML)
                            f.write(f"{int(time())}")
            elif last_heartbeat > int(time() - 120):
                if os.path.exists("lastalert"):
                    await bot.send_message(chat_id=TELEGRAM_CHAT,
                                           text="🟢 The <b>homeserver</b> is available again",
                                           parse_mode=ParseMode.HTML)
                    os.remove("lastalert")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
