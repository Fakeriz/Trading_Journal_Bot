import logging
from typing import Final
from telegram import (
                    Update,
                    ReplyKeyboardMarkup,
                    ReplyKeyboardRemove
                    )

from telegram.ext import (
                        ApplicationBuilder, 
                        ContextTypes, 
                        CommandHandler, 
                        MessageHandler, 
                        ConversationHandler,
                        filters,
                        CallbackContext)
from functools import wraps
from database_management import *

# Bot Token
BOT_TOKEN : Final = "7378006253:AAEZ_n9VQ3x3uLxG2uNzxIL2Ikc9rkj9cHc"

# Enable Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# User Ids whom can access to the bot
LIST_OF_ADMINS = [44557320]


# Decorator to limit access to bot.
def restricted(func):
    ''' This is a decorator that will limit access to the bot
        to only users in LIST_OF_ADMINS variable.
    '''

    @wraps(func)
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            print(f"Unauthorized access denied for {user_id}.")
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Access denied")
            return
        return await func(update, context, *args, **kwargs)
    return wrapped

# Telegram Bot's Handler
DATE, TIME, WIN_LOSS, SIDE, RR, PNL, STRATEGY, PICTURE = range(8) # To handle telegram bot state
trade_records = [] # To record trades

# Handlers
# Start handler
async def start_handler(update: Update, context:ContextTypes.DEFAULT_TYPE):
    text = """
        Welcome to trading journal bot.\nPlease send your trade information with below order:
        1.Date
        2.Time
        3.Win/Loss
        4.Side(Long/Short)
        5.RR
        6.PNL
        7.Strategy
        
        Please enter the Date (YYYY-MM-DD):
        """
    try:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.effective_message.id,
            text=text
        )
    except Exception as e:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"An error occurred: {str(e)}",
            reply_to_message_id=update.effective_message.id,
        )

    return DATE

async def date_handler(update:Update, context:ContextTypes.DEFAULT_TYPE):
    try:
        # Collect Date
        context.user_data['date'] = update.message.text
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.effective_message.id,
            text="Now please send Trade's Time (HH:MM)."
        )
    except Exception as e:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"An error occurred: {str(e)}",
            reply_to_message_id=update.effective_message.id,
        )
    return TIME

async def time_handler(update:Update, context:ContextTypes.DEFAULT_TYPE):
    try:
        # Collect Time
        context.user_data['time'] = update.message.text
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.effective_message.id,
            text="Now Please send Position's Status(Win/Loss)."
        )
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"An error occurred: {str(e)}",
            reply_to_message_id=update.effective_message.id,
        )
    return WIN_LOSS

async def win_loss_trade_handler(update:Update, context:ContextTypes.DEFAULT_TYPE):
    try:
        # Collect Win/Loss
        context.user_data['win_loss'] = update.message.text
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.effective_message.id,
            text="Now Please send Trade's Side."
        )
    except Exception as e:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"An error occurred: {str(e)}",
            reply_to_message_id=update.effective_message.id,
        )
    return SIDE

async def side_handler(update:Update, context:ContextTypes.DEFAULT_TYPE):
    try:
        # Collect Side
        context.user_data['side'] = update.message.text
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.effective_message.id,
            text="Now Please send Trade's RR."
        )
    except Exception as e:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"An error occurred: {str(e)}",
            reply_to_message_id=update.effective_message.id,
        )
    return RR

async def RR_handler(update:Update, context:ContextTypes.DEFAULT_TYPE):
    try:
        # Collect RR
        context.user_data['rr'] = update.message.text
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.effective_message.id,
            text="Now Please send Trade's PNL."
        )
    except Exception as e:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"An error occurred: {str(e)}",
            reply_to_message_id=update.effective_message.id,
        )
    return PNL


async def PNL_handler(update:Update, context:ContextTypes.DEFAULT_TYPE):
    try:
        # Collect Total PnL
        context.user_data['pnl'] = update.message.text
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.effective_message.id,
            text="Now Please send Trade's Strategy."
        )
    except Exception as e:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"An error occurred: {str(e)}",
            reply_to_message_id=update.effective_message.id,
        )
    return STRATEGY

async def strategy_handler(update:Update, context:ContextTypes.DEFAULT_TYPE):
    try:
        # Collect Strategy
        context.user_data['strategy'] = update.message.text
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.effective_message.id,
            text="Trade has been successfully recorded."
        )

        trade = {
            'date': context.user_data['date'],
            'time': context.user_data['time'],
            'win_loss': context.user_data['win_loss'],
            'side': context.user_data['side'],
            'rr': context.user_data['rr'],
            'pnl': context.user_data['pnl'],
            'strategy': context.user_data['strategy']
        }
        # Calling save_trade function from database_management
        save_trade(trade)
    except Exception as e:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"An error occurred: {str(e)}",
            reply_to_message_id=update.effective_message.id,
        )
    return ConversationHandler.END

# Cancel conversation
def cancel_handler(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Trade recording cancelled.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler("start", start_handler)],
            states={
            DATE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, date_handler
                )
            ],
            TIME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, time_handler
                )
            ],
            WIN_LOSS: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, win_loss_trade_handler
                )
            ],
            SIDE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, side_handler
                )
            ],
            RR: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, RR_handler
                )
            ],
            PNL: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, PNL_handler
                )
            ],
            STRATEGY: [
                MessageHandler(
                    filters.TEXT & filters.COMMAND, strategy_handler
                )
            ],
            },
            fallbacks=[
                CommandHandler("cancel", cancel_handler),
            ],
            allow_reentry=True,
        )
    )
    # Running Bot
    app.run_polling()
