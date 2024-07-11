import sqlite3
import datetime


# Initialize the database
def init_db():
    try:
        conn = sqlite3.connect('trades.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATETIME,
                time DATETIME,
                ticker TEXT,
                win_loss TEXT,
                side TEXT,
                rr INTEGER,
                pnl FLOAT,
                strategy TEXT,
                picture TEXT)
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)

def save_trade(date, ticker, time, win_loss, side, rr, pnl, strategy, picture):
    """
    Save a trade record to the database.

    Args:
        date (str): The date of the trade in 'YYYY-MM-DD' format.
        ticker (str): The ticker symbol of the traded asset.
        time (str): The time of the trade.
        win_loss (str): The status of the trade ('Win' or 'Loss').
        side (str): The side of the trade ('Long' or 'Short').
        rr (float): The risk-reward ratio of the trade.
        pnl (float): The profit or loss from the trade.
        strategy (str): The strategy used for the trade.
        picture (str): The file_id of the picture associated with the trade.

    Raises:
        Exception: If there is an issue saving the trade to the database.
    """

    try:
        # Connect to the database
        conn = sqlite3.connect('trades.db')
        c = conn.cursor()
        
        # Insert the trade record into the trades table
        c.execute('''
            INSERT INTO trades (date, time, ticker, win_loss, side, rr, pnl, strategy, picture)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (date, time, ticker, win_loss, side, rr, pnl, strategy, picture))
        
        # Commit the transaction
        conn.commit()
        
        # Close the database connection
        conn.close()
    except Exception as e:
        # Print the exception message if an error occurs
        print(e)

def get_trades_by_date_range(start_date: str, end_date:str):
    """
    Fetch trades from the database within the specified date range.
    """
    conn = sqlite3.connect('trades.db')
    c = conn.cursor()
    query = """
        SELECT id, date, time, ticker, side, win_loss, pnl, rr, strategy, picture
        FROM trades
        WHERE date BETWEEN ? AND ?
    """
    c.execute(query, (start_date, end_date))
    trades = c.fetchall()
    conn.close()
    
    # Convert Fetched Data to a list of dictionaries
    trade_list = []
    for trade in trades:
        trade_dict = {
            'id': trade[0],
            'date': trade[1],
            'time': trade[2],
            'ticker': trade[3],
            'side': trade[4],
            'status': trade[5],
            'pnl': trade[6],
            'rr': trade[7],
            'strategy': trade[8],
            'picture': trade[9]
        }
        trade_list.append(trade_dict)
    
    return trade_list

def get_trades_by_id(id: int):
    """Retrieve and search records by trade's ID.
    Args:
        id (int): The ID of the trade to retrieve.
    Returns:
        dict: A dictionary containing the trade details if found, otherwise None.
    """

    conn = sqlite3.connect('trades.db')
    c = conn.cursor()
    query = """
        SELECT *
        FROM trades 
        WHERE id=?
    """
    c.execute(query, (id,))
    trade = c.fetchone()
    conn.close()
    
    if trade:
        return {
            'id': trade[0],
            'date': trade[1],
            'time': trade[2],
            'ticker': trade[3],
            'side': trade[4],
            'status': trade[5],
            'pnl': trade[6],
            'rr': trade[7],
            'strategy': trade[8],
            'picture': trade[9]
        }
    else:
        return "No Trade Found..."

def get_trades_by_ticker(ticker_name: str):
    """Retrieve and search records by trade's ticker.
    Args:
        ticker_name -> str
            The name of specific ticker. e.g XAUUSD (Gold)
    Returns:
        dict: A dictionary containing all the trades found by ticker name.
    """
    conn = sqlite3.connect('trades.db')
    c = conn.cursor()
    query = """ 
        SELECT * 
        FROM trades
        WHERE ticker = ?
        """
    c.execute(query, (ticker_name,))
    trades = c.fetchall()
    conn.close()

    trade_list = []
    for trade in trades:
        trade_dict = {
            'id': trade[0],
            'date': trade[1],
            'time': trade[2],
            'ticker': trade[3],
            'side': trade[4],
            'status': trade[5],
            'pnl': trade[6],
            'rr': trade[7],
            'strategy': trade[8],
            'picture': trade[9]
        }
        trade_list.append(trade_dict)
    return trade_list

def get_trades_by_side(side: str):
    """Retrieve and search records by trade's side (Long/Short).
    Args:
        side -> str
            The side of trade whether it is a Long(Buy) Or Short(Sell) trade.
    Returns:
        dict: A dictionary containing all the trades found by ticker name.
    """

    conn = sqlite3.connect('trades.db')
    c = conn.cursor()
    query = """
        SELECT * 
        FROM trades
        WHERE side = ?
        """
    c.execute(query, (side,))
    trades = c.fetchall()
    conn.close()

    trade_list = []
    for trade in trades:
        trade_dict = {
            'id': trade[0],
            'date': trade[1],
            'time': trade[2],
            'ticker': trade[3],
            'side': trade[4],
            'status': trade[5],
            'pnl': trade[6],
            'rr': trade[7],
            'strategy': trade[8],
            'picture': trade[9]
        }
        trade_list.append(trade_dict)
    return trade_list

def get_trades_by_status(status: str):
    """Retrieve and search records by trade's status(Win/Loss)
    Args:
        status -> str
            Specifing whether search must be conducted by Win trades or Loss trades.
    Returns:
        dict: A dictionary containing all the trades found by ticker name.
    """
    
    conn = sqlite3.connect('trades.db')
    c = conn.cursor()
    query = """
        SELECT * 
        FROM trades
        WHERE win_loss = ?
        """
    c.execute(query, (status,))
    trades = c.fetchall()
    conn.close()

    trade_list = []
    for trade in trades:
        trade_dict = {
            'id': trade[0],
            'date': trade[1],
            'time': trade[2],
            'ticker': trade[3],
            'side': trade[4],
            'status': trade[5],
            'pnl': trade[6],
            'rr': trade[7],
            'strategy': trade[8],
            'picture': trade[9]
        }
        trade_list.append(trade_dict)

    return trade_list


def get_all_tickers():
    """
    Fetch all unique tickers from the database.
    
    Returns:
        list: A list of unique tickers.
    """
    try:
        conn = sqlite3.connect('trades.db')
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT ticker FROM trades")
        tickers = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tickers
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []

def get_trades_for_export(ticker, period):
    """
    Fetch trades for a specified ticker and period.
    
    Args:
        ticker (str): The ticker symbol.
        period (str): The period (e.g., '1D', '1W', '1M').
    
    Returns:
        list: A list of trades.
    """
    conn = sqlite3.connect('trades.db')
    c = conn.cursor()

    # Calculate date range using timedelta
    end_date = datetime.datetime.now() # Variable to store end date (today)
    if period == '1D':
        start_date = end_date - datetime.timedelta(days=1)
    elif period == '3D':
        start_date = end_date - datetime.timedelta(days=3)
    elif period == '1W':
        start_date = end_date - datetime.timedelta(weeks=1)
    elif period == '2W':
        start_date = end_date - datetime.timedelta(weeks=2)
    elif period == '1M':
        start_date = end_date - datetime.timedelta(days=10)
    elif period == '3M':
        start_date = end_date - datetime.timedelta(days=90)
    elif period == '6M':
        start_date = end_date - datetime.timedelta(days=180)

    # Query to fetch trades within specified data range.
    c.execute("SELECT * FROM trades WHERE ticker = ? AND date BETWEEN ? AND ?", (ticker, start_date, end_date))
    trades = c.fetchall()
    conn.close()
    
    return trades