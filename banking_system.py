import os.path
import pickle
import tkinter
import sys

class BankingSystem:
    user_data = {}
    active_user = 'logged out'
    
    def __init__(self):
        # Do not add any parameter to this method.
        # Delete "pass" after adding code into this method.
        pass

    def run_app(self):
        print("")
        self.load_user_data()
        active_user = self.login()
        #self.display_menu(active_user)

        
    def load_user_data(self):
        if os.path.exists('user_data.pkl') == False:
            a1 = Admin('Arthur', '123', 'Admin')
            u1 = Customer('Boris', 'ABC', 'User', '10 London Road', [CurrentAcc(1000, 100)])
            u2 = Customer('Chloe', '1+x', 'User', '99 Queens Road', [CurrentAcc(1000,100), SavingAcc(4000, 0.0299)])
            u3 = Customer('David', 'aBC', 'User', '2 Birmingham Street', [SavingAcc(200, 0.0099), SavingAcc(5000, 0.0499)])
            user_data_temp = {}
            user_data_temp[a1.username] = a1
            user_data_temp[u1.username] = u1
            user_data_temp[u2.username] = u2
            user_data_temp[u3.username] = u3
            user_data_file = open('user_data.pkl', 'wb')
            pickle.dump(user_data_temp,user_data_file)
            user_data_file.close()
        elif os.path.exists('user_data.pkl') == True:
            pass
        
        user_data_file = open('user_data.pkl', 'rb')
        BankingSystem.user_data = pickle.load(user_data_file)
    
    def login(self):
        print("-"*50)
        print("")
        print("Welcome to the banking system, please log in first.")

        username_input = input("Please enter your username: ")
        password_input = input("Please enter your password: ")
        
        if username_input in BankingSystem.user_data:
            if password_input == self.user_data[username_input].password:
                active_user = username_input
                self.display_menu(active_user)
            
            else:
                print("Invalid username/password")
                self.login()
                       
        else:
            print("Invalid username/password")
            self.login()

    def display_menu(self, active_user):
        
        if BankingSystem.user_data[active_user].user_type == 'Admin':
            option = self.admin_menu()
            
            if option == '1':
                self.customer_summary()
            
            elif option == '2':
                self.financial_forecast()
                
            elif option == '3':
                print("Transfer Money GUI is not available now.")
            
            elif option == '4':
                print("Account Management GUI is not available now.")
            
            else:
                self.display_menu(active_user)

        
        elif BankingSystem.user_data[active_user].user_type == 'User':
            option = self.user_menu()
            
            if option == '1':
                self.account_list(active_user)
            
            elif option == '2':
                self.account_summary(active_user)
            
            elif option == '3':
                print("Bye.")
            
            else:
                self.display_menu(active_user)
                    
        
    def admin_menu(self):
        print("")
        print("Please select an option:")
        print("  1 - Customer Summary")
        print("  2 - Financial Forecast")
        print("  3 - Transfer Money - GUI")
        print("  4 - Account management - GUI")
        option = input("Enter a number to select your option: ")
        return option
    
    def user_menu(self):
        print("")
        print("Please select an option:")
        print("  1 - View account")
        print("  2 - View summary")
        print("  3 - Quit")
        option = input("Enter a number to select your option: ")
        return option
    
    def account_list(self, active_user):
        active_user_accounts = self.user_data[active_user].accounts
        number_of_accounts = len(active_user_accounts)
        print("")
        print("--Account list--")
        print("Please select an option:")
        
        for acc in range(0, number_of_accounts):
            print("{} - {}: £{:.2f}" .format(acc+1, active_user_accounts[acc].acctype, active_user_accounts[acc].balance))
        
        option = input("Enter a number to select your option: ")
        if option.isdigit() == False:
            self.account_list(active_user)
        
        elif option.isdigit() == True:
            option = int(option)

            if option > number_of_accounts:
                self.account_list(active_user)
            
            else:
                self.account_balance(active_user, option)
            
    def account_balance(self, active_user, option):
        selected_account = self.user_data[active_user].accounts[option-1]

        print("")
        print("You selected {} - {}: £{:.2f}".format(option, selected_account.acctype, selected_account.balance))
        print("Please select an option:")
        print("  1 - Deposit")
        print("  2 - Withdraw")
        print("  3 - Go Back")
        menu_option = input("Enter a number to select your option: ")
        
        if menu_option == '3':
            self.account_list(active_user)
        elif menu_option == '1':
            self.deposit(active_user, option)
        elif menu_option == '2':
            self.withdraw(active_user, option)
        else:
            self.account_balance(active_user, option)
        
    def deposit(self, active_user, option):
        funds_added = int(input("Enter the amount you wish to deposit: £"))
        if funds_added > 0:
            self.user_data[active_user].accounts[option-1].balance += funds_added
        elif funds_added <= 0:
            print("")
            print("Invalid value entered.")
            print("")
            self.deposit(active_user, option)

        user_data_file = open('user_Data.pkl', 'wb')
        pickle.dump(BankingSystem.user_data, user_data_file)
        user_data_file.close()
        
        self.account_list(active_user)
    
    def withdraw(self, active_user, option):
        funds_withdrawn = int(input("Enter the amount you wish to withdraw: £"))
        account_balance = self.user_data[active_user].accounts[option-1].balance
        if funds_withdrawn > 0:
            if self.user_data[active_user].accounts[option-1].acctype == 'Current Account':
                overdraft_limit = self.user_data[active_user].accounts[option-1].overdraft_limit
                if funds_withdrawn > account_balance + overdraft_limit:
                    print("")
                    print("Not enough funds to withdraw this amount.")
                    self.account_balance(active_user, option)
                else:
                    self.user_data[active_user].accounts[option-1].balance -= funds_withdrawn     
            elif self.user_data[active_user].accounts[option-1].acctype == 'Saving Account':
                if funds_withdrawn > account_balance:
                    print("")
                    print("Not enough funds to withdraw this amount.")
                    self.account_balance(active_user, option)
                elif funds_withdrawn <= account_balance:
                    self.user_data[active_user].accounts[option-1].balance -= funds_withdrawn
        elif funds_withdrawn <= 0:
            print("")
            print("Invalid value entered.")
            print("")
            self.withdraw(active_user, option)

        user_data_file = open('user_Data.pkl', 'wb')
        pickle.dump(BankingSystem.user_data, user_data_file)
        user_data_file.close()

        self.account_list(active_user)

    def account_summary(self, active_user):
        active_user_accounts = self.user_data[active_user].accounts
        number_of_accounts = len(active_user_accounts)
        total_balance = 0
        user_address = self.user_data[active_user].address
        for acc in range(0, number_of_accounts):
            total_balance += active_user_accounts[acc].balance
            
        print("")
        print("-----Summary-----")
        print("  1 - Number of Bank Accounts you have: {}".format(number_of_accounts))
        print("  2 - Total Balance of all Accounts: £{:.2f}".format(total_balance))
        print("  3 - Address: {}".format(user_address))
    
    def customer_summary(self):
        user_data_file = open('user_data.pkl', 'rb')
        BankingSystem.user_data = pickle.load(user_data_file)
        user1 = self.user_data['Boris']
        user2 = self.user_data['Chloe']
        user3 = self.user_data['David']
        users = user1, user2, user3
        user_bank_accounts = ''
        total_user_accounts = 0

        print("")
        for user in users:
            user_bank_accounts = self.user_data[user.username].accounts
            total_user_accounts = len(user_bank_accounts)
            
            print("-"*5)
            print("")
            print("User: {}".format(user.username))
            print("Address: {}".format(user.address))

            for acc in range(0, total_user_accounts):
                print("  Account Type: {}".format(user.accounts[acc].acctype))
                print("  Balance: £{:.2f}".format(user.accounts[acc].balance))
                if user.accounts[acc].acctype == 'Current Account':
                    print("  Overdraft Limit: £{:.2f}".format(user.accounts[acc].overdraft_limit))
                elif user.accounts[acc].acctype == 'Saving Account':
                    print("  Interest Rate: {:.2f}%".format(user.accounts[acc].interest_rate*100))
                print("")
        user_data_file.close()

    def financial_forecast(self):
        user_data_file = open('user_data.pkl', 'rb')
        BankingSystem.user_data = pickle.load(user_data_file)
        user1 = self.user_data['Boris']
        user2 = self.user_data['Chloe']
        user3 = self.user_data['David']
        users = user1, user2, user3

        for user in users:
            total_balance = 0
            forecast_balance = 0
            user_name = self.user_data[user.username].username
            user_bank_accounts = self.user_data[user.username].accounts
            total_user_accounts = len(user_bank_accounts)
            for acc in range(0, total_user_accounts):
                total_balance += user_bank_accounts[acc].balance
            for acc in range(0, total_user_accounts):
                if user_bank_accounts[acc].acctype == 'Current Account':
                    forecast_balance += user_bank_accounts[acc].balance
                elif user_bank_accounts[acc].acctype == 'Saving Account':
                    forecast_balance += user_bank_accounts[acc].balance + (user_bank_accounts[acc].balance * user_bank_accounts[acc].interest_rate)

            print("-"*5)
            print("")
            print("User: {}".format(user_name))
            print("Number of Accounts: {}".format(total_user_accounts))
            print("Total money in bank: £{:.2f}".format(total_balance))
            print("Total money in bank after one year: £{:.2f}".format(forecast_balance))
            print("")

        user_data_file.close()


class User:
    def __init__(self, username, password, user_type):
        self.username = username
        self.password = password
        self.user_type = user_type
                
class Admin(User):
    def __init__(self, username, password, user_type):
        self.username = username
        self.password = password
        self.user_type = user_type    
    
class Customer(User):
    def __init__(self, username, password, user_type, address, accounts):
        self.username = username
        self.password = password
        self.user_type = user_type
        self.address = address
        self.accounts = accounts

class Account:
    def __init__(self, balance):
        self.balance = balance

class CurrentAcc(Account):
    def __init__(self, balance, overdraft_limit, acctype='Current Account'):
        self.balance = balance
        self.overdraft_limit = overdraft_limit
        self.acctype = acctype


class SavingAcc(Account):
    def __init__(self, balance, interest_rate, acctype='Saving Account'):
        self.balance = balance
        self.interest_rate = interest_rate
        self.acctype = acctype

class Admin_GUI:
    def __init__(self):
        pass

    def update_string(self):
        self.example_text.set("potato")

    def next_page(self):
        self.frame1.destroy()

    
    def transfer_money_window(self):

        #open the new window with tkinter
        self.gui_mw = tkinter.Tk()
        #assign the title of the tkinter window
        self.gui_mw.title("Admin - Transfer Money")
        #assign the dimensions of the tkinter window
        self.gui_mw.geometry("400x300")

        #set up the window frames
        self.frame1 = tkinter.Frame(self.gui_mw)
        self.frame2 = tkinter.Frame(self.gui_mw)
        self.frame3 = tkinter.Frame(self.gui_mw)
        self.frame4 = tkinter.Frame(self.gui_mw)
        self.frame5 = tkinter.Frame(self.gui_mw)

        self.example_text=tkinter.StringVar()
        self.example_text.set("Please select the Accounts you\nwish to transfer money between.")

        self.label1 = tkinter.Label(self.frame1, textvariable=self.example_text)
        self.button1 = tkinter.Button(self.frame1, text="test button", command=self.update_string)
        self.button2 = tkinter.Button(self.frame2, text="test butto2", command=self.next_page)

        self.button1.pack()
        self.button2.pack()

        self.label1.pack()

        self.frame1.pack()
        self.frame2.pack()
        self.frame3.pack()
        self.frame4.pack()
        self.frame5.pack()

        self.gui_mw.attributes('-topmost',True)

        self.gui_mw.mainloop()
