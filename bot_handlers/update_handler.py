from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from database.database_management import TradeDatabase
from utils.states_manager import UpdateTradesState
from utils.bot_management import return_to_main_menu



async def start_update_trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text("Please enter the Trade ID you want to update:")
    return UpdateTradesState.TRADE_ID

async def update_trade_by_id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    trade_id = update.message.text
    trades_db = TradeDatabase()

    try:
        trade = trades_db.get_trade_by_id(trade_id)
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")
        return UpdateTradesState.TRADE_ID

    if trade:
        context.user_data['trade_id'] = trade_id
        await update.message.reply_text(
            "Trade found, What would you like to update?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Ticker", callback_data='update_ticker')],
                [InlineKeyboardButton("Status", callback_data='update_status')],
                [InlineKeyboardButton("Side", callback_data='update_side')],
                [InlineKeyboardButton("Strategy", callback_data='update_strategy')],
                [InlineKeyboardButton("Cancel", callback_data='cancel_update')]
            ])
        )
        return UpdateTradesState.UPDATE_CHOICE
    else:
        await update.message.reply_text("Trade ID not found. Please enter a valid Trade ID:")
        return UpdateTradesState.TRADE_ID

async def update_trade_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    options = {
        'update_ticker': ("Please select the new Ticker:", [
            [InlineKeyboardButton("XAUUSD", callback_data='XAUUSD')],
            [InlineKeyboardButton("EURUSD", callback_data='EURUSD')],
            [InlineKeyboardButton("Back", callback_data='back_to_update_choice')]
        ]),
        'update_status': ("Please select the new Status:", [
            [InlineKeyboardButton("Win", callback_data='Win')],
            [InlineKeyboardButton("Loss", callback_data='Loss')],
            [InlineKeyboardButton("Back", callback_data='back_to_update_choice')]
        ]),
        'update_side': ("Please select new Side:", [
            [InlineKeyboardButton("Long", callback_data='Long')],
            [InlineKeyboardButton("Short", callback_data='Short')],
            [InlineKeyboardButton("Back", callback_data='back_to_update_choice')]
        ]),
        'update_strategy': ("Please select new Strategy:", [
            [InlineKeyboardButton("DHL", callback_data='DHL')],
            [InlineKeyboardButton("Close NYSE", callback_data='Close_NYSE')],
            [InlineKeyboardButton("MTR", callback_data='MTR')],
            [InlineKeyboardButton("FF", callback_data="FF")],
            [InlineKeyboardButton("Back", callback_data='back_to_update_choice')]
        ])
    }

    if query.data in options:
        message, buttons = options[query.data]
        await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(buttons))
        return UpdateTradesState[query.data.upper().replace('UPDATE_', 'UPDATE_')]

async def update_ticker_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'back_to_update_choice':
        await query.edit_message_text("What would you like to update?",
                                      reply_markup=InlineKeyboardMarkup([
                                          [InlineKeyboardButton("Ticker", callback_data='update_ticker')],
                                          [InlineKeyboardButton("Status", callback_data='update_status')],
                                          [InlineKeyboardButton("Side", callback_data='update_side')],
                                          [InlineKeyboardButton("Strategy", callback_data='update_strategy')],
                                          [InlineKeyboardButton("Cancel", callback_data='cancel_update')]
                                      ]))
        return UpdateTradesState.UPDATE_CHOICE

    trade_id = context.user_data['trade_id']
    trades_db = TradeDatabase()
    trades_db.update_trade(trade_id, {'ticker': query.data})
    await query.edit_message_text(f"Ticker updated to {query.data}")
    return ConversationHandler.END

async def update_status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'back_to_update_choice':
        await query.edit_message_text("What would you like to update?",
                                      reply_markup=InlineKeyboardMarkup([
                                          [InlineKeyboardButton("Ticker", callback_data='update_ticker')],
                                          [InlineKeyboardButton("Status", callback_data='update_status')],
                                          [InlineKeyboardButton("Side", callback_data='update_side')],
                                          [InlineKeyboardButton("Strategy", callback_data='update_strategy')],
                                          [InlineKeyboardButton("Cancel", callback_data='cancel_update')]
                                      ]))
        return UpdateTradesState.UPDATE_CHOICE

    trade_id = context.user_data['trade_id']
    trades_db = TradeDatabase()
    trades_db.update_trade(trade_id, {'status': query.data})
    await query.edit_message_text(f"Status updated to {query.data}")
    return await return_to_main_menu(update, context)

async def update_side_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'back_to_update_choice':
        await query.edit_message_text("What would you like to update?",
                                      reply_markup=InlineKeyboardMarkup([
                                          [InlineKeyboardButton("Ticker", callback_data='update_ticker')],
                                          [InlineKeyboardButton("Status", callback_data='update_status')],
                                          [InlineKeyboardButton("Side", callback_data='update_side')],
                                          [InlineKeyboardButton("Strategy", callback_data='update_strategy')],
                                          [InlineKeyboardButton("Cancel", callback_data='cancel_update')]
                                      ]))
        return UpdateTradesState.UPDATE_CHOICE

    trade_id = context.user_data['trade_id']
    trades_db = TradeDatabase()
    trades_db.update_trade(trade_id, {'side': query.data})
    await query.edit_message_text(f"Side updated to {query.data}")
    return await return_to_main_menu(update, context)

async def update_strategy_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'back_to_update_choice':
        await query.edit_message_text("What would you like to update?",
                                      reply_markup=InlineKeyboardMarkup([
                                          [InlineKeyboardButton("Ticker", callback_data='update_ticker')],
                                          [InlineKeyboardButton("Status", callback_data='update_status')],
                                          [InlineKeyboardButton("Side", callback_data='update_side')],
                                          [InlineKeyboardButton("Strategy", callback_data='update_strategy')],
                                          [InlineKeyboardButton("Cancel", callback_data='cancel_update')]
                                      ]))
        return UpdateTradesState.UPDATE_CHOICE

    trade_id = context.user_data['trade_id']
    trades_db = TradeDatabase()
    trades_db.update_trade(trade_id, {'strategy': query.data})
    await query.edit_message_text(f"Strategy updated to {query.data}")
    return await return_to_main_menu(update, context)

async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Update cancelled.")
    return await return_to_main_menu(update, context)
