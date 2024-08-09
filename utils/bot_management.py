import os
import logging
from functools import wraps
from dotenv import load_dotenv
from typing import Final

from telegram import Update
from telegram.ext import ContextTypes
from telegram import (
    Update, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup
    )


# Conversation states enumeration
INIT, DATE, DATE_VALIDATION, TIME, TICKER, WIN_LOSS, SIDE, RR, PNL, STRATEGY, PHOTO, SAVE, CHECK_TRADES, CHECK_DATE_RANGE, CHECK_ID, CHECK_TICKER, CHECK_SIDE, CHECK_STATUS = range(18)


# Load environment variables from a .env file
LIST_OF_ADMINS = os.getenv('LIST_OF_ADMINS')
LIST_OF_ADMINS = [int(admin_id) for admin_id in LIST_OF_ADMINS.split(',')]

# Load BOT_TOKEN environment variable
load_dotenv()
BOT_TOKEN : Final = os.environ["BOT_TOKEN"]

# Settings for bot's logging.
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)



# Decorator to restrict access to the bot to only admins.
def restricted(func):
    """
    Decorator to restrict access to certain functions to admin users only.
    
    This decorator checks if the user attempting to access the decorated function
    is in the list of authorized admin users. If the user is not authorized, access
    is denied and a warning message is logged.
    
    Parameters:
    - func: The function to be decorated.
    
    Returns:
    - The wrapped function with access control.
    """
    @wraps(func)
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            logger.warning(f"Unauthorized access denied for {user_id}.")
            await update.message.reply_text("Access denied")
            return
        return await func(update, context, *args, **kwargs)
    return wrapped



@restricted
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the /start command. Sends a welcome message and provides options for the user to choose from.

    Args:
        update (Update): The update object that contains the user's message.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.
    
    Returns:
        int: The next state in the conversation (INIT).
    """

    # Get the user that sent the /start command and log their name
    if update.message:
        user = update.message.from_user
        chat_id = update.message.chat.id
    elif update.callback_query:
        user = update.callback_query.from_user
        chat_id = update.callback_query.message.chat.id
        await update.callback_query.answer()

    logger.info("User %s started the conversation.", user.first_name)
    
    # Define the keyboard options for the user to choose from
    keyboard = [
        [InlineKeyboardButton("➕ Add New Trade", callback_data='add_new_trade')],
        [InlineKeyboardButton("📊 Check Previous Trades", callback_data='check_previous_trades')],
        [InlineKeyboardButton("📁 Export Data (CSV)", callback_data='export_csv')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the welcome message with the keyboard options
    await context.bot.send_message(chat_id=chat_id,
                                   text="Please choose an option from the menu below:",
                                   reply_markup=reply_markup)
    return INIT



async def return_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Informs the user that they are returning to the main menu and then displays the main menu options.
    
    Args:
        update (Update): The update object that contains the user's message.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.
    
    Returns:
        int: The next state in the conversation (INIT).
    """

    # chat_id = update.effective_chat.id if update.effective_chat else update.callback_query.message.chat.id

    if update.callback_query:
        await update.callback_query.answer()

    await start(update, context)
    return INIT
