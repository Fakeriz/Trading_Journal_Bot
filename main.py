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
from configs.bot_management import logger, restricted, BOT_TOKEN
from bot_handlers.add_trade import *
from bot_handlers.check_trades import *
from database.database_management import *
from bot_handlers.export_data import *


@restricted
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    
    keyboard = [
            [InlineKeyboardButton("Add New Trade", callback_data='add_new_trade')],
            [InlineKeyboardButton("Check Previous Trades", callback_data='check_previous_trades')],
            [InlineKeyboardButton("Export Data (CSV)", callback_data='export_csv')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to trading journal bot. Choose an option:", reply_markup=reply_markup)
    return INIT


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            INIT: [
                CallbackQueryHandler(new_trade_handler, pattern='^add_new_trade$'),
                CallbackQueryHandler(check_previous_trades_handler, pattern='^check_previous_trades$'),
                CallbackQueryHandler(export_data_handler, pattern='^export_csv$')
            ],
            WIN_LOSS: [
                CallbackQueryHandler(win_loss_handler, pattern='^(XAUUSD|EURUSD)$')
            ],
            SIDE: [
                CallbackQueryHandler(side_handler, pattern='^(Win|Loss)$')
            ],
            STRATEGY: [
                CallbackQueryHandler(strategy_handler, pattern='^(Long|Short)$')
            ],
            DATE: [
                CallbackQueryHandler(date_handler, pattern='^(DHL|Close_NYSE|MTR|FF)$'),
                MessageHandler(filters.TEXT & ~filters.COMMAND, date_handler)
            ],
            TIME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, time_handler)
            ],
            RR: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, rr_handler)
            ],
            PNL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, pnl_handler)
            ],
            PHOTO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, photo_handler)
            ],
            SAVE: [
                MessageHandler(filters.PHOTO & ~filters.COMMAND, save_trade_handler)
            ],
            CHECK_TRADES:[
                CallbackQueryHandler(check_by_date_range_handler, pattern='^by_date_range$'),
                CallbackQueryHandler(check_by_trade_id_handler, pattern='^by_trade_id$'),
                CallbackQueryHandler(check_by_ticker_name_handler, pattern='^by_ticker_name$'),
                CallbackQueryHandler(check_by_side_handler, pattern='^by_side$'),
                CallbackQueryHandler(check_by_status_handler, pattern='^by_status$')
            ],
            CHECK_DATE_RANGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, date_range_handler)
            ],
            CHECK_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, trade_id_handler)
            ],
            CHECK_TICKER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ticker_name_handler)
            ],
            CHECK_SIDE: [
                CallbackQueryHandler(side_selection_handler, pattern='^(Long|Short)$')
            ],
            CHECK_STATUS: [
                CallbackQueryHandler(status_selection_handler, pattern='^(Win|Loss)$')
            ],
            EXPORT_PERIOD: [
                CallbackQueryHandler(export_data_period_handler, pattern='^(1D|2D|3D|1W|2W|1M|2M|3M|6M|custom)$')
            ],
            EXPORT_TICKER: [
                CallbackQueryHandler(export_ticker_handler, pattern='^(all_trades|choose_ticker)$')
            ],
            CUSTOM_DATE_RANGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_date_range)
            ],
            CUSTOM_TICKER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_ticker)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(conv_handler)
    logger.info("Bot Started...")
    application.run_polling()

if __name__ == "__main__":
    main()
