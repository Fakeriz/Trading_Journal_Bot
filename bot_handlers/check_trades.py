from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, ContextTypes

from utils.bot_management import return_to_main_menu
from utils.states_manager import CheckTradesStates
from database.database_management import TradeDatabase

# Creating TradeDatabase instance
trades_db = TradeDatabase()

async def check_previous_trades_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Provides options to check previous trades
    available optionse are:
    - By Date Range
    - By ID
    - By Ticker Name
    - By Trade's Side
    - by Trade's Status

    Args:
        update (Update): The update object that contains the callback query.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.
    
    Returns:
        int: The next state in the conversation (CHECK_TRADES).
    """
    query = update.callback_query
    await query.answer()

     # Create a keyboard with options for checking trades by different criteria
    keyboard = [
        [InlineKeyboardButton("By Date Range", callback_data='by_date_range')],
        [InlineKeyboardButton("By Trade ID", callback_data='by_trade_id')],
        [InlineKeyboardButton('By Ticker Name', callback_data='by_ticker_name')],
        [InlineKeyboardButton("By Side(Long/Short)", callback_data="by_side")],
        [InlineKeyboardButton("By Status(Win/Loss)", callback_data="by_status")]

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

     # Ask the user how they would like to check the trades
    await query.edit_message_text(
        text="How Would You Like To Check The Trades?",
        reply_markup=reply_markup
    )
    return CheckTradesStates.CHECK_TRADES



async def check_by_date_range_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Prompts the user to enter the date range for checking trades.
    
    Args:
        update (Update): The update object that contains the callback query.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.
    
    Returns:
        int: The next state in the conversation (CHECK_DATE_RANGE).
    """
    query = update.callback_query
    await query.answer()

    # Ask the user to enter the date range
    await query.edit_message_text(
        text="Please enter the date range (YYYY-MM-DD to YYYY-MM-DD):"
    )
    return CheckTradesStates.CHECK_DATE_RANGE



async def check_by_trade_id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Prompts the user to enter the trade ID for checking trades.
    
    Args:
        update (Update): The update object that contains the callback query.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.
    
    Returns:
        int: The next state in the conversation (CHECK_ID).
    """
    query = update.callback_query
    await query.answer()

    # Ask the user to enter the trade ID
    await query.edit_message_text(
        text="Please enter the trade ID:")
    return CheckTradesStates.CHECK_ID



async def check_by_ticker_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Prompts the user to enter the ticker name for checking trades.
    
    Args:
        update (Update): The update object that contains the callback query.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.
    
    Returns:
        int: The next state in the conversation (CHECK_TICKER).
    """
    query = update.callback_query
    await query.answer()

    # Ask user to enter the ticker name
    await query.edit_message_text(
        text="Please enter the ticker name (e.g., XAUUSD):")
    return CheckTradesStates.CHECK_TICKER



async def check_by_side_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Prompts the user to select the side (Long/Short) for checking trades.
    
    Args:
        update (Update): The update object that contains the callback query.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.
    
    Returns:
        int: The next state in the conversation (CHECK_SIDE).
    """
    query = update.callback_query
    await query.answer()
    
    # Create a keyboard with options for selecting the trade side
    keyboard = [
        [InlineKeyboardButton("Long", callback_data='Long')],
        [InlineKeyboardButton("Short", callback_data='Short')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    # Ask the user to select the side
    await query.edit_message_text(
        text="Select the side (Long/Short):",
        reply_markup=reply_markup)
    return CheckTradesStates.CHECK_SIDE



async def check_by_status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Prompts the user to select the status (Win/Loss) for checking trades.
    
    Args:
        update (Update): The update object that contains the callback query.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.
    
    Returns:
        int: The next state in the conversation (CHECK_STATUS).
    """
    query = update.callback_query
    await query.answer()
    
    # Create a keyboard with options for selecting the trade status
    keyboard = [
        [InlineKeyboardButton("Win", callback_data='Win')],
        [InlineKeyboardButton("Loss", callback_data='Loss')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

     # Ask the user to select the status
    await query.edit_message_text(
        text="Select the status (Win/Loss):", 
        reply_markup=reply_markup
        )
    
    return CheckTradesStates.CHECK_STATUS



async def display_trades(update: Update, context: ContextTypes.DEFAULT_TYPE, trades):
    """
    Displays the list of trades to the user.
    
    Args:
        update (Update): The update object that contains the user's message.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.
        trades (list): The list of trades to display.
    """
    if not trades:
         # Inform the user if no trades are found
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="No trades found for the given criteria."
        )
    else:
        # Display each trade's details
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
    Handles the user's input for date range and retrieves the trades from the database.
    
    Args:
        update (Update): The update object that contains the user's message.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.
    
    Returns:
        int: Ends the conversation.
    """
    date_range = update.message.text.split(' to ')
    trades = trades_db.get_trades_by_date_range(date_range[0], date_range[1])
    await display_trades(update, context, trades)
    return await  return_to_main_menu(update, context)



async def trade_id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the user's input for trade ID and retrieves the trade from the database.
    
    Args:
        update (Update): The update object that contains the user's message.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.
    
    Returns:
        int: Ends the conversation.S
    """
    trade_id = update.message.text
    trade = trades_db.get_trade_by_id(trade_id)
    await display_trades(update, context, [trade] if trade else [])
    return await  return_to_main_menu(update, context)



async def ticker_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the user's input for ticker name and retrieves the trades from the database.
    
    Args:
        update (Update): The update object that contains the user's message.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.
    
    Returns:
        int: Ends the conversation.
    """
    ticker_name = update.message.text
    trades = trades_db.get_trades_by_ticker(ticker_name)
    await display_trades(update, context, trades)
    return await  return_to_main_menu(update, context)



async def side_selection_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the user's selection of trade side (Long/Short) and retrieves the trades from the database.
    
    Args:
        update (Update): The update object that contains the callback query.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.
    
    Returns:
        int: Ends the conversation.
    """
    query = update.callback_query
    await query.answer()
    side = query.data
    trades = trades_db.get_trades_by_side(side)
    await display_trades(update, context, trades)
    return await return_to_main_menu(update, context)



async def status_selection_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the user's selection of trade status (Win/Loss) and retrieves the trades from the database.
    
    Args:
        update (Update): The update object that contains the callback query.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.
    
    Returns:
        int: Ends the conversation.
    """
    query = update.callback_query
    await query.answer()
    status = query.data
    trades = trades_db.get_trades_by_status(status)
    await display_trades(update, context, trades)
    return await return_to_main_menu(update, context)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Cancels the current trade checking process.
    
    Args:
        update (Update): The update object that contains the user's message.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.
    
    Returns:
        int: Ends the conversation.
    """
    await update.message.reply_text('Trade recording cancelled.')
    return await  return_to_main_menu(update, context)
