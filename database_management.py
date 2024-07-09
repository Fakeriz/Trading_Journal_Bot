import sqlite3

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
    conn.close()

    trade_list = []
    for trade in c.fetchall():
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
    conn.close()

    trade_list = []
    for trade in c.fetchall():
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
        WHERE status = ?
        """
    c.execute(query, (status,))
    conn.close()

    trade_list = []
    for trade in c.fetchall():
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