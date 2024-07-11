import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import database_management
import csv
import io
from datetime import datetime, timedelta
from main import INIT


logger = logging.getLogger(__name__)

EXPORT_TICKER, EXPORT_PERIOD = range(2)


async def start_export_to_csv(update: Update, conext: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Fetch available tickers from the database
    tickers = database_management.get_all_tickers()
    if not tickers:
        await query.edit_message_text(
            text = 'No tickers found.',
        )
        return INIT

    keyboard = [[InlineKeyboardButton(ticker, callback_data=ticker)] for ticker in tickers]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Please select the ticker:", reply_markup=reply_markup)
    return EXPORT_TICKER


async def export_ticker_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the ticker selection and prompts the user to select an export period.

    Args:
        update (Update): Incoming Telegram update.
        context (ContextTypes.DEFAULT_TYPE): Context of the Telegram update.

    Returns:
        int: The next state in the conversation (EXPORT_PERIOD).
    """
    
    query = update.callback_query
    await query.answer()

    # Store the selected ticker in user data
    context.user_data['selected_ticker'] = query.data

    # Create an InlineKeyboard with periods
    keyboard = [
        [InlineKeyboardButton("1D", callback_data='1D')],
        [InlineKeyboardButton("3D", callback_data='3D')],
        [InlineKeyboardButton("1W", callback_data='1W')],
        [InlineKeyboardButton("2W", callback_data='2W')],
        [InlineKeyboardButton("1M", callback_data='1M')],
        [InlineKeyboardButton("3M", callback_data='3M')],
        [InlineKeyboardButton("6M", callback_data='6M')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Prompt user to select a period for export
    await query.edit_message_text("Please select the period for export:", reply_markup=reply_markup)
    return EXPORT_PERIOD

async def export_period_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the period selection, fetches trade data from the database, and exports it to a CSV file.

    Args:
        update (Update): Incoming Telegram update.
        context (ContextTypes.DEFAULT_TYPE): Context of the Telegram update.

    Returns:
        int: The end of the conversation handler (ConversationHandler.END).
    """
    query = update.callback_query
    await query.answer()

    # get selected period & ticker name
    period = query.data
    ticker = context.user_data['selected_ticker']

    # Fetching trades from db based on period and ticker
    trades = database_management.get_trades_for_export(ticker, period)
    if not trades:
        await query.edit_message_text(
            text=f"No trades found for {ticker} within date range {period}"
        )
        return INIT
    
    # Create a CSV file from the fetched trades
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write rows to csv file.
    writer.writerow(['ID', 'Date', 'Time', 'Ticker', 'Side', 'Status', 'PnL', 'RR', 'Strategy'])
    for trade in trades:
        writer.writerow([trade[0], trade[1], trade[2], trade[3], trade[4], trade[5], trade[6], trade[7], trade[8]])
    output.seek(0)
    csv_file = output.getvalue()

    # Send the CSV file to the user
    await query.message.reply_document(document=csv_file.encode('utf-8'), filename=f'{ticker}_trades_{period}.csv')
    return ConversationHandler.END