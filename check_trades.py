import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import database_management

logger = logging.getLogger(__name__)

CHECK_TRADES, DATE_RANGE, SPECIFIC_TRADE, TICKER_NAME, SIDE, STATUS = range(6)

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

async def handle_date_range_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle user input for date range and fetch trades within that range.

    This function expects the user to input a date range in 
        the format 'YYYY-MM-DD to YYYY-MM-DD'.
    It fetches the trades from the database that fall within
        this range and displays them to the user.
    """
    
    # Extract and strip the date range from the user's message
    date_range = update.message.text.strip()
    try:
        # Split the date range into start and end dates
        start_date, end_date = date_range.split(" to ")
    except ValueError:
        # Notify the user if the date range format is invalid
        await update.message.reply_text("Invalid format. Please enter the date range as 'YYYY-MM-DD to YYYY-MM-DD'.")
        return DATE_RANGE

    # Fetch trades from database by usding database_management module
    trades = database_management.get_trades_by_date_range(start_date, end_date)
    
    # Notify the user if no trades are found for the specified date range
    if not trades:
        await update.message.reply_text("No trades found for the specified date range.")
        return ConversationHandler.END
    
    # Iterate through the fetched trades and display each one to the user
    for trade in trades:
        caption = (
                f"ID: {trade['id']}\n"
                f"Date: {trade['date']}\n"
                f"Time: {trade['time']}\n"
                f"Ticker: {trade['ticker']}\n"
                f"Side: {trade['side']}\n"
                f"Status: {trade['status']}\n"
                f"PnL: {trade['pnl']}\n"
                f"RR: {trade['rr']}\n"
                f"Strategy: {trade['strategy']}"
            )
        # If statement for those record without picture
        if trade['picture']:
            await update.message.reply_photo(photo=trade['picture'], caption=caption)
        else:
            await update.message.reply_text(text=caption)
    return ConversationHandler.END


async def check_trade_by_id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Please enter trade's unique ID.")
    return SPECIFIC_TRADE

async def check_trades_by_ticker_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Checking previous trades by ticker's name
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text= "Please provide ticker's name.")
    return TICKER_NAME

async def check_trades_by_side_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Checking previous trades by trade's side (Buy/Sell)
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Please send position's side (Long/Short).")
    return SIDE

async def check_trades_by_status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Checking previous trades by trade's status (Win/Loss)
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Please send trade's status (Win/Loss).")
    return STATUS