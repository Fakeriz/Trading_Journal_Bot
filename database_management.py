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
        

# Save trades to db
def save_trade(date, ticker, time, win_loss, side, rr, pnl, strategy, picture):
    try:
        conn = sqlite3.connect('trades.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO trades (date, time,ticker, win_loss, side, rr, pnl, strategy, picture)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (date, time, ticker, win_loss, side, rr, pnl, strategy, picture))
        conn.commit()
        conn.close()
    except Exception as e:
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