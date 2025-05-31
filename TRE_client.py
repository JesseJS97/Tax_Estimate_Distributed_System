# Client-Side Application
# Developed by Jesse Scully
# Collects a user's data, performs preliminary pre-processing of the data items
# Then sends the data to the remote application/s at server-side
# Influenced by:
# https://pyro5.readthedocs.io/en/latest/intro.html
# https://www.geeksforgeeks.org/use-of-flag-in-programming/

import Pyro5.api
print("Please use URI for Server_1 initially")
print("Please input URI for Server_2 further in program")

uri = input("Enter URI of Server: ")
tax_server1 = Pyro5.api.Proxy(uri)

# Ask user for tax return estimate input
tax_return_input = int(input("Please enter tax return estimate: "))

# Establish a hard-coded person ID and password
person_ID = 154477
password = "hellothere123"

# Ask user for login details
person_ID_input = int(input("Please enter your ID number: "))
person_PW_input = str(input("PLease enter your password: "))

if person_ID == person_ID_input and password == person_PW_input:
    print("Details match!")
else:
    print("Details dont match, sorry!")
    exit()

# Ask user for 8-digit Tax File Number
# Initialise flag variable to signal to server1 there is a TFN present
has_TFN_flag_input = str(input("Do you have an 8-digit TFN number? Y/N"))
# Initialise flag as boolean to be used in Server 1
if has_TFN_flag_input == 'Y':
    has_TFN_flag = True
else:
    has_TFN_flag = False

# If user has TFN, will ask user to enter to enter TFN
# Along with other information (e.g. first and last name, email address, age)
# As well as Person ID
if has_TFN_flag:
    person_TFN_input = int(input("Please enter 8-digit TFN number: "))
    person_FN = str(input("Please enter First name: "))
    person_LN = str(input("Please enter Last Name: "))
    person_Email = str(input("Please enter email address: "))

    person_ID_input = int(input("Please enter your ID number again: "))

    # Ask for PHIC input to decide if MLS needs to be paid
    person_PHIC = str(input("Do you have Private Health Insurance Cover? (Y/N): "))
    ndi_list = []

    # Call function from Server_1 to calculate tax if TFN found (phase 1)
    tax_server1.Tax_Data([], has_TFN_flag, person_PHIC, person_ID_input)
    
    print("Sending data to server...")

elif not has_TFN_flag:
    person_FN = str(input("Please enter First name: "))
    person_LN = str(input("Please enter Last Name: "))
    person_Email = str(input("Please enter email address: "))

    person_ID_input = int(input("Please enter your ID number again: "))

    # Ask for PHIC input to decide if MLS needs to be paid
    person_PHIC = str(input("Do you have Private Health Insurance Cover? (Y/N): "))
    ndi_list = []
    # Request a sequence of biweekly taxable income and the corresponding tax withheld
    num_data_items = int(input("How many pay period (data items) would you like to enter? (1-26)"))
    
    if 1 <= num_data_items <= 26:
        # Iterate over the number of requested data items
        for i in range(num_data_items):
            taxable_income = int(input("Taxable income: "))
            tax_withheld = int(input("Tax withheld: "))
            # Append data to list of items with appropriate tax income and withheld tax
            ndi_list.append((taxable_income, tax_withheld))
    
    print("Sending data to server...")

    # Call function from Server_1 to calculate tax if no TFN found
    tax_server1.Tax_Data(ndi_list, has_TFN_flag, person_PHIC, 0)


else:
    print("Invalid input! Exiting program...")
    exit()


