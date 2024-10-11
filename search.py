import sqlite3
from safe_data import *

'''
How to use the search function:
-----------------------------------------------------
search_term:    the term you want to search for
table:          the table you want to search in
column:         only enter if you want to search in a specific column, otherwise leave empty

CODE EXAMPLE:
search_term = input("Enter search term: ")
search_results = search(search_term, table, column)
display_search_results(search_results)
-----------------------------------------------------
'''

def search(search_term, table, column="*"):
    connection = sqlite3.connect("mealmanagement.db")
    cursor = connection.cursor()

    table = table.upper()

    cursor.execute(f"PRAGMA table_info({table})")
    columns_info = cursor.fetchall()
    # Password column skipped
    columns = [info[1] for info in columns_info if "password" not in info[1].lower()]

    # If no columns are left, return
    if not columns:
        return f"No columns found in {table}"

    # If specific columns are requested, filter them against the table's column info
    if column != "*":
        column = column if column in columns else "*"
    
    # Join the columns to put in query
    if column == "*":
        columns_to_query = ", ".join(columns)
    else: 
        columns_to_query = column
    
    cursor.execute(f"SELECT {columns_to_query} FROM {table}")
    all_data = cursor.fetchall()
    search_results = []

    # add column names to the search results first (and set them to upper case)
    search_results.append([col.upper() for col in columns])

    # loop through all data in the table
    for row in all_data:
        decrypted_data = []
        for item in row:
            # if item is not a password, append it to the decrypted_data list
            if isinstance(item, bytes) and len(item) == 256:
                decrypted_data.append(decrypt_data(private_key(), item))
            else:
                decrypted_data.append(item)
        # if the search term is in the decrypted data, add it to the search results
        if any(search_term in str(field) for field in decrypted_data):
            search_results.append(decrypted_data)
        
    if len(search_results) == 1:
            return []

    return search_results


def display_search_results(search_results):
    print("--- Results ---")
    if type(search_results) == str:
        print(search_results)
        return

    for i in range(len(search_results)):
        line = ""
        if i == 0:
            line += "     "
        else:
            line += f"[{i}]  "
        for j in range(4):
            line += str(search_results[i][j]).ljust(15)
        print(line)
    return
    