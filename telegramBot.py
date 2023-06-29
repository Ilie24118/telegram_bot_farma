import logging
import pandas as pd
import requests
import asyncio
import telegram

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from functools import wraps

token = "" # <---------- Token ---------|


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    dataFrame = pd.read_csv("info.csv", header=None)
    count = 0
    for addres in dataFrame[0]:
        # print(dataFrame[1][count])
        if dataFrame[1][count] >= 999:
            await update.message.reply_text(f"{addres} - Unknown Distance")
        else:
            await update.message.reply_text(addres)
        count = count + 1


async def send(chat, msg):
    await telegram.Bot(token).sendMessage(
        chat_id=chat, text=msg
    )


async def restrict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Access denied"
    )


"""Start the bot."""
# Create the Application and pass it your bot's token.
application = (
    Application.builder()
    .token(token)
    .build()
)
usr_id = 0 # <----- USER ID ----------------|


# Restrict bot to the specified user_id
restrict_handler = MessageHandler(~filters.User(usr_id), restrict)
application.add_handler(restrict_handler)

# on different commands - answer in Telegram
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("info", info))


# Run the bot until the user presses Ctrl-C
# application.run_polling()
