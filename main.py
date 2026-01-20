import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()

    try:
        c.execute("""CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                t_type  TEXT NOT NULL,
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

def is_date_valid(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    
    except ValueError:
        return False

def add_transaction():
    while True:
        transaction_type = input("Would you like to add an income or an expense (income/expense): ").lower()
        
        if (transaction_type == "income" or transaction_type == "expense"):
            break

        else:
            print("Please enter a valid type!")
    
    while True:
        try:
            amount = float(input("Amount: "))
            if (amount <= 0):
                print("Amount must be positive!")
                continue
            break
        
        except ValueError:
            print("Please enter a valid number")
        
    while True:
        category = input("Category: ").lower()

        if not category.strip():
            print("Please enter a category!")
        else:
            break
    
    while True:
        date = input("Date (YYYY-MM-DD): ")

        if not date.strip():
            print("Please enter a date!")
        
        elif not is_date_valid(date):
            print("Please enter a valid date!")
        
        else:
            break

    description = input("Description (optional): ")
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect('finance.db')
    c = conn.cursor()

    c.execute("""INSERT INTO transactions (t_type, amount, category, date, description, created_at)
              VALUES (?, ?, ?, ?, ?, ?)""", 
              (transaction_type, amount, category, date, description, created_at))
    conn.commit()
    conn.close()

    print("Transaction added succesfully!")

def list_transactions():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()

    try:
        print("1-See all your transactions")
        print("2-See your incomes")
        print("3-See your expenses")
        print("4-Return to main menu")

        seeOpr = input("Please enter your operation: ")

        if (seeOpr.isdigit() == False or int(seeOpr) < 1 or int(seeOpr) > 4):
            print("Please enter a valid operation!")
        
        elif (seeOpr == "4"):
            print("Returning to the main menu.")
            return
            
        elif (seeOpr == "1"):

            c.execute("SELECT * FROM transactions")
            rows = c.fetchall()

            if not rows:
                print("There aren't any transactions!")
                return

            for row in rows:
                print(row)

        elif (seeOpr == "2" or seeOpr == "3"):
            if (seeOpr == "2"):
                t_type = "income"
            else:
                t_type = "expense"

            c.execute("SELECT * FROM transactions WHERE t_type = ?", (t_type,))

            rows = c.fetchall()

            if not rows:
                if (seeOpr == "2"):
                    print("There aren't any incomes!")
                else:
                    print("There aren't any expenses!")
            
                return
            
            for row in rows:
                print(row)
            
    except sqlite3.Error as e:
        print("Database error found: ", e)
        return
    
    finally:
        conn.close()

def delete_transaction():
    try:
        conn = sqlite3.connect('finance.db')
        c = conn.cursor()
        
        while True:
            print("Please enter transaction ID to delete")
            id = input("Write \"exit\" to return to the main menu: ")

            if (id.lower() == "exit"):
                print("Returning to the main menu.")
                return

            if not id.isdigit() or int(id) <= 0:
                print("Invalid ID")
                continue

            c.execute("SELECT * FROM transactions WHERE id = ?", (id,))

            row = c.fetchone()

            if row == None:
                print("There are no transactions with this ID!")
            
            else:
                c.execute("DELETE FROM transactions WHERE id = ?", (id,))
                conn.commit()
                print("Transaction deleted successfully!")
                break
    
    except sqlite3.Error as e:
        print("Databese error found: ", e)
        return

    finally:
        conn.close()

def show_summary():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()

    c.execute("SELECT SUM(amount) FROM transactions WHERE t_type = 'income'")

    incomes = c.fetchone()[0] or 0

    c.execute("SELECT SUM(amount) FROM transactions WHERE t_type = 'expense'")

    expenses = c.fetchone()[0] or 0

    balance = incomes - expenses

    conn.close()

    print("Total income:", incomes)
    print("Total expenses:", expenses)
    print("Balance:", balance)

def edit_transaction():
    try:
        conn = sqlite3.connect('finance.db')
        c = conn.cursor()
        
        while True:
            id = input("Enter transaction ID: ")
            
            

            if not id.isdigit() or int(id) <= 0:
                print("Invalid ID")
                break
            
            c.execute("SELECT * FROM transactions WHERE id = ?", (id,))

            row = c.fetchone()

            if row == None:
                print("There are no transactions with this ID!")

            else:

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
                        while True:
                            try:
                                newAmount = float(input("Amount: "))
                                if (newAmount <= 0):
                                    print("Amount must be positive!")
                                    continue
                                break
                            
                            except ValueError:
                                print("Please enter a valid number")
                       
                        c.execute ("UPDATE transactions  SET amount = ? WHERE id = ?", (newAmount, id))
                    
                    elif (eOpr == "2"):
                        while True:
                            newType = input("Would you like to add an income or an expense (income/expense): ").lower()
            
                            if (newType == "income" or newType == "expense"):
                                break

                            else:
                                print("Please enter a valid type!")
                        
                        c.execute ("UPDATE transactions SET t_type = ? WHERE id = ?", (newType, id))

                    elif (eOpr == "3"):
                        newCategory = input("New category: ")
                        c.execute ("UPDATE transactions SET category = ? WHERE id = ?", (newCategory, id))
                
                    elif (eOpr == "4"):

                        while True:
                            
                            newDate = input("New date (YYYY-MM-DD): ")
                            
                            if not newDate.strip():
                                print("Please enter a date!")
        
                            elif not is_date_valid(newDate):
                                print("Please enter a valid date!")
        
                            else:
                                break
                
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
    
    except sqlite3.Error as e:
        print("Database error found: ", e)
        return

    finally:
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