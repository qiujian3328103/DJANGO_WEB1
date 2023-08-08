# generate_fake_data.py

import sqlite3
import random
from faker import Faker
from datetime import datetime, timedelta

def delete_table(table_name = "yield_data"):
    """_summary_
    delete the table 
    """
    # Connect to the SQLite database (replace 'your_database.db' with your actual database file)
    conn = sqlite3.connect(r'C:\Users\Jian Qiu\Dropbox\pythonprojects\django_web1\db.sqlite3')
    cursor = conn.cursor()

    # Drop the table
    query = f"DROP TABLE IF EXISTS {table_name};"
    cursor.execute(query)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def generate_fake_data():
    # Connect to the database
    conn = sqlite3.connect(r'C:\Users\Jian Qiu\Dropbox\pythonprojects\django_web1\db.sqlite3')
    c = conn.cursor()
    
    # Create the yield_data table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS yield_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                root_lot_id TEXT,
                wafer_id CHAR(2),
                yield_value FLOAT,
                date DATE
            )''')

    # Generate and insert fake data
    fake = Faker()
    root_lot_ids = [fake.random_letter() + fake.random_letter() + fake.random_letter() + str(fake.random_number(digits=2)) for _ in range(5)]
    wafer_ids = [f'{i:02}' for i in range(1, 26)]
    start_date = datetime(2023, 1, 1)
    end_date = datetime.now()

    data_entries = []

    for _ in range(10000):
        root_lot_id = random.choice(root_lot_ids)
        wafer_id = random.choice(wafer_ids)
        yield_value = round(random.uniform(70, 99), 2)
        date = fake.date_between(start_date=start_date, end_date=end_date)
        data_entries.append((root_lot_id, wafer_id, yield_value, date))

    c.executemany('INSERT INTO yield_data (root_lot_id, wafer_id, yield_value, date) VALUES (?, ?, ?, ?)', data_entries)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    delete_table(table_name="yield_data")
    delete_table(table_name="yield_table")
    generate_fake_data()
