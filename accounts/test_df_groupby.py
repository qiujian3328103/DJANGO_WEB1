import pandas as pd 

import sqlite3 

# Connect to the SQLite database
conn = sqlite3.connect(r'/Users/JianQiu/Dropbox/pythonprojects/django_web1/db.sqlite3')

# Load data into a DataFrame
df = pd.read_sql_query("SELECT * FROM yield_data", conn)

# Close the connection
conn.close()



df["date"] = pd.to_datetime(df['date'])
df['current_date'] = df['date'].dt.strftime('%Y-%w')
print(df)
# Group data by 'current_date' and calculate the average yield_value
grouped_data = df.groupby('current_date')['yield_value'].mean().reset_index()


print(grouped_data)