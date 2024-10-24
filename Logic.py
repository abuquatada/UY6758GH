"""                                                        Project Id: UY6758GH
                                            Task: Develop a Personal Finance Management Application



Objective:
Create a command-line application that helps users manage their personal finances by tracking
income, expenses, and generating financial reports.

"""

from DBAL import *
import datetime


""" 1. User Registration and Authentication (Days 1-5):
    - Implement user registration with unique usernames and passwords.
    - Add login functionality to authenticate users.
"""

# Function for Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to Register new user
def register_user(username,password,cursor,conn):
    try:
        hashed_password = hash_password(password)
        cursor.execute(f'INSERT INTO users (username, password) VALUES ("{username}","{hashed_password}")')
        conn.commit()
        print(f"User {username} registered successfully!")
    except sqlite3.IntegrityError:
        print("Username already exists. Please choose another username.")


# Login function
def login(username,password,cursor):
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    if user and user[2] == hash_password(password):
        print(f"Welcome back, {username}!")
        return user[0]
    else:
        print("Invalid username or password.")
        return False


# -----------------------------------------------------------------------------------------------------------

""" 2. Income and Expense Tracking (Days 6-10):
    - Allow users to add, update, and delete income and expense entries.
    - Categorize transactions (e.g., Food, Rent, Salary, etc.).
"""


# Add income
def add_income(user_id, amount, category, description,date,cursor,conn):
    cursor.execute('INSERT INTO income (user_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)', 
                   (user_id, amount, category, description, date))
    conn.commit()
    print("Income added successfully.")
          


# Add expense
def add_expense(user_id, amount, category, description,date,cursor,conn):
    
    cursor.execute('INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)', 
                   (user_id, amount, category, description, date))
    conn.commit()
    print("Expense added successfully.")



# Update income or expense
def update_entry(table, entry_id, amount, category, description,cursor=None,conn=None):
    cursor.execute(f'UPDATE {table} SET amount = ?, category = ?, description = ? WHERE id = ?', 
                   (amount, category, description, entry_id))
    conn.commit()
    print(f"{table.capitalize()} entry updated successfully.")
        

# Delete entry
def delete_entry(table, entry_id,cursor=None,conn=None):
    cursor.execute(f'DELETE FROM {table} WHERE id = ?', (entry_id,))
    conn.commit()
    print(f"{table.capitalize()} entry deleted successfully.")
    
   
    
##---------------------------------------------------------------------------------------------------
""" 3. Financial Reports (Days 11-15):
    - Generate monthly and yearly financial reports.
    - Calculate total income, expenses, and savings.
"""


def generate_report(user_id, cursor,month=None, year=None):
    # Build the date filter based on the input parameters
    date_filter = ""
    params = [user_id]

    if month and year:
        # Filter by specific month and year
        date_filter = "AND strftime('%Y-%m', date) = ?"
        date_value = f"{year}-{int(month):02d}"
        params.append(date_value)
    elif year:
        # Filter by specific year
        date_filter = "AND strftime('%Y', date) = ?"
        date_value = f"{year}"
        params.append(date_value)

    # Query total income
    cursor.execute(f'''
        SELECT SUM(amount) FROM income
        WHERE user_id = ? {date_filter}
    ''', params)
    total_income = cursor.fetchone()[0] or 0

    # Query total expenses
    cursor.execute(f'''
        SELECT SUM(amount) FROM expenses
        WHERE user_id = ? {date_filter}
    ''', params)
    total_expense = cursor.fetchone()[0] or 0

    # Calculate savings
    savings = total_income - total_expense

    # Generate the report title
    if month and year:
        report_title = f"Financial Report for {datetime.date(year, int(month), 1):%B %Y}"
    elif year:
        report_title = f"Financial Report for the Year {year}"
    else:
        report_title = "Overall Financial Report"

    # Display the report
    print("\n" + "=" * len(report_title))
    print(report_title)
    print("=" * len(report_title))
    print(f"Total Income : ${total_income:.2f}")
    print(f"Total Expenses: ${total_expense:.2f}")
    print(f"Savings      : ${savings:.2f}\n")
    
    report = f"\n{report_title}\n{'=' * len(report_title)}\n"
    report += f"Total Income : ${total_income:.2f}\n"
    report += f"Total Expenses: ${total_expense:.2f}\n"
    report += f"Savings      : ${savings:.2f}\n"
    
    return report


# Calculation of total income ,expenses and savings
def calculation_(user_id, period='monthly', month=None, year=None):
    # Filter based on the period (monthly/yearly/all-time)
    date_filter = ""
    params = [user_id]

    if period == 'monthly' and month and year:
        date_filter = "AND strftime('%Y-%m', date) = ?"
        date_value = f"{year}-{int(month):02d}"
        params.append(date_value)
    elif period == 'yearly' and year:
        date_filter = "AND strftime('%Y', date) = ?"
        params.append(str(year))

    # Query total income
    cursor.execute(f"SELECT SUM(amount) FROM income WHERE user_id = ? {date_filter}", params)
    total_income = cursor.fetchone()[0] or 0

    # Query total expenses
    cursor.execute(f"SELECT SUM(amount) FROM expenses WHERE user_id = ? {date_filter}", params)
    total_expense = cursor.fetchone()[0] or 0

    # Calculate savings
    savings = total_income - total_expense

    # Display the results
    print(f"\nCalculation Results for {period.capitalize()}:")
    print(f"Total Income    : ${total_income:.2f}")
    print(f"Total Expenses  : ${total_expense:.2f}")
    print(f"Savings         : ${savings:.2f}\n")




## ---------------------------------------------------

""" 4. Budgeting (Days 16-20):
    - Enable users to set monthly budgets for different categories.
    - Notify users when they exceed their budget limits.
"""

# Set budgets for categories
def set_budget(user_id, category, budget_amount,cursor,conn):
    cursor.execute('INSERT INTO budgets (user_id, category, budget_amount) VALUES (?, ?, ?)', 
                   (user_id, category, budget_amount))
    conn.commit()
    print(f"Budget for {category} set to {budget_amount}.")
    

# Notify when budget is exceeded
def check_budget(user_id, category, cursor):
    cursor.execute('SELECT budget_amount FROM budgets WHERE user_id = ? AND category = ?', (user_id, category))
    budget = cursor.fetchone()
    if budget:
        cursor.execute('SELECT SUM(amount) FROM expenses WHERE user_id = ? AND category = ?', (user_id, category))
        total_expense = cursor.fetchone()[0] or 0
        if total_expense > budget[0]:
            print(f"Warning: You have exceeded your budget for {category}!")
            return True  # Budget exceeded
    return False  # Budget not exceeded
  



##------------------------------------------------------------------------------------------------------------

"""5. Data Persistence (Days 21-23):
     - Store user data and transactions in a SQLite or any other database as per your preference.
     - Implement functions to back up and restore data.
"""
import shutil

## Backup the database
def backup_database(source_db='finance.db', backup_db='backup_finance.db'):
    shutil.copy(source_db, backup_db)
    print("Database backup created successfully.")
    
# backup_database()

## Restore the database
def restore_database(backup_db='backup_finance.db',target_db='finance.db'):
    shutil.copy(backup_db,target_db)
    print("Database restored successfully.")
# restore_database()


