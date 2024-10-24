from Logic import *
# Step 1: User Registration and Authentication (Days 1-5)
user_input = input("Type 'si' for Sign_In\nType 'su' for Sign_Up: ").lower()

if user_input == "su":
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    register_user(username, password,cursor,conn)
elif user_input == "si":
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    user_id = login(username, password,cursor)
    if user_id:
        print("Login successful!")

        # Main menu after successful login
        while True:
            print("\nMain Menu:")
            print("1. Add Income")
            print("2. Add Expense")
            print("3. Update Income/Expense")
            print("4. Delete Income/Expense")
            print("5. Generate Financial Report")
            print("6. Set Monthly Budget")
            print("7. Check Budget Status")
            print("8. Calculate Total Income, Expenses, and Savings")
            print("9. Exit")
            user_action = input("Enter the number of your choice: ")

            # Step 2: Income and Expense Tracking (Days 6-10)
            if user_action == "1":
                # Add Income
                amount = float(input("Enter income amount: "))
                category = input("Enter income category (e.g., Salary, Freelance): ")
                description = input("Enter description: ")
                date = input("Enter the date (YYYY-MM-DD) or leave blank for today date ")
                if date:
                    pass
                else:
                    date=str(datetime.date.today())
                    
                add_income(user_id, amount, category, description,date,cursor,conn)

            elif user_action == "2":
                # Add Expense
                amount = float(input("Enter expense amount: "))
                category = input("Enter expense category (e.g., Rent, Groceries): ")
                description = input("Enter description: ")
                date = input("Enter the date (YYYY-MM-DD) or leave blank for today date ")
                if date:
                    pass
                else:
                    date=str(datetime.date.today())
                add_expense(user_id, amount, category, description,date,cursor,conn)

                # Check if expense exceeds budget
                check_budget(user_id, category)

            elif user_action == "3":
                # Update Income/Expense
                table = input("Enter 'income' to update income or 'expense' to update expense: ").lower()
                entry_id = int(input(f"Enter the {table} entry ID to update: "))
                amount = float(input(f"Enter new {table} amount: "))
                category = input(f"Enter new {table} category: ")
                description = input(f"Enter new {table} description: ")
                update_entry(table, entry_id, amount, category, description,cursor,conn)

            elif user_action == "4":
                # Delete Income/Expense
                table = input("Enter 'income' to delete income or 'expense' to delete expense: ").lower()
                entry_id = int(input(f"Enter the {table} entry ID to delete: "))
                delete_entry(table, entry_id,cursor,conn)

            # Step 3: Financial Reports (Days 11-15)
            elif user_action == "5":
                report_type = input("Generate report for 'month', 'year', or leave blank for all time: ").lower()
                if report_type == "month":
                    month = int(input("Enter month (1-12): "))
                    year = int(input("Enter year: "))
                    generate_report(user_id,cursor,month=month, year=year)
                elif report_type == "year":
                    year = int(input("Enter year: "))
                    generate_report(user_id,cursor,year=year)
                else:
                    generate_report(user_id,cursor)

            # Step 4: Set Monthly Budget (Days 16-20)
            elif user_action == "6":
                category = input("Enter category to set budget for (e.g., Rent, Groceries): ")
                budget_amount = float(input(f"Enter monthly budget for {category}: "))
                set_budget(user_id, category, budget_amount,cursor,conn)

            # Step 5: Check Budget Status
            elif user_action == "7":
                category = input("Enter category to check budget for (e.g., Rent, Groceries): ")
                check_budget(user_id, category,cursor)

            # Step 6: Calculate Total Income, Expenses, and Savings
            elif user_action == "8":
                # Ask for period (monthly/yearly) or leave it blank for all time
                period_type = input("Calculate for 'month', 'year', or leave blank for all time: ").lower()
                if period_type == "month":
                    month = int(input("Enter month (1-12): "))
                    year = int(input("Enter year: "))
                    calculation_(user_id, period='monthly', month=month, year=year)
                elif period_type == "year":
                    year = int(input("Enter year: "))
                    calculation_(user_id, period='yearly', year=year)
                else:
                    calculation_(user_id)

            elif user_action == "9":
                print("Exiting the application...")
                break

            else:
                print("Invalid choice. Please try again.")

    else:
        print("Login failed.")
