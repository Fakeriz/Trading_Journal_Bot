from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from database.database_management import TradeDatabase
from utils.states_manager import UpdateTradesState
from utils.bot_management import return_to_main_menu



async def start_update_trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Starts the trade update process by displaying a menu with options to update a trade,
    remove a trade, or remove the entire database.

    Args:
        update (Update): The update object containing the callback query.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.

    Returns:
        int: The next state in the conversation (UPDATE_CHOICE).
    """

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("🗃️ Update a Trade", callback_data="update_trade_by_id")],
        [InlineKeyboardButton("✐ Remove a Trade", callback_data='remove_trade')],
        [InlineKeyboardButton("💀 Remove Whole Database", callback_data='remove_all_data')]
    ]
    # Display the keyboard to the user.
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
    """
    Handles the user input for the Trade ID, verifies if the trade exists, and
    prompts the user to choose the field they want to update.

    Args:
        update (Update): The update object containing the user's input.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.

    Returns:
        int: The next state in the conversation (UPDATE_FIELD_CHOICE or TRADE_ID).
    """
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
        return UpdateTradesState.UPDATE_FIELD_CHOICE
    else:
        await update.message.reply_text("Trade ID not found. Please enter a valid Trade ID:")
        return UpdateTradesState.TRADE_ID


async def update_field_choice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the user's choice of which field to update (e.g., ticker, status, side, strategy),
    and prompts the user for the new value.

    Args:
        update (Update): The update object containing the callback query.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.

    Returns:
        int: The next state in the conversation (UPDATE_TICKER, UPDATE_STATUS, UPDATE_SIDE, or UPDATE_STRATEGY).
    """
    query = update.callback_query
    await query.answer()
    
    field = query.data.split('_')[1]
    # field = query.data
    context.user_data['update_field'] = field
    
    if field == 'ticker':
        await query.message.reply_text("Please enter the new ticker:")
        return UpdateTradesState.UPDATE_TICKER

    elif field == 'status':
        keyboard = [
            [InlineKeyboardButton("Win", callback_data='update_status_Win')],
            [InlineKeyboardButton("Loss", callback_data='update_status_Loss')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Select the new status:", reply_markup=reply_markup)
        return UpdateTradesState.UPDATE_STATUS

    elif field == 'side':
        keyboard = [
            [InlineKeyboardButton("Long", callback_data='update_side_Long')],
            [InlineKeyboardButton("Short", callback_data='update_side_Short')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Select the new side:", reply_markup=reply_markup)
        return UpdateTradesState.UPDATE_SIDE

    elif field == 'strategy':
        keyboard = [
            [InlineKeyboardButton("DHL", callback_data='update_strategy_DHL')],
            [InlineKeyboardButton("Close_NYSE", callback_data='update_strategy_Close_NYSE')],
            [InlineKeyboardButton("MTR", callback_data='update_strategy_MTR')],
            [InlineKeyboardButton("FF", callback_data='update_strategy_FF')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Select the new strategy:", reply_markup=reply_markup)
        return UpdateTradesState.UPDATE_STRATEGY
    else:
        return await return_to_main_menu(update, context)


async def update_ticker_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the update of the ticker field for a specific trade.

    Args:
        update (Update): The update object containing the user's input.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.

    Returns:
        Coroutine: Returns to the main menu after updating the ticker.
    """
    new_ticker = update.message.text
    trade_id = context.user_data['trade_id']
    trades_db = TradeDatabase()
    
    try:
        trades_db.update_trade(trade_id, ticker=new_ticker)
        await update.message.reply_text(f"Ticker updated successfully to {new_ticker}.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred while updating the ticker: {e}")
    
    return await return_to_main_menu(update, context)


async def update_status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the update of the status field for a specific trade.

    Args:
        update (Update): The update object containing the callback query.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.

    Returns:
        Coroutine: Returns to the main menu after updating the status.
    """
    query = update.callback_query
    await query.answer()
    
    new_status = query.data.split('_')[-1]
    trade_id = context.user_data['trade_id']
    trades_db = TradeDatabase()
    
    try:
        trades_db.update_trade(trade_id, win_loss=new_status)
        await query.message.reply_text(f"Status updated successfully to {new_status}.")
    except Exception as e:
        await query.message.reply_text(f"An error occurred while updating the status: {e}")
    
    return await return_to_main_menu(update, context)


async def update_side_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the update of the side field for a specific trade.

    Args:
        update (Update): The update object containing the callback query.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.

    Returns:
        Coroutine: Returns to the main menu after updating the side.
    """
    query = update.callback_query
    await query.answer()
    
    new_side = query.data.split('_')[-1]
    trade_id = context.user_data['trade_id']
    trades_db = TradeDatabase()
    
    try:
        trades_db.update_trade(trade_id, side=new_side)
        await query.message.reply_text(f"Side updated successfully to {new_side}.")
    except Exception as e:
        await query.message.reply_text(f"An error occurred while updating the side: {e}")
    
    return await return_to_main_menu(update, context)


async def update_strategy_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the update of the strategy field for a specific trade.

    Args:
        update (Update): The update object containing the callback query.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.

    Returns:
        Coroutine: Returns to the main menu after updating the strategy.
    """
    query = update.callback_query
    await query.answer()
    
    new_strategy = query.data.split('_')[-1]
    trade_id = context.user_data['trade_id']
    trades_db = TradeDatabase()
    
    try:
        trades_db.update_trade(trade_id, strategy=new_strategy)
        await query.message.reply_text(f"Strategy updated successfully to {new_strategy}.")
    except Exception as e:
        await query.message.reply_text(f"An error occurred while updating the strategy: {e}")
    
    return await return_to_main_menu(update, context)


async def start_remove_trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Initiates the process to remove a specific trade by prompting the user to enter the Trade ID.

    Args:
        update (Update): The update object containing the callback query.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.

    Returns:
        int: The next state in the conversation (REMOVE_TRADE_ID).
    """
    await update.callback_query.message.reply_text("Please enter the Trade ID you want to remove:")
    return UpdateTradesState.REMOVE_TRADE_ID


async def remove_trade_by_id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the removal of a trade by its ID. Checks if the trade exists, and if so, removes it.
    If the trade does not exist, prompts the user to enter a valid Trade ID.

    Args:
        update (Update): The update object containing the user's input.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.

    Returns:
        int: The next state in the conversation (REMOVE_TRADE_ID) if an error occurs or trade not found,
              or returns to the main menu after successful removal.
    """
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
    """
    Initiates the process to remove the entire database by presenting a confirmation keyboard to the user.

    Args:
        update (Update): The update object containing the callback query.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.

    Returns:
        int: The next state in the conversation (REMOVE_ALL_DATA).
    """
    keyboard = [
        [InlineKeyboardButton("👍🏼 Confirm", callback_data='confirm_remove_all_data')],
        [InlineKeyboardButton("⛔ Cancel", callback_data='cancel_remove_all_data')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(
        text="Are you sure you want to remove the whole database?",
        reply_markup=reply_markup
    )
    return UpdateTradesState.REMOVE_ALL_DATA

async def remove_whole_database(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the removal of the entire database. Provides feedback to the user on the success or failure of the operation.

    Args:
        update (Update): The update object containing the callback query.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.

    Returns:
        Coroutine: Returns to the main menu after removing the database or if an error occurs.
    """
    trades_db = TradeDatabase()

    try:
        trades_db.remove_all_trades()
        await update.callback_query.message.reply_text("The whole database has been removed.")
    except Exception as e:
        await update.callback_query.message.reply_text(f"An error occurred: {e}")

    return await return_to_main_menu(update, context)