import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()

    try:
        c.execute("""CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                type  TEXT NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL)""")
        
        conn.commit()

    except sqlite3.Error as e:
        print("Database error detected: ", e)

    finally:
        if conn:
            conn.close()

def add_transaction():
    transaction_type = input("Would you like to add an income or an expense (income/expense): ").lower()
    amount = float(input("Amount: "))
    category = input("Category: ").lower()
    date = input("Date (DD-MM-YYYY): ")
    description = input("Description (optional): ")
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect('finance.db')
    c = conn.cursor()

    c.execute("""INSERT INTO transactions (type, amount, category, date, description, created_at)
              VALUES (?, ?, ?, ?, ?, ?)""", 
              (transaction_type, amount, category, date, description, created_at))
    conn.commit()
    conn.close()

    print("Transaction added succesfully!")

def list_transactions():
    print("1-See all your transactions")
    print("2-See your incomes")
    print("3-See your expenses")
    print("4-Return to main menu")

    seeOpr = input("Please enter your operation: ")

    conn = sqlite3.connect('finance.db')
    c = conn.cursor()

    if (seeOpr.isdigit() == False or int(seeOpr) < 1 or int(seeOpr) > 4):
        print("Please enter a valid operation!")
    
    elif (seeOpr == "4"):
        print("Returning to the main menu.")
        conn.close()
        return
        
    elif (seeOpr == "1"):

        c.execute("SELECT * FROM transactions")
        rows = c.fetchall()

        if not rows:
            print("There aren't any transactions!")
            conn.close()
            return

        for row in rows:
            print(row)

        conn.close()

    elif (seeOpr == "2" or seeOpr == "3"):
        if (seeOpr == "2"):
            t_type = "income"
        else:
            t_type = "expense"

        c.execute("SELECT * FROM transactions WHERE type = ?", (t_type,))

        rows = c.fetchall()

        if not rows:
            if (seeOpr == "2"):
                print("There aren't any incomes!")
            else:
                print("There aren't any expenses!")
            conn.close()
            return
        
        for row in rows:
            print(row)
        
        conn.close()

def delete_transaction():
    id = input("Please enter transaction ID to delete: ")

    if (id.isdigit() == False):
        print("Invalid ID")
        return

    conn = sqlite3.connect('finance.db')
    c = conn.cursor()

    c.execute("DELETE FROM transactions WHERE id = ?", (id,))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")

while True:
    print("1-Add an expense/income")
    print("2-Remove a transaction")
    print("3-See your transactions")
    print("4-Edit your transactions")
    print("5-Exit")

    opr = input("Please enter your operaiton: ")

    if (opr.isdigit() == False or int(opr) < 1 or int(opr) > 5):
        print("Please enter a valid operation!")
        break

    elif (opr == "1"):
        add_transaction()

    elif (opr == "2"):
        delete_transaction()
    
    elif (opr == "3"):
       list_transactions()

    elif (opr == "5"):
        print("Terminating the program...")
        break