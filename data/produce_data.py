import sqlite3
import random
from datetime import datetime, timedelta

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(r'database\trades.db')
cursor = conn.cursor()

# Create the trades table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    time TEXT,
                    ticker TEXT,
                    win_loss TEXT,
                    side TEXT,
                    rr REAL,
                    pnl REAL,
                    strategy TEXT,
                    picture TEXT)''')

# Generate random data and insert 200 records
tickers = ['EURUSD', 'XAUUSD', 'US30', 'GBPUSD', 'EURJPY']
win_loss_choices = ['Win', 'Loss']
sides = ['Long', 'Short']
strategies = ['MTR', 'FF', 'Close NYSE', 'DHL']

for _ in range(200):
    # Random date within the last year
    random_days_ago = random.randint(0, 365)
    random_date = (datetime.now() - timedelta(days=random_days_ago)).strftime('%Y-%m-%d')
    
    # Random time
    random_time = f"{random.randint(0, 23):02}:{random.randint(0, 59):02}"
    
    # Random ticker, win_loss, side, strategy
    ticker = random.choice(tickers)
    win_loss = random.choice(win_loss_choices)
    side = random.choice(sides)
    strategy = random.choice(strategies)
    
    # Random rr (between 1 and 6) and pnl (between 10 and 100)
    rr = round(random.uniform(1, 6), 2)
    pnl = round(random.uniform(10, 100), 2)
    
    # Placeholder for the photo (could be file paths or URLs in practice)
    picture = 'photo_placeholder.png'
    
    # Insert the record into the database
    cursor.execute('''INSERT INTO trades (date, time, ticker, win_loss, side, rr, pnl, strategy, picture)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (random_date, random_time, ticker, win_loss, side, rr, pnl, strategy, picture))

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("200 records have been inserted into trades.db")

# Function to add a new trade manually
def add_trade(date, time, ticker, win_loss, side, rr, pnl, strategy, picture):
    conn = sqlite3.connect('trades.db')
    cursor = conn.cursor()
    
    cursor.execute('''INSERT INTO trades (date, time, ticker, win_loss, side, rr, pnl, strategy, picture)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (date, time, ticker, win_loss, side, rr, pnl, strategy, picture))
    
    conn.commit()
    conn.close()
    print("New trade has been added to trades.db")

# Example of how to use the add_trade function
# add_trade('2024-08-13', '14:30', 'EURUSD', 'Win', 'Long', 3.5, 75.25, 'MTR', 'new_photo.png')
