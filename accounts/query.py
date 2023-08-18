import sqlite3 
import pandas as pd
def get_filtered_data(product_id, start_date, end_date):
    # conn = sqlite3.connect(r'C:\Users\Jian Qiu\Dropbox\pythonprojects\django_web1\db.sqlite3')  # Replace with the actual path to your SQLite database
    conn = sqlite3.connect(r"/Users/JianQiu/Dropbox/pythonprojects/django_web1/db.sqlite3")
    cursor = conn.cursor()

    # SQL query to retrieve filtered data
    query = """
    SELECT * FROM yield_data
    WHERE product_id = ? AND date >= ?  
      AND date <= ?
    """
    # Use pandas to read data directly from the database into a DataFrame
    filtered_data = pd.read_sql_query(query, conn, params=(product_id, start_date, end_date))

    conn.close()

    return filtered_data

# if __name__ == "__main__":
#     start_date = '2023-06-01'
#     end_date = '2023-06-30'
#     df = get_filtered_data(product_id="Magnus", start_date=start_date, end_date=end_date)
#     print(df)


# import pandas as pd

# # Your DataFrame
# data = {
#     'id': [1011, 1012, 1013],
#     'root_lot_id': ['GhX92', 'GhX92', 'GhX92'],
#     'wafer_id': ['02', '02', '02'],
#     'product_id': ['Kamorta', 'Kamorta', 'Kamorta'],
#     'bin_type': ['ATPG_INT', 'ATPG_SAF', 'IDDQ'],
#     'yield_value': [71.55, 71.55, 71.55],
#     'date': ['2023-08-02', '2023-08-02', '2023-08-02'],
#     'current_date': ['2023-31', '2023-31', '2023-31']
# }

# df = pd.DataFrame(data)

# # Pivot the DataFrame
# pivot_df = df.pivot_table(index='current_date', columns='bin_type', values='yield_value', aggfunc='mean')

# print(pivot_df)