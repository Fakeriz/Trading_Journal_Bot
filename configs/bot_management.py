from functools import wraps
import os
import logging
from dotenv import load_dotenv
from typing import Final

from telegram import Update
from telegram.ext import ContextTypes

# Conversation states enumeration
INIT, DATE, TIME, TICKER, WIN_LOSS, SIDE, RR, PNL, STRATEGY, PHOTO, SAVE, CHECK_TRADES, CHECK_DATE_RANGE, CHECK_ID, CHECK_TICKER, CHECK_SIDE, CHECK_STATUS = range(17)

# Load environment variables from a .env file
LIST_OF_ADMINS = os.getenv('LIST_OF_ADMINS')
LIST_OF_ADMINS = [int(admin_id) for admin_id in LIST_OF_ADMINS.split(',')]

# Load BOT_TOKEN environment variable
load_dotenv()
BOT_TOKEN : Final = os.environ["BOT_TOKEN"]

# Settings for bot's logging.
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


# Decorator to restretic access to the bot to only admins.
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