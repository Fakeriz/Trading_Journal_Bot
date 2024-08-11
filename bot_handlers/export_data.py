from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, ContextTypes

from database.database_management import TradeDatabase
from utils.bot_management import return_to_main_menu
from utils.states_manager import ExportStates
from datetime import datetime, timedelta
import pandas as pd
from io import BytesIO



# Define states
# EXPORT_TICKER, EXPORT_PERIOD, CUSTOM_DATE_RANGE, CUSTOM_TICKER = range(17, 21)

# Creating TradeDatabase instance
trades_db = TradeDatabase()


async def export_data_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the initial export data request by providing options for the date period.
    
    Args:
        update (Update): The update object that contains the callback query.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.
    
    Returns:
        int: The next state in the conversation (EXPORT_PERIOD).
    """
    query = update.callback_query
    await query.answer()

    # Create a keyboard with options for the date period
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

    # Ask the user to choose the date period for export
    await query.edit_message_text(
        text="Please choose the date period for export:",
        reply_markup=reply_markup
    )
    return ExportStates.EXPORT_PERIOD


async def export_data_period_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the user's selection of the date period and asks for further criteria (ticker).
    
    Args:
        update (Update): The update object that contains the callback query.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.
    
    Returns:
        int: The next state in the conversation (EXPORT_TICKER or CUSTOM_DATE_RANGE).
    """
    query = update.callback_query
    period = query.data
    context.user_data['period'] = period

    await query.answer()

    if period == 'custom':
        # Ask the user to enter a custom date range
        await query.message.reply_text("Please enter the custom date range (YYYY-MM-DD to YYYY-MM-DD):")
        return ExportStates.CUSTOM_DATE_RANGE

    # Ask for ticker or choose to export all trades
    keyboard = [
        [InlineKeyboardButton("All Trades", callback_data='all_trades')],
        [InlineKeyboardButton("Choose Ticker", callback_data='choose_ticker')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Do you want to export trades for a specific ticker or all trades?", reply_markup=reply_markup)
    return ExportStates.EXPORT_TICKER


async def export_ticker_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the user's selection of exporting all trades or a specific ticker.
    
    Args:
        update (Update): The update object that contains the callback query.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.
    
    Returns:
        int: The next state in the conversation (CUSTOM_TICKER or ConversationHandler.END).
    """
    query = update.callback_query
    await query.answer()

    ticker = query.data

    if ticker == 'choose_ticker':
        # Ask the user to enter the ticker name
        await query.message.reply_text("Please enter the ticker name (e.g., XAUUSD):")
        return ExportStates.CUSTOM_TICKER
    else:
        # Handle the 'all_trades' option
        period = context.user_data['period']
        start_date, end_date = get_date_range_from_period(period)
        trades = trades_db.get_trades_for_export(None, period, start_date=start_date, end_date=end_date)
        await export_to_csv(update, context, trades, 'all_trades', period)
        await query.message.reply_text("Data exported successfully.")
        return await return_to_main_menu(update, context)


async def handle_custom_ticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the user's input for the ticker name and retrieves the trades for export.
    
    Args:
        update (Update): The update object that contains the user's message.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.
    
    Returns:
        int: Ends the conversation.
    """
    ticker = update.message.text
    period = context.user_data['period']
    start_date, end_date = get_date_range_from_period(period)
    
    trades = trades_db.get_trades_for_export(ticker, period, start_date=start_date, end_date=end_date)
    await export_to_csv(update, context, trades, ticker, period)
    await update.message.reply_text("Data exported successfully.")
    return await  return_to_main_menu(update, context)


async def handle_custom_date_range(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the user's input for the custom date range and retrieves the trades for export.
    
    Args:
        update (Update): The update object that contains the user's message.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.
    
    Returns:
        int: Ends the conversation.
    """
    date_range = update.message.text
    try:
        start_date_str, end_date_str = date_range.split(" to ")
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        period = context.user_data['period']
        ticker = context.user_data.get('ticker', None)
        trades = trades_db.get_trades_for_export(ticker, period, start_date=start_date, end_date=end_date)
        await export_to_csv(update, context, trades, ticker if ticker else 'all_trades', period)
        await update.message.reply_text("Data exported successfully.")
    except ValueError:
        await update.message.reply_text("Invalid date range format. Please use YYYY-MM-DD to YYYY-MM-DD.")
    return await  return_to_main_menu(update, context)


def get_date_range_from_period(period):
    """
    Converts a given period into a start and end date range.
    
    Args:
        period (str): The period string (e.g., '1D', '1W', '1M', etc.).
    
    Returns:
        tuple: A tuple containing the start and end dates as strings.
    """

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
    """
    Exports the trades to a CSV file and sends it to the user.
    
    Args:
        update (Update): The update object that contains the user's message.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.
        trades (list): The list of trades to be exported.
        filename_prefix (str): The prefix for the filename.
        period (str): The period for the export.
    """
    if not trades:
        # Inform the user if no trades are found
        await update.message.reply_text("No trades found for the selected criteria.")
        return

    # Convert trades to a DataFrame and then to CSV
    df = pd.DataFrame(trades)

    # If the dataframe is empy then inform the user.
    if df.empty:
        await update.message.reply_text("No trades found for the selected criteria.")
        return
    
    # Add columns header to dataframe
    cols = ['ID', 'Date', 'Time', 'Ticker', 'Status', 'Side', 'R:R Ratio', 'PnL', 'Strategy', 'Photo']
    if not all(col in df.columns for col in cols):
        df.columns = cols

    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    # Send the CSV file to the user
    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document=csv_buffer,
        filename=f'{filename_prefix}_{period}.csv'
    )
