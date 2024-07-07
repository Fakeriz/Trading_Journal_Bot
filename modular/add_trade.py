from telegram import (
                    Update, 
                    InlineKeyboardButton,
                    InlineKeyboardMarkup
    )
from telegram.ext import (
            ConversationHandler, 
            ContextTypes
    )
import database_management


# Conversation states
INIT, DATE, TIME, TICKER, WIN_LOSS, SIDE, RR, PNL, STRATEGY, PHOTO, SAVE = range(11)

async def new_trade_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Starts the process of adding a new trade.
    """
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("XAUUSD", callback_data='XAUUSD')],
        [InlineKeyboardButton("EURUSD", callback_data='EURUSD')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Please Choose Ticker's Name.", reply_markup=reply_markup)
    return WIN_LOSS

async def win_loss_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the selection of the trade result (Win/Loss).
    """
    query = update.callback_query
    await query.answer()
    
    context.user_data['ticker_name'] = query.data  # Store selected ticker
    
    keyboard = [
        [InlineKeyboardButton("Win", callback_data='Win')],
        [InlineKeyboardButton("Loss", callback_data='Loss')],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Trade Status? (WIN/LOSS).", reply_markup=reply_markup)
    return SIDE

async def side_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the selection of the trade side (Long/Short).
    """
    query = update.callback_query
    await query.answer()
    
    context.user_data['win_loss'] = query.data  # Store win/loss status
    
    keyboard = [
        [InlineKeyboardButton("Long", callback_data='Long')],
        [InlineKeyboardButton("Short", callback_data='Short')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text= "Position Side? (Buy/Sell)", reply_markup=reply_markup)
    return STRATEGY

async def strategy_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the selection of the trading strategy.
    Currently, available strategies are:
    - MTR
    - FF
    - Close NYSE
    - DHL (High/Low previous day) 
    """
    query = update.callback_query
    await query.answer()
    
    context.user_data['side'] = query.data # store trade's side
    
    keyboard = [
        [InlineKeyboardButton("DHL", callback_data='DHL')],
        [InlineKeyboardButton("Close NYSE", callback_data='Close_NYSE')],
        [InlineKeyboardButton("MTR", callback_data='MTR')],
        [InlineKeyboardButton("FF", callback_data="FF")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text= "Trading Setup?", reply_markup=reply_markup)
    return DATE

async def date_handler(update:Update, context:ContextTypes.DEFAULT_TYPE):
    """
    Asks the user for the trade date.
    """
    query = update.callback_query
    await query.answer()

    # Collect Date
    context.user_data['strategy'] = query.data
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Please enter the date of the trade (YYYY-MM-DD):"
    )
    return TIME

async def time_handler(update:Update, context:ContextTypes.DEFAULT_TYPE):
    """
    Asks the user for the trade time.
    """
    # Collect Time
    context.user_data['date'] = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.id,
        text="Time Of Trade?(HH:MM)"
    )
    return RR

async def rr_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Asks the user for the Risk:Reward ratio.
    """
    # Collect RR
    context.user_data['time'] = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.id,
        text="What is Risk:Reward Ration?"
    )
    return PNL


async def pnl_handler(update:Update, context:ContextTypes.DEFAULT_TYPE):
    """
    Asks the user for the PnL (Profit and Loss) of the trade.
    """
    # Collect Total PnL
    context.user_data['rr'] = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.id,
        text="What was PnL?"
    )
    return PHOTO

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Asks the user to send a picture of the trade.
    """
    context.user_data['pnl'] = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.id,
        text="Please Send a Picture of Your Trade."
    )
    return SAVE

async def save_trade_handler(update:Update, context:ContextTypes.DEFAULT_TYPE):
    """
    Saves the trade details to the database.
    """
    context.user_data['photo'] = update.message.photo[-1].file_id
    # Call save_trade function to record data in database
    database_management.save_trade(
        date= context.user_data['date'], 
        time= context.user_data['time'], 
        ticker = context.user_data['ticker_name'],
        win_loss= context.user_data['win_loss'], 
        side= context.user_data['side'], 
        rr= context.user_data['rr'], 
        pnl= context.user_data['pnl'],
        strategy= context.user_data['strategy'], 
        picture= context.user_data['photo'])

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.id,
        text="Recorded Succesfully."
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Cancels the current trade recording process.
    """
    await update.message.reply_text('Trade recording cancelled.')
    return ConversationHandler.END