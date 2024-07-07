import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

logger = logging.getLogger(__name__)

CHECK_TRADES, DATE_RANGE, SPECIFIC_TRADE = range(3)

async def start_check_trades(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the start of the check trades process.
    """
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Date Range", callback_data='date_range')],
        [InlineKeyboardButton("Specific Trade", callback_data='specific_trade')],
        [InlineKeyboardButton("Ticker", callback_data='ticker')],
        [InlineKeyboardButton("Trade's Side", callback_data='trade_side')],
        [InlineKeyboardButton("Trade's Status(Win/Loss)", callback_data='trade_status')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="How would you like to check the trades?", reply_markup=reply_markup)
    return CHECK_TRADES

async def trade_date_range_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles checking trades by date range.
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Please enter the date range (YYYY-MM-DD to YYYY-MM-DD):")
    return DATE_RANGE

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Cancels the current checking trades process.
    """
    await update.message.reply_text('Checking previous trades cancelled.')
    logger.info(f"Checking previous trades cancelled by user {update.effective_user.id}")
    return ConversationHandler.END
