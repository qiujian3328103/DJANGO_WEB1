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
                product_id TEXT,
                bin_type TEXT,
                yield_value FLOAT,
                date DATE
            )''')

    # Generate and insert fake data
    fake = Faker()
    root_lot_ids = [fake.random_letter() + fake.random_letter() + fake.random_letter() + str(fake.random_number(digits=2)) for _ in range(600)]  # Generate 600 root_lot_ids
    wafer_ids = [f'{i:02}' for i in range(1, 26)]
    product_ids = ["Kamorta", "Magnus", "Jcala"]
    bin_types = ["ATPG_INT", "ATPG_SAF", "IDDQ", "MBIST_HV", "MBIST_LV", "DC", "TDF", "YIELD", "CONTINUITY", "RX"]

    start_date = datetime(2023, 1, 1)
    end_date = datetime.now()

    data_entries = []

    for root_lot_id in root_lot_ids:
        for wafer_id in wafer_ids:
            product_id = random.choice(product_ids)
            date = fake.date_between(start_date=start_date, end_date=end_date)

            bin_values = [random.uniform(0, 100) for _ in range(10)]
            total_sum = sum(bin_values)
            bin_values = [value * 100 / total_sum for value in bin_values]

            yield_value = round(random.uniform(70, 99), 2)
            atpg_int = max(round(random.uniform(15, 85), 2), 3.00)
            atpg_saf = max(round(random.uniform(5, 95), 2), 3.00)
            other_mbist = max(round(random.uniform(3, 97), 2), 3.00)
            other_bins = [max(round(random.uniform(0, 100 - atpg_int - atpg_saf - other_mbist), 2), 3.00) for _ in range(7)]

            bin_values[bin_types.index("ATPG_INT")] = atpg_int
            bin_values[bin_types.index("ATPG_SAF")] = atpg_saf
            bin_values[bin_types.index("MBIST_HV")] = other_mbist
            bin_values[bin_types.index("MBIST_LV")] = other_mbist
            bin_values[bin_types.index("DC")] = other_bins[0]
            bin_values[bin_types.index("TDF")] = other_bins[1]
            bin_values[bin_types.index("YIELD")] = other_bins[2]
            bin_values[bin_types.index("CONTINUITY")] = other_bins[3]
            bin_values[bin_types.index("RX")] = other_bins[4]

            bin_entries = list(zip(bin_types, bin_values))

            for bin_type, bin_value in bin_entries:
                data_entries.append((root_lot_id, wafer_id, product_id, bin_type, yield_value, date))  # Removed a bin_value here

    c.executemany('INSERT INTO yield_data (root_lot_id, wafer_id, product_id, bin_type, yield_value, date) VALUES (?, ?, ?, ?, ?, ?)', data_entries)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
if __name__ == '__main__':
    delete_table(table_name="yield_data")
    delete_table(table_name="yield_table")
    generate_fake_data()
