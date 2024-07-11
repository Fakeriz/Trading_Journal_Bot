import logging
from typing import Final
from telegram import (
    Update, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup
    )
from telegram.ext import (
    Application, 
    CommandHandler, 
    ConversationHandler, 
    CallbackQueryHandler, 
    MessageHandler, 
    filters, 
    ContextTypes
    )
from functools import wraps
from add_trade import *
from check_trades import *
from database_management import *
from export_data import *
from os import environ
from dotenv import load_dotenv

# Importing BOT_TOKEN
load_dotenv()
BOT_TOKEN : Final = environ["BOT_TOKEN"]

# Settings for bot's logging.
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

LIST_OF_ADMINS = [44557320]

INIT = range(1)

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
            [InlineKeyboardButton("Add New Trade", callback_data='add_new_trade')],
            [InlineKeyboardButton("Check Previous Trades", callback_data='check_previous_trades')],
            [InlineKeyboardButton("Export Data (CSV)", callback_data='export_csv')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to trading journal bot. Choose an option:", reply_markup=reply_markup)
    return INIT

async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    await query.answer()

    keyboard = [
            [InlineKeyboardButton("Add New Trade", callback_data='add_new_trade')],
            [InlineKeyboardButton("Check Previous Trades", callback_data='check_previous_trades')],
            [InlineKeyboardButton("Export Data (CSV)", callback_data='export_csv')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Welcome to trading journal bot. Choose an option:", reply_markup=reply_markup)
    return INIT

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            INIT: [
                CallbackQueryHandler(
                    new_trade_handler, pattern='^add_new_trade$'
                    ),
                CallbackQueryHandler(
                    start_check_trades, pattern='^check_previous_trades$'
                    ),
                CallbackQueryHandler(
                    start_export_to_csv, pattern='^export_csv$'
                    )
            ],
            EXPORT_TICKER: [CallbackQueryHandler(
                export_ticker_selected,
            )],
            EXPORT_PERIOD: [CallbackQueryHandler(
                export_period_selected,
            )],
            WIN_LOSS: [CallbackQueryHandler(
                win_loss_handler, pattern='^(XAUUSD|EURUSD)$'
                )],
            SIDE: [CallbackQueryHandler(
                side_handler, pattern='^(Win|Loss)$'
            )],
            STRATEGY: [CallbackQueryHandler(
                strategy_handler, pattern='^(Long|Short)$'
            )],
            DATE: [CallbackQueryHandler(
                date_handler, pattern='^(DHL|Close_NYSE|MTR|FF)$'
            )],
            TIME: [MessageHandler(
                filters.TEXT & ~filters.COMMAND, time_handler
            )],
            RR: [MessageHandler(
                filters.TEXT & ~filters.COMMAND, rr_handler
            )],
            PNL: [MessageHandler(
                filters.TEXT & ~filters.COMMAND, pnl_handler
            )],
            PHOTO: [MessageHandler(
                filters.TEXT & ~filters.COMMAND, photo_handler
            )],
            SAVE: [MessageHandler(
                filters.PHOTO & ~filters.COMMAND, save_trade_handler
            )],
            CHECK_TRADES: [
                CallbackQueryHandler(
                    check_trade_by_date_range_handler, pattern='^date_range$'
                ),
                CallbackQueryHandler(
                    check_trade_by_id_handler, pattern='^specific_trade$'
                ),
                CallbackQueryHandler(
                    check_trades_by_ticker_handler, pattern='^ticker$'
                ),
                CallbackQueryHandler(
                    check_trades_by_side_handler, pattern='^trade_side$'
                ),
                CallbackQueryHandler(
                    check_trades_by_status_handler, pattern='^trade_status$'
                ),
            ],
            DATE_RANGE : [MessageHandler(
                filters.TEXT & ~filters.COMMAND, handle_date_range_input
                )],
            SPECIFIC_TRADE: [MessageHandler(
                filters.TEXT & ~filters.COMMAND, handle_trades_by_id_input
                )],
            TICKER_NAME : [MessageHandler(
                filters.TEXT & ~filters.COMMAND, handle_trades_by_ticker_input
                )],
            SEARCH_SIDE : [CallbackQueryHandler(
                    handle_trades_by_side_input, pattern="^Long|Short$"
                )],
            SEARCH_STATUS: [CallbackQueryHandler(
                handle_trades_by_status_input, pattern="^Win|Loss$"
            )],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    application.add_handler(conv_handler)
    logger.info("Bot Started...")
    application.run_polling()


if __name__ == "__main__":
    main()