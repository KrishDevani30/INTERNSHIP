import sqlite3

def check_database():
    try:
        # Connect to database
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        
        # Check table structure
        print("\nTable Structure:")
        cursor.execute("PRAGMA table_info(products)")
        columns = cursor.fetchall()
        for col in columns:
            print(col)
            
        # Check contents
        print("\nTable Contents:")
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        print(f"Number of rows: {len(rows)}")
        for row in rows:
            print(row)
            
        conn.close()
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    check_database() 