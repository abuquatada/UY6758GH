import unittest
import sqlite3
from Logic import *
import os
import tempfile

# Create an in-memory SQLite database for testing
class TestFinanceApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a connection to a new in-memory SQLite database
        cls.conn = sqlite3.connect(':memory:')
        cls.cursor = cls.conn.cursor()

        # Set up the database schema
        cls.cursor.execute('''
            CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)
        ''')
        cls.cursor.execute('''
            CREATE TABLE income (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, amount REAL, category TEXT, description TEXT, date TEXT)
        ''')
        cls.cursor.execute('''
            CREATE TABLE expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, amount REAL, category TEXT, description TEXT, date TEXT)
        ''')
        cls.cursor.execute('''
            CREATE TABLE budgets (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, category TEXT, budget_amount REAL)
        ''')
        cls.conn.commit()

    def test_hash_password(self):
        password = "test123"
        hashed_password = hash_password(password)
        self.assertEqual(len(hashed_password), 64)

    def test_register_user(self):
        # Register a new user with the in-memory database cursor
        register_user("testuser", "password123", self.cursor, self.conn)
        self.cursor.execute("SELECT * FROM users WHERE username = 'testuser'")
        user = self.cursor.fetchone()
        self.assertIsNotNone(user)
        self.assertEqual(user[1], "testuser")

    def test_login_success(self):
        # Register a user and test successful login
        register_user("testuser2", "password123",self.cursor,self.conn)
        result = login("testuser2", "password123",self.cursor)
        self.assertTrue(result)

    def test_add_income(self):
        # Add an income entry and check if it is stored correctly
        add_income(1, 1000, 'Salary', 'March Salary', '2024-03-01',self.cursor, self.conn)
        self.cursor.execute("SELECT * FROM income WHERE user_id = 1")
        income = self.cursor.fetchone()
        self.assertIsNotNone(income)
        self.assertEqual(income[2], 1000)

    def test_add_expense(self):
        # Add an expense entry and check if it is stored correctly
        add_expense(1, 200, 'Groceries', 'March groceries', '2024-03-05',self.cursor, self.conn)
        self.cursor.execute("SELECT * FROM expenses WHERE user_id = 1")
        expense = self.cursor.fetchone()
        self.assertIsNotNone(expense)
        self.assertEqual(expense[2], 200)

    def test_generate_report(self):
        # Add income and expense, then generate a report
        add_income(1, 2000, 'Freelance', 'Website development', '2024-03-10', self.cursor, self.conn)
        add_expense(1, 300, 'Entertainment', 'Movie tickets', '2024-03-12', self.cursor, self.conn)
        report = generate_report(1, self.cursor, month=3, year=2024)
        print('\n\n\n',f"meri report {report}",'\n\n\n')
        self.assertIn("Total Income : $3000", report)
        self.assertIn("Total Expenses: $650", report)
        
    def test_set_budget(self):
        # Set a budget and check if it is stored correctly
        set_budget(1, 'Groceries', 300.00, self.cursor, self.conn)
        self.cursor.execute("SELECT * FROM budgets WHERE user_id = 1 AND category = 'Groceries'")
        budget = self.cursor.fetchone()
        self.assertIsNotNone(budget)
        self.assertEqual(budget[3], 300.00)  

    
    def test_budget_exceeded(self):
        # Set a budget and add expenses to exceed it
        set_budget(1, 'Entertainment', 150.00, self.cursor, self.conn)

        # Add expenses
        add_expense(1, 100.00, 'Entertainment', 'Movie tickets', '2024-03-01', self.cursor, self.conn)
        add_expense(1, 100.00, 'Entertainment', 'Concert tickets', '2024-03-05', self.cursor, self.conn)

        # Check if the budget is exceeded
        exceeded = check_budget(1, 'Entertainment', self.cursor)
        self.assertTrue(exceeded) 
       
       
    def test_budget_not_exceeded(self):
        # Clear previous expenses for this test to prevent interference
        self.cursor.execute('DELETE FROM expenses WHERE user_id = 1 AND category = "Groceries"')
        self.conn.commit()

        # Set a budget of $300 for 'Groceries'
        set_budget(1, 'Groceries', 300.00, self.cursor, self.conn)

        # Add expenses that are within the budget
        add_expense(1, 100.00, 'Groceries', 'Weekly groceries', '2024-03-01', self.cursor, self.conn)
        add_expense(1, 50.00, 'Groceries', 'Fruits and vegetables', '2024-03-05', self.cursor, self.conn)

        # Total expenses = 100 + 50 = 150 (which is within the $300 budget)
        exceeded = check_budget(1, 'Groceries', self.cursor)

        # Print total expenses for debugging
        self.cursor.execute('SELECT SUM(amount) FROM expenses WHERE user_id = 1 AND category = "Groceries"')
        total_expense = self.cursor.fetchone()[0]
        print(f"Total expenses for Groceries: {total_expense}")  # Should print 150.00

        # Assert that the budget has not been exceeded
        self.assertFalse(exceeded)


        
        
    def setUp(self):
        # Create a temporary directory for the test database and backup
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_db = os.path.join(self.test_dir.name, 'finance.db')
        self.backup_db = os.path.join(self.test_dir.name, 'backup_finance.db')

        # Create a dummy SQLite database
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
        cursor.execute("INSERT INTO users (username, password) VALUES ('testuser', 'testpassword')")
        conn.commit()
        conn.close()

    def tearDown(self):
        # Cleanup the temporary directory
        self.test_dir.cleanup()

    def test_backup_database(self):
        # Perform the backup
        backup_database(source_db=self.test_db, backup_db=self.backup_db)

        # Check if the backup file exists
        self.assertTrue(os.path.exists(self.backup_db))

        # Verify that the content of the backup is the same as the original
        conn_original = sqlite3.connect(self.test_db)
        conn_backup = sqlite3.connect(self.backup_db)

        cursor_original = conn_original.cursor()
        cursor_backup = conn_backup.cursor()

        cursor_original.execute('SELECT * FROM users')
        cursor_backup.execute('SELECT * FROM users')

        original_data = cursor_original.fetchall()
        backup_data = cursor_backup.fetchall()

        self.assertEqual(original_data, backup_data)

        conn_original.close()
        conn_backup.close()

    def test_restore_database(self):
        # Perform the backup first
        backup_database(source_db=self.test_db, backup_db=self.backup_db)

        # Delete the original database to simulate a restore scenario
        os.remove(self.test_db)

        # Perform the restore
        restore_database(backup_db=self.backup_db, target_db=self.test_db)

        # Check if the restored database exists
        self.assertTrue(os.path.exists(self.test_db))

        # Verify that the restored database contains the same data
        conn_restored = sqlite3.connect(self.test_db)
        cursor_restored = conn_restored.cursor()

        # Fetch the data from the restored database
        cursor_restored.execute('SELECT * FROM users')
        restored_data = cursor_restored.fetchall()

        # Compare the restored data, including the id column
        self.assertEqual(restored_data, [(1, 'testuser', 'testpassword')])

        conn_restored.close()
               

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

if __name__ == '__main__':
    unittest.main()
