import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import database_management

logger = logging.getLogger(__name__)

CHECK_TRADES, DATE_RANGE, SPECIFIC_TRADE, TICKER_NAME, SEARCH_SIDE, SEARCH_STATUS = range(6)

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

# CHECK TRADES BY DATE RANGE BUTTON HANDLER AND DB HANDLER
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


# CHECK TRADES BY ID BUTTON HANDLER AND DB HANDLER
async def check_trade_by_id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Prompt the user to enter a trade's unique ID to fetch the trade details.

    Args:
        update (Update): Incoming Telegram update.
        context (ContextTypes.DEFAULT_TYPE): Context of the Telegram update.
    
    Returns:
        int: The next state in the conversation.
    """

    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Please enter trade's unique ID.")
    return SPECIFIC_TRADE

async def handle_trades_by_id_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the input of trade ID, fetch trade details, and send them to the user.

    Args:
        update (Update): Incoming Telegram update.
        context (ContextTypes.DEFAULT_TYPE): Context of the Telegram update.

    Returns:
        int: The end of the conversation handler.
    """

    try:
        trade_id = int(update.message.text.strip())
    except ValueError:
        await update.message.reply_text(text="Wrong ID, please enger an valid number.")
        return SPECIFIC_TRADE
    
    # Fetch trade details from the database by ID
    trades = database_management.get_trades_by_id(trade_id)

    if not trades:
        await update.message.reply_text("No trades found for the specified ID.")
        return ConversationHandler.END
    
    # Ensure trades is a list even if only one trade is found
    if isinstance(trades, dict):
        trades = [trades]

    # Send trade details to the user
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


# CHECK TRADES BY TICKER NAME - BUTTON HANDLER AND DB HANDLER
async def check_trades_by_ticker_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Prompt the user to enter a ticker name to fetch trades associated with that ticker.

    Args:
        update (Update): Incoming Telegram update.
        context (ContextTypes.DEFAULT_TYPE): Context of the Telegram update.
    
    Returns:
        int: The next state in the conversation.
    """

    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text= "Please provide ticker's name.")
    return TICKER_NAME

async def handle_trades_by_ticker_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the input of a ticker name, fetch trades associated with the ticker, and send them to the user.

    Args:
        update (Update): Incoming Telegram update.
        context (ContextTypes.DEFAULT_TYPE): Context of the Telegram update.

    Returns:
        int: The end of the conversation handler.
    """

    try:
        ticker_name = update.message.text.strip()
    except ValueError:
        await update.message.reply_text(text="Please send valid ticker name (e.g XAUUSD)")
        return TICKER_NAME
    
    # Fetch trades from the database by ticker name
    trades = database_management.get_trades_by_ticker(ticker_name)

    if not trades:
        await update.message.reply_text(f"No trades found for the specified ticker name: {ticker_name}.")
        return ConversationHandler.END
    
    # Send trade details to the user
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

        # Send a photo if available, otherwise send text
        if trade['picture']:
            await update.message.reply_photo(photo=trade['picture'], caption=caption)
        else:
            await update.message.reply_text(text=caption)
    return ConversationHandler.END


# CHECK TRADES BY SIDE (LONG/SHORT) - BUTTON HANDLER AND DB HANDLER
async def check_trades_by_side_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Prompt the user to enter the trade's side (Long/Short) to fetch trades based on the side.

    Args:
        update (Update): Incoming Telegram update.
        context (ContextTypes.DEFAULT_TYPE): Context of the Telegram update.
    
    Returns:
        int: The next state in the conversation.
    """

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Long", callback_data="Long")],
        [InlineKeyboardButton("Short", callback_data="Short")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
            text = "Please send position's side (Long/Short).",
            reply_markup = reply_markup)
    return SEARCH_SIDE

async def handle_trades_by_side_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    side = query.data.split('_')[-1].capitalize()

    # Fetch trades from the database by side
    trades = database_management.get_trades_by_side(side)

    if not trades:
        await query.edit_message_text(f"No trades found for the selected side: {side}.")
        return CHECK_TRADES
    
    # Send trade details to the user
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
        if trade['picture']:
            await query.message.reply_photo(photo=trade['picture'], caption=caption)
        else:
            await query.message.reply_text(text=caption)
    return ConversationHandler.END



# CHECK TRADES BY TRADE STATUS (WIN/LOSS) - BUTTON HANDLER AND DB HANDLER
async def check_trades_by_status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Prompt the user to enter the trade's status (Win/Loss) to fetch trades based on the status.

    Args:
        update (Update): Incoming Telegram update.
        context (ContextTypes.DEFAULT_TYPE): Context of the Telegram update.
    
    Returns:
        int: The next state in the conversation.
    """

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Win", callback_data='Win')],
        [InlineKeyboardButton("Loss", callback_data="Loss")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
            text="Please send trade's status (Win/Loss).",
            reply_markup= reply_markup)
    return SEARCH_STATUS

async def handle_trades_by_status_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    status = query.data

    # Fetch trades from the database by side
    trades = database_management.get_trades_by_status(status)

    if not trades:
        await query.edit_message_text("No trades found for the selected status.")
        return CHECK_TRADES
    
    # Send trade details to the user
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
        if trade['picture']:
            await query.message.reply_photo(photo=trade['picture'], caption=caption)
        else:
            await query.message.reply_text(text=caption)
    return ConversationHandler.END
