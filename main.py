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

def show_summary():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()

    c.execute("SELECT SUM(amount) FROM transactions WHERE type = 'income'")

    incomes = c.fetchone()[0] or 0

    c.execute("SELECT SUM(amount) FROM transactions WHERE type = 'expense'")

    expenses = c.fetchone()[0] or 0

    balance = incomes - expenses

    conn.close()

    print("Total income:", incomes)
    print("Total expenses:", expenses)
    print("Balance:", balance)

def edit_transaction():
   while True:
        id = input("Enter transaction ID: ")
        
        conn = sqlite3.connect('finance.db')
        c = conn.cursor()

        while True:
            print("1-Amount")
            print("2-Type")
            print("3-Category")
            print("4-Date")
            print("5-Description")
            print("6-Edit another transaction")
            print("7-Return to the main menu")

            eOpr = input("Please enter your operation: ")
            
            if (eOpr.isdigit() == False or int(eOpr) < 1 or int(eOpr) > 7):
                print("Please enter a valid operation!")
                break
            elif (eOpr == "1"):
                newAmount = input("New amount: ")
                c.execute ("UPDATE transactions  SET amount = ? WHERE id = ?", (newAmount, id))
            
            elif (eOpr == "2"):
                newType = input("New type: ")
                c.execute ("UPDATE transactions SET type = ? WHERE id = ?", (newType, id))

            elif (eOpr == "3"):
                newCategory = input("New category: ")
                c.execute ("UPDATE transactions SET category = ? WHERE id = ?", (newCategory, id))
        
            elif (eOpr == "4"):
                newDate = input("New date (DD-MM-YYYY): ")
                c.execute ("UPDATE transactions SET date = ? WHERE id = ?", (newDate, id))

            elif (eOpr == "5"):
                newDescription = input("New description: ")
                c.execute ("UPDATE transactions SET description = ? WHERE id = ?", (newDescription, id))
            
            elif (eOpr == "6"):
                break

            elif (eOpr == "7"):
                print("Returning to the main menu.")
                return
            
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
    print("5-Show summary")
    print("6-Exit")

    opr = input("Please enter your operaiton: ")

    if (opr.isdigit() == False or int(opr) < 1 or int(opr) > 6):
        print("Please enter a valid operation!")
        continue

    elif (opr == "1"):
        add_transaction()

    elif (opr == "2"):
        delete_transaction()
    
    elif (opr == "3"):
       list_transactions()

    elif (opr == "4"):
        edit_transaction()

    elif (opr == "5"):
        show_summary()

    elif (opr == "6"):
        print("Terminating the program...")
        break