import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect('trades.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS trades
                 (date DATETIME, time DATETIME, win_loss TEXT, side TEXT, rr INTEGER, pnl FLOAT, strategy TEXT, picture TEXT)''')
    conn.commit()
    conn.close()

def save_trade(trade):
    conn = sqlite3.connect('trades.db')
    c = conn.cursor()
    c.execute("INSERT INTO trades (date, time, win_loss, side, rr, pnl, strategy, picture) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (trade['date'], trade['time'], trade['win_loss'], trade['side'], trade['rr'], trade['pnl'], trade['strategy'], trade['picture']))
    conn.commit()
    conn.close()

# Call init_db when the script starts
if __name__ == '__main__':
    init_db()
