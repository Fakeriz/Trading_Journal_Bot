from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from database.database_management import TradeDatabase
from utils.states_manager import UpdateTradesState
from utils.bot_management import return_to_main_menu



async def start_update_trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Update a Trade", callback_data="update_trade")],
        [InlineKeyboardButton("Remove a Trade", callback_data='remove_trade')],
        [InlineKeyboardButton("Remove Whole Database",callback_data='remove_all_data')]
    ]

    repyly_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text = "What Would You Like To Do?",
        reply_markup=repyly_markup
    )
    return UpdateTradesState.UPDATE_CHOICE

async def start_update_trade_by_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Prompts the user to enter the Trade ID they want to update.
    
    Args:
        update (Update): The update object that contains the callback query.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.
    
    Returns:
        int: The next state in the conversation (TRADE_ID).
    """
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

async def start_remove_trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text("Please enter the Trade ID you want to remove:")
    return UpdateTradesState.REMOVE_TRADE_ID

async def remove_trade_by_id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    trade_id = update.message.text
    trades_db = TradeDatabase()

    try:
        trade = trades_db.get_trade_by_id(trade_id)
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")
        return UpdateTradesState.REMOVE_TRADE_ID

    if trade:
        try:
            trades_db.remove_trade_by_id(trade_id)
            await update.message.reply_text(f"Trade with ID {trade_id} has been removed.")
        except Exception as e:
            await update.message.reply_text(f"An error occurred: {e}")
    else:
        await update.message.reply_text("Trade ID not found. Please enter a valid Trade ID:")
        return UpdateTradesState.REMOVE_TRADE_ID

    return await return_to_main_menu(update, context)

async def start_remove_whole_trades(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Confirm", callback_data='confirm_remove_all_data')],
        [InlineKeyboardButton("Cancel", callback_data='cancel_remove_all_data')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(
        text="Are you sure you want to remove the whole database?",
        reply_markup=reply_markup
    )
    return UpdateTradesState.REMOVE_ALL_DATA

async def remove_whole_database(update: Update, context: ContextTypes.DEFAULT_TYPE):
    trades_db = TradeDatabase()

    try:
        trades_db.remove_all_trades()
        await update.callback_query.message.reply_text("The whole database has been removed.")
    except Exception as e:
        await update.callback_query.message.reply_text(f"An error occurred: {e}")

    return await return_to_main_menu(update, context)
