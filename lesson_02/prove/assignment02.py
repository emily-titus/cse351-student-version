"""
Course    : CSE 351
Assignment: 02
Student   : <Emily Titus>

Instructions:
    - review instructions in the course
"""

# Don't import any other packages for this assignment
import os
import random
import threading
from money import *
from cse351 import *

# ---------------------------------------------------------------------------
def main(): 

    print('\nATM Processing Program:')
    print('=======================\n')

    create_data_files_if_needed()

    # Load ATM data files
    data_files = get_filenames('data_files')
    # print(data_files)
    
    log = Log(show_terminal=True)
    log.start_timer()
    bankdict={ 1: Money("0"), 2: Money("0"), 3: Money("0"), 4: Money("0"), 5: Money("0"), 6: Money("0"), 7: Money("0"), 8: Money("0"), 9: Money("0"), 10: Money("0"), 11: Money("0"), 12: Money("0"), 13: Money("0"), 14: Money("0"), 15: Money("0"), 16: Money("0"), 17: Money("0"), 18: Money("0"), 19: Money("0"), 20: Money("0")}
    bank = Bank(bankdict)

    # TODO - Add a ATM_Reader for each data file
    atm1 = ATM_Reader(data_files[0], bank)
    atm2 = ATM_Reader(data_files[1], bank)
    atm3 = ATM_Reader(data_files[2], bank)
    atm4 = ATM_Reader(data_files[3], bank)
    atm5 = ATM_Reader(data_files[4], bank)
    atm6 = ATM_Reader(data_files[5], bank)
    atm7 = ATM_Reader(data_files[6], bank)
    atm8 = ATM_Reader(data_files[7], bank)
    atm9 = ATM_Reader(data_files[8], bank)
    atm10 = ATM_Reader(data_files[9], bank)
    
    atm1.start()
    atm2.start()
    atm3.start()
    atm4.start()
    atm5.start()
    atm6.start()
    atm7.start()
    atm8.start()
    atm9.start()
    atm10.start()

    atm1.join()
    atm2.join()
    atm3.join()
    atm4.join()
    atm5.join()
    atm6.join()
    atm7.join()
    atm8.join()
    atm9.join()
    atm10.join()
    test_balances(bank)

    log.stop_timer('Total time')


# ===========================================================================
class ATM_Reader(threading.Thread):
    # TODO - implement this class here
    ...
    
    def __init__(self, data_file, bank):
        threading.Thread.__init__(self)
        self.data_file = data_file
        self.bank = bank

    def run(self,):
        with open(self.data_file) as f:
            next(f)
            next(f)
            for line in f:
                account_num = int(line.split(",")[0])
                type = line.split(",")[1]
                amount = Money(line.split(",")[2])
                if type == "w":
                   self.bank.withdraw(account_num, amount)
                else:
                    self.bank.deposit(account_num, amount)


# ===========================================================================
class Account():
    # TODO - implement this class here
    ...

    money = Money("")

    def __init__(self, money):
        self.money = money

    def get_balance(self):
        return self.money
        

# ===========================================================================
class Bank():
    # TODO - implement this class here
    ...

    accountsdict = {

    }
    def __init__(self,dict):
        self.accountsdict = dict

    def deposit(self, account, amount):
        camount = Money(str(amount)) 
        current = self.accountsdict[int(account)]
        newamount=Money("000")
        newamount.digits = current._Money__add(current.digits, camount.digits)
        print(f"New balance after deposit: {newamount}")
        self.accountsdict[int(account)]=newamount

    def withdraw(self, account, amount): 
        camount = Money(str(amount)) 
        current = self.accountsdict[int(account)]
        newamount=Money("000")
        newamount.digits = current._Money__sub(current.digits, camount.digits)
        print(f"New balance after deposit: {newamount}")
        self.accountsdict[int(account)]=newamount
    def get_balance(self, account):
        return self.accountsdict.get(int(account))

    
        


# ---------------------------------------------------------------------------

def get_filenames(folder):
    """ Don't Change """
    filenames = []
    for filename in os.listdir(folder):
        if filename.endswith(".dat"):
            filenames.append(os.path.join(folder, filename))
    return filenames

# ---------------------------------------------------------------------------
def create_data_files_if_needed():
    """ Don't Change """
    ATMS = 10
    ACCOUNTS = 20
    TRANSACTIONS = 250000

    sub_dir = 'data_files'
    if os.path.exists(sub_dir):
        return

    print('Creating Data Files: (Only runs once)')
    os.makedirs(sub_dir)

    random.seed(102030)
    mean = 100.00
    std_dev = 50.00

    for atm in range(1, ATMS + 1):
        filename = f'{sub_dir}/atm-{atm:02d}.dat'
        print(f'- {filename}')
        with open(filename, 'w') as f:
            f.write(f'# Atm transactions from machine {atm:02d}\n')
            f.write('# format: account number, type, amount\n')

            # create random transactions
            for i in range(TRANSACTIONS):
                account = random.randint(1, ACCOUNTS)
                trans_type = 'd' if random.randint(0, 1) == 0 else 'w'
                amount = f'{(random.gauss(mean, std_dev)):0.2f}'
                f.write(f'{account},{trans_type},{amount}\n')

    print()

# ---------------------------------------------------------------------------
def test_balances(bank):
    """ Don't Change """

    # Verify balances for each account
    correct_results = (
        (1, '59362.93'),
        (2, '11988.60'),
        (3, '35982.34'),
        (4, '-22474.29'),
        (5, '11998.99'),
        (6, '-42110.72'),
        (7, '-3038.78'),
        (8, '18118.83'),
        (9, '35529.50'),
        (10, '2722.01'),
        (11, '11194.88'),
        (12, '-37512.97'),
        (13, '-21252.47'),
        (14, '41287.06'),
        (15, '7766.52'),
        (16, '-26820.11'),
        (17, '15792.78'),
        (18, '-12626.83'),
        (19, '-59303.54'),
        (20, '-47460.38'),
    )

    wrong = False
    for account_number, balance in correct_results:
        bal = bank.get_balance(account_number)
        print(f'{account_number:02d}: balance = {bal}')
        if Money(balance) != bal:
            wrong = True
            print(f'Wrong Balance: account = {account_number}, expected = {balance}, actual = {bal}')

    if not wrong:
        print('\nAll account balances are correct')



if __name__ == "__main__":
    main()

