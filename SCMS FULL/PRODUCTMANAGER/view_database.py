import sqlite3
from tabulate import tabulate

def view_database():
    # Connect to the database
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    
    # Get all products
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    
    # Get column names
    cursor.execute('PRAGMA table_info(products)')
    columns = [column[1] for column in cursor.fetchall()]
    
    # Print the data in a nice table format
    print("\nProduct Database Contents:")
    print(tabulate(products, headers=columns, tablefmt='grid'))
    
    # Close the connection
    conn.close()

if __name__ == '__main__':
    view_database() 