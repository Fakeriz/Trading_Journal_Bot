import sqlite3
import datetime


class TradeDatabase:
    def __init__(self, db_path=r'database/trades.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the database and create trades table if it does not exist."""
        try:
            conn = sqlite3.connect(self.db_path)
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
                    picture TEXT
                )
            ''')
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)


    def save_trade(self, date, ticker, time, win_loss, side, rr, pnl, strategy, picture):
        """Save a trade record to the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('''
                INSERT INTO trades (date, time, ticker, win_loss, side, rr, pnl, strategy, picture)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (date, time, ticker, win_loss, side, rr, pnl, strategy, picture))

            # Get trade id
            trade_id = c.lastrowid

            conn.commit()
            return trade_id

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None

        finally:
            if conn:
                conn.close()

    def get_trades_by_date_range(self, start_date, end_date):
        """Fetch trades from the database within the specified date range."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        query = """
            SELECT id, date, time, ticker, side, win_loss, pnl, rr, strategy, picture
            FROM trades
            WHERE date BETWEEN ? AND ?
        """
        c.execute(query, (start_date, end_date))
        trades = c.fetchall()
        conn.close()
        
        return [self._trade_to_dict(trade) for trade in trades]

    def get_trade_by_id(self, trade_id):
        """Retrieve and search records by trade's ID."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        query = "SELECT * FROM trades WHERE id=?"
        c.execute(query, (trade_id,))
        trade = c.fetchone()
        conn.close()
        
        return self._trade_to_dict(trade) if trade else None

    def get_trades_by_ticker(self, ticker_name):
        """Retrieve and search records by trade's ticker."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        query = "SELECT * FROM trades WHERE ticker = ?"
        c.execute(query, (ticker_name,))
        trades = c.fetchall()
        conn.close()
        
        return [self._trade_to_dict(trade) for trade in trades]

    def get_trades_by_side(self, side):
        """Retrieve and search records by trade's side (Long/Short)."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        query = "SELECT * FROM trades WHERE side = ?"
        c.execute(query, (side,))
        trades = c.fetchall()
        conn.close()
        
        return [self._trade_to_dict(trade) for trade in trades]

    def get_trades_by_status(self, status):
        """Retrieve and search records by trade's status (Win/Loss)."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        query = "SELECT * FROM trades WHERE win_loss = ?"
        c.execute(query, (status,))
        trades = c.fetchall()
        conn.close()
        
        return [self._trade_to_dict(trade) for trade in trades]

    def get_all_tickers(self):
        """Fetch all unique tickers from the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT DISTINCT ticker FROM trades")
            tickers = [row[0] for row in c.fetchall()]
            conn.close()
            return tickers
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []

    def get_trades_for_export(self, ticker=None, period=None, start_date=None, end_date=None):
        """Fetch trades for a specified ticker and period, or custom date range."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        if period:
            end_date = datetime.datetime.now().date()
            start_date = self._calculate_start_date(period, end_date)
        elif start_date and end_date:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        else:
            raise ValueError("Either period or custom date range must be specified.")

        query = "SELECT * FROM trades WHERE date BETWEEN ? AND ?"
        params = (start_date, end_date)

        if ticker:
            query += " AND ticker = ?"
            params = (start_date, end_date, ticker)

        c.execute(query, params)
        trades = c.fetchall()
        conn.close()

        return [self._trade_to_dict(trade) for trade in trades]

    def _calculate_start_date(self, period, end_date):
        """Calculate start date based on period."""
        periods = {
            '1D': 1, '2D': 2, '3D': 3,
            '1W': 7, '2W': 14,
            '1M': 30, '2M': 60, '3M': 90, '6M': 180
        }
        if period not in periods:
            raise ValueError("Invalid period specified.")
        return end_date - datetime.timedelta(days=periods[period])

    def _trade_to_dict(self, trade):
        """Convert trade tuple to dictionary."""
        return {
            'id': trade[0],
            'date': trade[1],
            'time': trade[2],
            'ticker': trade[3],
            'side': trade[4],
            'win_loss': trade[5],
            'pnl': trade[6],
            'rr': trade[7],
            'strategy': trade[8],
            'picture': trade[9]
        } if trade else None
