from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, ContextTypes

from configs.bot_management import *
import database.database_management as database_management

async def check_previous_trades_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Provides options to check previous trades
    available optionse are:
    - By Date Range
    - By ID
    - By Ticker Name
    - By Trade's Side
    - by Trade's Status
    """
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("By Date Range", callback_data='by_date_range')],
        [InlineKeyboardButton("By Trade ID", callback_data='by_trade_id')],
        [InlineKeyboardButton('By Ticker Name', callback_data='by_ticker_name')],
        [InlineKeyboardButton("By Side(Long/Short)", callback_data="by_side")],
        [InlineKeyboardButton("By Status(Win/Loss)", callback_data="by_status")]

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="How Would You Like To Check The Trades?",
        reply_markup=reply_markup
    )
    return CHECK_TRADES

async def check_by_date_range_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text="Please enter the date range (YYYY-MM-DD to YYYY-MM-DD):"
    )
    return CHECK_DATE_RANGE

async def check_by_trade_id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="Please enter the trade ID:")
    return CHECK_ID

async def check_by_ticker_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="Please enter the ticker name (e.g., XAUUSD):")
    return CHECK_TICKER

async def check_by_side_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("Long", callback_data='Long')],
        [InlineKeyboardButton("Short", callback_data='Short')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Select the side (Long/Short):",
        reply_markup=reply_markup)
    return CHECK_SIDE

async def check_by_status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("Win", callback_data='Win')],
        [InlineKeyboardButton("Loss", callback_data='Loss')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Select the status (Win/Loss):", 
        reply_markup=reply_markup)
    return CHECK_STATUS

# Collecting user inputs and displaying results
async def display_trades(update: Update, context: ContextTypes.DEFAULT_TYPE, trades):
    """
    Displays the list of trades to the user.
    """
    if not trades:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="No trades found for the given criteria."
        )
    else:
        for trade in trades:
            trade_details = (
                f"Trade ID: {trade['id']}\n"
                f"Date: {trade['date']}\n"
                f"Time: {trade['time']}\n"
                f"Ticker: {trade['ticker']}\n"
                f"Side: {trade['side']}\n"
                f"Status: {trade['status']}\n"
                f"RR: {trade['rr']}\n"
                f"PnL: {trade['pnl']}\n"
                f"Strategy: {trade['strategy']}\n"
            )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=trade_details
            )

async def date_range_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles date range input.
    """
    date_range = update.message.text.split(' to ')
    trades = database_management.get_trades_by_date_range(date_range[0], date_range[1])
    await display_trades(update, context, trades)
    return ConversationHandler.END

async def trade_id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles trade ID input.
    """
    trade_id = update.message.text
    trade = database_management.get_trades_by_id(trade_id)
    await display_trades(update, context, [trade] if trade else [])
    return ConversationHandler.END

async def ticker_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles ticker name input.
    """
    ticker_name = update.message.text
    trades = database_management.get_trades_by_ticker(ticker_name)
    await display_trades(update, context, trades)
    return ConversationHandler.END

async def side_selection_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles side (Long/Short) selection.
    """
    query = update.callback_query
    await query.answer()
    side = query.data
    trades = database_management.get_trades_by_side(side)
    await display_trades(update, context, trades)
    return ConversationHandler.END

async def status_selection_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles status (Win/Loss) selection.
    """
    query = update.callback_query
    await query.answer()
    status = query.data
    trades = database_management.get_trades_by_status(status)
    await display_trades(update, context, trades)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Cancels the current trade recording process.
    """
    await update.message.reply_text('Trade recording cancelled.')
    return ConversationHandler.END
