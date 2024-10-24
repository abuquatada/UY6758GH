import sqlite3
import hashlib

# Connection to SQLite database
conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

# Create users table to store username and password
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()

# Create income table to store the income details
cursor.execute('''
    CREATE TABLE IF NOT EXISTS income (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        category TEXT,
        description TEXT,
        date DATE,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
''')
conn.commit()


# Create expenses table to store the expenses 
cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        category TEXT,
        description TEXT,
        date DATE,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
''')
conn.commit()

cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            category TEXT,
            budget_amount REAL,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')
conn.commit()




#---------------------------Dummy Data--------------------------
# cursor.execute('''INSERT INTO expenses (user_id, amount, category, description, date) VALUES 
# (1, 1500, 'Rent', 'January apartment rent', '2023-01-05'),
# (1, 300, 'Groceries', 'Monthly groceries', '2023-01-15'),
# (1, 200, 'Entertainment', 'Movie tickets', '2023-01-18'),
# (1, 150, 'Transport', 'Fuel expenses', '2023-01-20'),
# (1, 1500, 'Rent', 'February apartment rent', '2023-02-05'),
# (1, 350, 'Groceries', 'Monthly groceries', '2023-02-12'),
# (1, 100, 'Entertainment', 'Concert tickets', '2023-02-14'),
# (1, 200, 'Transport', 'Fuel expenses', '2023-02-20'),
# (1, 1600, 'Rent', 'March apartment rent', '2023-03-05'),
# (1, 400, 'Groceries', 'Monthly groceries', '2023-03-10'),
# (1, 250, 'Entertainment', 'Restaurant dining', '2023-03-18'),
# (1, 150, 'Transport', 'Fuel expenses', '2023-03-20'),
# (1, 1700, 'Rent', 'April apartment rent', '2023-04-05'),
# (1, 450, 'Groceries', 'Monthly groceries', '2023-04-12'),
# (1, 100, 'Entertainment', 'Museum visit', '2023-04-20');''')
# conn.commit()

# cursor.execute('''INSERT INTO income (user_id, amount, category, description, date) VALUES 
# (1, 5000, 'Salary', 'Monthly Salary', '2023-01-25'),
# (1, 200, 'Freelance', 'Website development', '2023-01-10'),
# (1, 500, 'Investments', 'Stock market returns', '2023-02-05'),
# (1, 6000, 'Salary', 'Monthly Salary', '2023-02-25'),
# (1, 1000, 'Freelance', 'App development', '2023-03-02'),
# (1, 700, 'Investments', 'Crypto trading profits', '2023-03-10'),
# (1, 6000, 'Salary', 'Monthly Salary', '2023-03-25'),
# (1, 500, 'Freelance', 'Content writing', '2023-04-15'),
# (1, 6500, 'Salary', 'Monthly Salary', '2023-04-25');''')
# conn.commit()

# cursor.execute('INSERT INTO budgets (user_id, category, budget_amount) VALUES (?, ?, ?)', (1, 'Rent', 1500.00))
# cursor.execute('INSERT INTO budgets (user_id, category, budget_amount) VALUES (?, ?, ?)', (1, 'Groceries', 300.00))
# cursor.execute('INSERT INTO budgets (user_id, category, budget_amount) VALUES (?, ?, ?)', (1, 'Utilities', 200.00))
# cursor.execute('INSERT INTO budgets (user_id, category, budget_amount) VALUES (?, ?, ?)', (1, 'Entertainment', 150.00))
# cursor.execute('INSERT INTO budgets (user_id, category, budget_amount) VALUES (?, ?, ?)', (1, 'Transport', 100.00))


# cursor.execute('INSERT INTO budgets (user_id, category, budget_amount) VALUES (?, ?, ?)', (2, 'Rent', 2000.00))
# cursor.execute('INSERT INTO budgets (user_id, category, budget_amount) VALUES (?, ?, ?)', (2, 'Groceries', 400.00))
# cursor.execute('INSERT INTO budgets (user_id, category, budget_amount) VALUES (?, ?, ?)', (2, 'Utilities', 250.00))
# cursor.execute('INSERT INTO budgets (user_id, category, budget_amount) VALUES (?, ?, ?)', (2, 'Entertainment', 200.00))
# cursor.execute('INSERT INTO budgets (user_id, category, budget_amount) VALUES (?, ?, ?)', (2, 'Transport', 150.00))
# conn.commit()