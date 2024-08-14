from telegram.ext import (
    Application, 
    CommandHandler, 
    ConversationHandler, 
    CallbackQueryHandler, 
    MessageHandler, 
    filters, 
    )
from utils.bot_management import logger, BOT_TOKEN, start
from utils.states_manager import *
from bot_handlers.add_trade import *
from bot_handlers.check_trades import *
from bot_handlers.update_handler import *
from database.database_management import *
from bot_handlers.export_data import *


def main():
    """
    Main function to run the Telegram bot. Sets up the conversation handler with different states and handlers.
    """

    # Create the application with the bot token
    application = Application.builder().token(BOT_TOKEN).build()

    # Define the conversation handler with different states and their respective handlers
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            TradeStates.INIT: [
                CallbackQueryHandler(new_trade_handler, pattern='^add_new_trade$'),
                CallbackQueryHandler(check_previous_trades_handler, pattern='^check_previous_trades$'),
                CallbackQueryHandler(export_data_handler, pattern='^export_csv$'),
                CallbackQueryHandler(start_update_trade, pattern='^update_trade$')
            ],
            TradeStates.WIN_LOSS: [
                CallbackQueryHandler(win_loss_handler) #, pattern='^(XAUUSD|EURUSD)$'
            ],
            TradeStates.SIDE: [
                CallbackQueryHandler(side_handler, pattern='^(Win|Loss)$')
            ],
            TradeStates.STRATEGY: [
                CallbackQueryHandler(strategy_handler, pattern='^(Long|Short)$')
            ],
            TradeStates.RR: [
                CallbackQueryHandler(rr_handler, pattern='^(DHL|Close_NYSE|MTR|FF)$'),
                MessageHandler(filters.TEXT & ~filters.COMMAND, rr_handler)
            ],
            TradeStates.PNL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, pnl_handler)
            ],
            TradeStates.DATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, date_handler)
            ],
            TradeStates.TIME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, time_handler)
            ],
            TradeStates.PHOTO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, photo_handler)
            ],
            TradeStates.SAVE: [
                MessageHandler(filters.PHOTO & ~filters.COMMAND, save_trade_handler)
            ],
            CheckTradesStates.CHECK_TRADES:[
                CallbackQueryHandler(check_by_date_range_handler, pattern='^by_date_range$'),
                CallbackQueryHandler(check_by_trade_id_handler, pattern='^by_trade_id$'),
                CallbackQueryHandler(check_by_ticker_name_handler, pattern='^by_ticker_name$'),
                CallbackQueryHandler(check_by_side_handler, pattern='^by_side$'),
                CallbackQueryHandler(check_by_status_handler, pattern='^by_status$')
            ],
            CheckTradesStates.CHECK_DATE_RANGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, date_range_handler)
            ],
            CheckTradesStates.CHECK_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, trade_id_handler)
            ],
            CheckTradesStates.CHECK_TICKER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ticker_name_handler)
            ],
            CheckTradesStates.CHECK_SIDE: [
                CallbackQueryHandler(side_selection_handler, pattern='^(Long|Short)$')
            ],
            CheckTradesStates.CHECK_STATUS: [
                CallbackQueryHandler(status_selection_handler, pattern='^(Win|Loss)$')
            ],
            ExportStates.EXPORT_PERIOD: [
                CallbackQueryHandler(export_data_period_handler, pattern='^(1D|2D|3D|1W|2W|1M|2M|3M|6M|custom)$')
            ],
            ExportStates.EXPORT_TICKER: [
                CallbackQueryHandler(export_ticker_handler, pattern='^(all_trades|choose_ticker)$')
            ],
            ExportStates.CUSTOM_DATE_RANGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_date_range)
            ],
            ExportStates.CUSTOM_TICKER: [
                CallbackQueryHandler(handle_custom_ticker)
            ],
            UpdateTradesState.UPDATE_CHOICE: [
                CallbackQueryHandler(start_update_trade_by_id, pattern='^update_trade_by_id$'),
                CallbackQueryHandler(start_remove_trade, pattern='^remove_trade$'),
                CallbackQueryHandler(start_remove_whole_trades, pattern='^remove_all_data$'),
            ],
            UpdateTradesState.TRADE_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, update_trade_by_id_handler),
                MessageHandler(filters.TEXT & ~filters.COMMAND, remove_trade_by_id_handler),
            ],
            UpdateTradesState.UPDATE_FIELD_CHOICE: [
                CallbackQueryHandler(update_field_choice_handler, pattern='^update_(ticker|status|side|strategy)$'),
            ],
            UpdateTradesState.UPDATE_TICKER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, update_ticker_handler),
            ],
            UpdateTradesState.UPDATE_STATUS: [
                CallbackQueryHandler(update_status_handler, pattern='^update_status_(Win|Loss)$'),
            ],
            UpdateTradesState.UPDATE_SIDE: [
                CallbackQueryHandler(update_side_handler, pattern='^update_side_(Long|Short)$'),
            ],
            UpdateTradesState.UPDATE_STRATEGY: [
                CallbackQueryHandler(update_strategy_handler, pattern='^update_strategy_(DHL|Close_NYSE|MTR|FF)$'),
            ],
            UpdateTradesState.REMOVE_TRADE_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, remove_trade_by_id_handler)
            ],
            UpdateTradesState.REMOVE_ALL_DATA: [
                CallbackQueryHandler(remove_whole_database, pattern='^confirm_remove_all_data$')
            ],
    
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    # Add the conversation handler to the application
    application.add_handler(conv_handler)
    
    # Log that the bot has started
    logger.info("Bot Started...")

    # Start polling for updates
    application.run_polling()

if __name__ == "__main__":
    main()