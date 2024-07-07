import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

logger = logging.getLogger(__name__)

CHECK_TRADES, DATE_RANGE, SPECIFIC_TRADE = range(3)

async def start_check_trades(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the start of the check trades process.
    """
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Date Range", callback_data='date_range')],
        [InlineKeyboardButton("By ID", callback_data='specific_trade')],
        [InlineKeyboardButton("Ticker", callback_data='ticker')],
        [InlineKeyboardButton("Trade's Side", callback_data='trade_side')],
        [InlineKeyboardButton("Trade's Status(Win/Loss)", callback_data='trade_status')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="How would you like to check the trades?", reply_markup=reply_markup)
    return CHECK_TRADES

async def check_trade_by_date_range_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles checking trades by date range.
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Please enter the date range (YYYY-MM-DD to YYYY-MM-DD):")
    return DATE_RANGE

async def check_trade_by_id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Please enter trade's unique ID.")
    return SPECIFIC_TRADE

async def check_trades_by_ticker_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Checking previous trades by ticker's name
    """
    pass

async def check_trades_by_side_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Checking previous trades by trade's side (Buy/Sell)
    """
    pass

async def check_trades_by_status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Checking previous trades by trade's status (Win/Loss)
    """
    pass

