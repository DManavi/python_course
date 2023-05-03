#######################################
# Helper functions
#######################################

def input_int(prompt):
    return int(input(prompt))


def input_account_number(prompt="Account#> "):
    account_no = input(prompt)

    if len(account_no) == 0:
        print("No account entered.")

    return account_no


def get_account_balance_by_no(account_no):
    file_name = f"{account_no}.txt"

    account_balance = 0

    with open(file_name) as account_file:
        for transaction in account_file.readlines():
            account_balance += int(transaction.strip("\n"))

    return account_balance

#######################################
# Sub applications
#######################################


def login():
    """
    Returns (login status, username)
    """

    logged_in = False
    username = None
    invalid_login_count = 0

    while logged_in == False and invalid_login_count < 3:
        temp_username = input("Username> ")
        temp_password = input("Password> ")

        user_credentials = f"{temp_username}:{temp_password}"

        # check user/pass
        with open("./users.txt") as users_file:

            # read each line
            for correct_credentials in users_file.readlines():
                # check user/pass
                if user_credentials == correct_credentials.strip("\n"):
                    username = temp_username
                    logged_in = True
                    break

        if logged_in == False:
            # increase counter
            print("Invalid username or password. Try again!")
            invalid_login_count += 1

    #
    return (logged_in, username)


def menu():
    print("Please choose the option: ")
    print("1) Balance")
    print("2) Transactions")
    print("3) Deposit")
    print("4) Withdraw")
    print("5) Transfer")
    print("6) New Account")
    print("0) Logout")

    user_input = input_int("Operation> ")

    return user_input


def get_account_balance():
    account_no = input_account_number()
    if len(account_no) == 0:
        return

    account_balance = get_account_balance_by_no(account_no)

    print(f"Account #{account_no} balance is ${account_balance}")


def get_account_transactions():
    account_no = input_account_number()
    if len(account_no) == 0:
        return

    file_name = f"{account_no}.txt"

    print("-*-*" * 20)

    with open(file_name) as account_file:
        for transaction in account_file.readlines():
            amount = int(transaction.strip("\n"))

            # positive / deposit
            if amount > 0:
                print(f"Deposit ${amount}")
            # negative / withdraw
            else:
                print(f"Withdraw $({amount})")

            print("-" * 80)

    print()
    print("-*-*" * 20)


def deposit():
    # account
    account_no = input_account_number()
    if len(account_no) == 0:
        return

    # amount
    amount = input_int("Amount> ")

    # deposit > 0
    if amount < 1:
        print("Amount must be greater than 0")
        return

    file_name = f"{account_no}.txt"

    with open(file_name, "a") as account_file:
        account_file.write(f"\n{amount}")

    print(f"${amount} was depositted to #{account_no}.")

    new_balance = get_account_balance_by_no(account_no) + amount
    print(f"{account_no} new balance is ${new_balance}")


def withdraw():
    # account
    account_no = input_account_number()
    if len(account_no) == 0:
        return

    # amount
    amount = input_int("Amount> ")

    # check
    current_account_balance = get_account_balance_by_no(account_no)

    if current_account_balance < amount:
        print("Insufficient fund!")
        print(f"Maximum allowed amount is ${current_account_balance}")
        return

    file_name = f"{account_no}.txt"

    with open(file_name, "a") as account_file:
        account_file.write(f"\n{amount * -1}")

    print(f"${amount} was withdrawn from #{account_no}.")
    print(f"{account_no} new balance is ${current_account_balance - amount * -1}")


def transfer():

    # from
    source_account = input_account_number("Source Account#> ")
    if len(source_account) == 0:
        return

    # to
    dest_account = input_account_number("Dest. Account#> ")
    if len(dest_account) == 0:
        return

    # amount
    amount = input_int("Amount> ")

    # check
    current_source_account_balance = get_account_balance_by_no(source_account)

    if current_source_account_balance < amount:
        print("Insufficient fund!")
        print(f"Maximum allowed amount is ${current_source_account_balance}")
        return

    # withdraw (from source)
    source_account_file_name = f"{source_account}.txt"

    with open(source_account_file_name, "a") as account_file:
        account_file.write(f"\n{amount * -1}")

    # deposit (to dest)
    dest_account_file_name = f"{dest_account}.txt"

    with open(dest_account_file_name, "a") as account_file:
        account_file.write(f"\n{amount}")

    print(f"${amount} was transferred from #{source_account} to #{dest_account}")


def new_account():
    # account
    account_no = input_account_number()
    if len(account_no) == 0:
        return

    # amount
    amount = input_int("Amount> ")

    # deposit > 0
    if amount < 1:
        print("Amount must be greater than 0")
        return

    file_name = f"{account_no}.txt"

    with open(file_name, "a") as account_file:
        account_file.write(f"{amount}")

    print(f"Account #{account_no} is now opened with ${amount} balance.")

#######################################
# Main Application
#######################################


while True:
    # attemp to login
    (logged_in, username) = login()

    # prevent user trying to login more than 3 times
    if logged_in == False:
        print("You can't login more than 3 times")
        break

    # main logic
    print(f"Welcome {username}")

    while True:
        selected_menu = menu()

        # balance
        if selected_menu == 1:
            get_account_balance()

        # transactions
        elif selected_menu == 2:
            get_account_transactions()

        # deposit
        elif selected_menu == 3:
            deposit()

        # withdraw
        elif selected_menu == 4:
            withdraw()

        # transfer
        elif selected_menu == 5:
            transfer()

        # new account
        elif selected_menu == 6:
            new_account()

        # exit
        elif selected_menu == 0:
            print("Logged out!")
            break
        else:
            print("Invalid input")
