from add_trade import *
from check_trades import *
from database_management import *


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            INIT: [
                    CallbackQueryHandler(new_trade_handler, pattern='^add_new_trade$'),
                    ],
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
