from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, ContextTypes

import database.database_management as database_management
from configs.bot_management import *
from datetime import datetime, timedelta
import pandas as pd
from io import BytesIO




# Define states
EXPORT_TICKER, EXPORT_PERIOD, CUSTOM_DATE_RANGE, CUSTOM_TICKER = range(17, 21)

# Handlers for exporting data
async def export_data_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("1 Day", callback_data='1D')],
        [InlineKeyboardButton("2 Days", callback_data='2D')],
        [InlineKeyboardButton("3 Days", callback_data='3D')],
        [InlineKeyboardButton("1 Week", callback_data='1W')],
        [InlineKeyboardButton("2 Weeks", callback_data='2W')],
        [InlineKeyboardButton("1 Month", callback_data='1M')],
        [InlineKeyboardButton("2 Months", callback_data='2M')],
        [InlineKeyboardButton("3 Months", callback_data='3M')],
        [InlineKeyboardButton("6 Months", callback_data='6M')],
        [InlineKeyboardButton("Custom Date Range", callback_data='custom')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Please choose the date period for export:",
        reply_markup=reply_markup
    )
    return EXPORT_PERIOD

async def export_data_period_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    period = query.data
    context.user_data['period'] = period

    await query.answer()

    if period == 'custom':
        await query.message.reply_text("Please enter the custom date range (YYYY-MM-DD to YYYY-MM-DD):")
        return CUSTOM_DATE_RANGE

    # Ask for ticker or choose to export all trades
    keyboard = [
        [InlineKeyboardButton("All Trades", callback_data='all_trades')],
        [InlineKeyboardButton("Choose Ticker", callback_data='choose_ticker')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Do you want to export trades for a specific ticker or all trades?", reply_markup=reply_markup)
    return EXPORT_TICKER

async def export_ticker_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    ticker = query.data

    if ticker == 'choose_ticker':
        await query.message.reply_text("Please enter the ticker name (e.g., XAUUSD):")
        return CUSTOM_TICKER
    else:
        # Handle the 'all_trades' option
        period = context.user_data['period']
        start_date, end_date = get_date_range_from_period(period)
        trades = database_management.get_trades_for_export(None, period, start_date=start_date, end_date=end_date)
        await export_to_csv(update, context, trades, 'all_trades', period)
        await query.message.reply_text("Data exported successfully.")
        return ConversationHandler.END

async def handle_custom_ticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ticker = update.message.text
    period = context.user_data['period']
    start_date, end_date = get_date_range_from_period(period)
    
    trades = database_management.get_trades_for_export(ticker, period, start_date=start_date, end_date=end_date)
    await export_to_csv(update, context, trades, ticker, period)
    await update.message.reply_text("Data exported successfully.")
    return ConversationHandler.END

async def handle_custom_date_range(update: Update, context: ContextTypes.DEFAULT_TYPE):
    date_range = update.message.text
    try:
        start_date_str, end_date_str = date_range.split(" to ")
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        period = context.user_data['period']
        ticker = context.user_data.get('ticker', None)
        trades = database_management.get_trades_for_export(ticker, period, start_date=start_date, end_date=end_date)
        await export_to_csv(update, context, trades, ticker if ticker else 'all_trades', period)
        await update.message.reply_text("Data exported successfully.")
    except ValueError:
        await update.message.reply_text("Invalid date range format. Please use YYYY-MM-DD to YYYY-MM-DD.")
    return ConversationHandler.END

def get_date_range_from_period(period):
    end_date = datetime.now()
    if period == '1D':
        start_date = end_date - timedelta(days=1)
    elif period == '2D':
        start_date = end_date - timedelta(days=2)
    elif period == '3D':
        start_date = end_date - timedelta(days=3)
    elif period == '1W':
        start_date = end_date - timedelta(weeks=1)
    elif period == '2W':
        start_date = end_date - timedelta(weeks=2)
    elif period == '1M':
        start_date = end_date - timedelta(days=30)
    elif period == '2M':
        start_date = end_date - timedelta(days=60)
    elif period == '3M':
        start_date = end_date - timedelta(days=90)
    elif period == '6M':
        start_date = end_date - timedelta(days=180)
    else:
        start_date = None  # Custom date range will be handled separately

    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

async def export_to_csv(update: Update, context: ContextTypes.DEFAULT_TYPE, trades, filename_prefix, period):
    if not trades:
        await update.message.reply_text("No trades found for the selected criteria.")
        return

    df = pd.DataFrame(trades)
    if df.empty:
        await update.message.reply_text("No trades found for the selected criteria.")
        return

    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document=csv_buffer,
        filename=f'{filename_prefix}_{period}.csv'
    )
