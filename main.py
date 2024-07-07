import logging
import os
from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ConversationHandler, 
    CallbackQueryHandler, ContextTypes, filters
)
from functools import wraps
import database_management
from datetime import datetime


BOT_TOKEN: Final = "7378006253:AAEZ_n9VQ3x3uLxG2uNzxIL2Ikc9rkj9cHc"
# Logging setup
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Admin user IDs
LIST_OF_ADMINS = [44557320]  # Consider moving this to a configuration file

#Stages
ADD_TRADE_ROUTE, PRE_TRADE_ROUTE = range(2)
# Conversation states
INIT, DATE, TIME, TICKER, WIN_LOSS, SIDE, RR, PNL, STRATEGY, PHOTO, SAVE = range(11)

def restricted(func):
    """
    Decorator to restrict access to certain functions to admin users only.
    """
    @wraps(func)
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            logger.warning(f"Unauthorized access denied for {user_id}.")
            await update.message.reply_text("Access denied")
            return
        return await func(update, context, *args, **kwargs)
    return wrapped

@restricted
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list.

    keyboard = [
        [
            InlineKeyboardButton("Add New Trade", callback_data='add_new_trade'),
            InlineKeyboardButton("Check Previous Trades", callback_data='check_previous_trades'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    await update.message.reply_text("Welcome to trading journal bot. Choose an option:", reply_markup=reply_markup)
    return INIT

async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Add New Trade", callback_data='add_new_trade'),
            InlineKeyboardButton("Check Previous Trades", callback_data='check_previous_trades'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    await query.edit_message_text(text="Welcome to trading journal bot. Choose an option:", reply_markup=reply_markup)
    return INIT


async def new_trade_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Starts the process of adding a new trade.
    """
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("XAUUSD", callback_data='XAUUSD')],
        [InlineKeyboardButton("EURUSD", callback_data='EURUSD')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Please Choose Ticker's Name.", reply_markup=reply_markup)
    return WIN_LOSS

async def win_loss_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the selection of the trade result (Win/Loss).
    """
    query = update.callback_query
    await query.answer()
    
    context.user_data['ticker_name'] = query.data  # Store selected ticker
    
    keyboard = [
        [InlineKeyboardButton("Win", callback_data='Win')],
        [InlineKeyboardButton("Loss", callback_data='Loss')],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Trade Status? (WIN/LOSS).", reply_markup=reply_markup)
    return SIDE

async def side_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the selection of the trade side (Long/Short).
    """
    query = update.callback_query
    await query.answer()
    
    context.user_data['win_loss'] = query.data  # Store win/loss status
    
    keyboard = [
        [InlineKeyboardButton("Long", callback_data='Long')],
        [InlineKeyboardButton("Short", callback_data='Short')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text= "Position Side? (Buy/Sell)", reply_markup=reply_markup)
    return STRATEGY

async def strategy_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the selection of the trading strategy.
    Currently, available strategies are:
    - MTR
    - FF
    - Close NYSE
    - DHL (High/Low previous day) 
    """
    query = update.callback_query
    await query.answer()
    
    context.user_data['side'] = query.data # store trade's side
    
    keyboard = [
        [InlineKeyboardButton("DHL", callback_data='DHL')],
        [InlineKeyboardButton("Close NYSE", callback_data='Close_NYSE')],
        [InlineKeyboardButton("MTR", callback_data='MTR')],
        [InlineKeyboardButton("FF", callback_data="FF")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text= "Trading Setup?", reply_markup=reply_markup)
    return DATE

async def date_handler(update:Update, context:ContextTypes.DEFAULT_TYPE):
    """
    Asks the user for the trade date.
    """
    query = update.callback_query
    await query.answer()

    # Collect Date
    context.user_data['strategy'] = query.data
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Please enter the date of the trade (YYYY-MM-DD):"
    )
    return TIME

async def time_handler(update:Update, context:ContextTypes.DEFAULT_TYPE):
    """
    Asks the user for the trade time.
    """
    # Collect Time
    context.user_data['date'] = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.id,
        text="Time Of Trade?(HH:MM)"
    )
    return RR

async def rr_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Asks the user for the Risk:Reward ratio.
    """
    # Collect RR
    context.user_data['time'] = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.id,
        text="What is Risk:Reward Ration?"
    )
    return PNL


async def pnl_handler(update:Update, context:ContextTypes.DEFAULT_TYPE):
    """
    Asks the user for the PnL (Profit and Loss) of the trade.
    """
    # Collect Total PnL
    context.user_data['rr'] = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.id,
        text="What was PnL?"
    )
    return PHOTO

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Asks the user to send a picture of the trade.
    """
    context.user_data['pnl'] = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.id,
        text="Please Send a Picture of Your Trade."
    )
    return SAVE

async def save_trade_handler(update:Update, context:ContextTypes.DEFAULT_TYPE):
    """
    Saves the trade details to the database.
    """
    context.user_data['photo'] = update.message.photo[-1].file_id
    # Call save_trade function to record data in database
    database_management.save_trade(
        date= context.user_data['date'], 
        time= context.user_data['time'], 
        ticker = context.user_data['ticker_name'],
        win_loss= context.user_data['win_loss'], 
        side= context.user_data['side'], 
        rr= context.user_data['rr'], 
        pnl= context.user_data['pnl'],
        strategy= context.user_data['strategy'], 
        picture= context.user_data['photo'])

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.id,
        text="Recorded Succesfully."
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Cancels the current trade recording process.
    """
    await update.message.reply_text('Trade recording cancelled.')
    logger.info(f"Trade recording cancelled by user {update.effective_user.id}")
    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            INIT: [CallbackQueryHandler(new_trade_handler, pattern='^add_new_trade$')],
            WIN_LOSS: [CallbackQueryHandler(win_loss_handler, pattern='^(XAUUSD|EURUSD)$')],
            SIDE: [CallbackQueryHandler(side_handler, pattern='^(Win|Loss)$')],
            STRATEGY: [CallbackQueryHandler(strategy_handler, pattern='^(Long|Short)$')],
            DATE: [CallbackQueryHandler(date_handler, pattern='^(DHL|Close_NYSE|MTR|FF)$')],
            TIME: [MessageHandler(
                    filters.TEXT & ~filters.COMMAND, time_handler
                )],
            RR: [MessageHandler(
                    filters.TEXT & ~filters.COMMAND, rr_handler
                )],
            PNL: [MessageHandler(
                    filters.TEXT & ~filters.COMMAND, pnl_handler),
                ],
            PHOTO: [MessageHandler(
                    filters.TEXT & ~filters.COMMAND, photo_handler)
                ],
            SAVE: [MessageHandler(
                filters.PHOTO & ~filters.COMMAND, save_trade_handler)
                ]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    application.add_handler(conv_handler)
    logger.info("Bot started")
    application.run_polling()


if __name__ == "__main__":
    main()