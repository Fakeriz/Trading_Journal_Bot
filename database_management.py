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