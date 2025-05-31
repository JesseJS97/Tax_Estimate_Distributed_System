# Server 1 logic (Phase 1 & Phase 2)
# Developed by Jesse Scully
# Description: Using implementation style (i), Phase 1 server will utilise
# a two tier application using the Pyro5 library
# The following code has been influenced by:
# https://pyro5.readthedocs.io/en/latest/servercode.html
# https://pyro5.readthedocs.io/en/latest/intro.html
# https://github.com/irmen/Pyro5/blob/master/examples/nonameserver/server.py
# https://www.geeksforgeeks.org/use-of-flag-in-programming/

# Use Pyro5 library api
import Pyro5.api

'''
Server app provides services that process data received from client
Calculates users annual taxable income and tax withheld
Generates tax return estimate against the estimate criter
Returns estimate result to client
Server may send a request to the database server to fetch a users payroll tax data
or from the PITD if needed
'''

@Pyro5.api.expose
class PyroService():

# Display individual tax related data
# e.g. Sequence of biweekly taxable income and tax withheld
# <taxable_income, tax_withheld> pairs on screen in their input order

    def Tax_Data(self, ndi_list, has_TFN_flag, person_PHIC, person_TFN):
        tfn = None
                # This is basis for phase 2 if person does have a TFN
        if has_TFN_flag:
            # Need to implement processing logic by retrieving data from server2
            uri_tfn = input("What is the Pyro uri of server_2 if you have TFN? ")
            tfn_maker = Pyro5.api.Proxy(uri_tfn)
            tfn = int(input("Enter TFN: "))

            get_data = tfn_maker.get_taxpayerdata(tfn)

            # Gather data and create ndi_list from taxpayers db
            tfn = get_data[0][2]
            ndi_list = [(row[4], row[5]) for row in get_data]

        # This is the basis for Phase 1 if person does not have TFN
        else:
            for income, withheld in ndi_list:
                print(f"Income: {income}, Tax withheld: {withheld}")
        
        # Calculate annual taxable_income
        total_taxable_income = sum(income for income, _ in ndi_list)

        # Calculate tax return estimate according to tax return criteria
        total_tax_withheld = sum(withheld for _, withheld in ndi_list)

        # Parameters for 0-18200 income earners 
        if 0 <= total_taxable_income <= 18200:
            print(f"TFN: {tfn}")
            print(f"Annual Taxable Income: {total_taxable_income}")
            print(f"Total Tax Withheld: {total_tax_withheld}")

            # Calculate total net income
            net_income = total_taxable_income - total_tax_withheld
            print(f"Net income: {net_income}")

            # Calculate Medicare Levy
            medicare_levy = 0.02 * total_taxable_income
            
            # Calculate tax refund
            tax_refund = total_tax_withheld - 0
            print(f"Estimated tax refund amount: {tax_refund}")


        elif 18200 < total_taxable_income <= 45000:
            print(f"TFN: {tfn}")
            print(f"Annual Taxable Income: {total_taxable_income}")
            print(f"Total Tax Withheld: {total_tax_withheld}")

            # Calculate total net income
            net_income = total_taxable_income - total_tax_withheld
            print(f"Net income: {net_income}")

            # Calculate medicare levy
            medicare_levy = 0.02 * total_taxable_income

            # Calculate tax refund using 2023-2024 criteria
            tax_income_bracket = total_taxable_income - 18200
            bracket2_taxed = tax_income_bracket * 0.19
            total_tax = medicare_levy + bracket2_taxed

            # Determine if tax refund or amount owed depending on
            # Total tax withheld vs total tax owed
            if total_tax_withheld >= total_tax:
                tax_refund = total_tax_withheld - total_tax
                print(f"Estimated tax refund amount: {tax_refund}")           
            else:
                tax_owed = total_tax - total_tax_withheld
                print(f"Estimated amount owed: {tax_owed}")

        # Parameters for 45000-120000 income earners 
        elif 45000 < total_taxable_income <= 120000:
            print(f"TFN: {tfn}")
            print(f"Annual Taxable Income: {total_taxable_income}")
            print(f"Total Tax Withheld: {total_tax_withheld}")

            # Calculate total net income
            net_income = total_taxable_income - total_tax_withheld
            print(f"Net income: {net_income}")

            # Calculate medicare levy
            medicare_levy = 0.02 * total_taxable_income

            # Calculate tax refund using 2023-2024 criteria
            tax_income_bracket = total_taxable_income - 45000
            bracket3_taxed = tax_income_bracket * 0.325 + 5092
            total_tax = medicare_levy + bracket3_taxed

            # Calculate tax refund lower bracket with MLS not considered
            if 45000 < total_taxable_income <= 90000:
                if total_tax_withheld >= total_tax:
                    tax_refund = total_tax_withheld - total_tax
                    print(f"Estimated tax refund amount: {tax_refund}")           
                else:
                    tax_owed = total_tax - total_tax_withheld
                    print(f"Estimated amount owed: {tax_owed}")

            # Calculate tax refund with MLS considered
            elif 90001 <= total_taxable_income <= 105000:
                tti_mls = total_taxable_income * 0.01
                #Determine if taxpayer needs to pay MLS
                if person_PHIC == 'N':
                    mls_total_tax = tti_mls + total_tax
                else:
                    mls_total_tax = total_tax
                # Determine if tax refund or amount owed depending on
                # Total tax withheld vs total tax owed
                if total_tax_withheld >= mls_total_tax:
                    tax_refund = total_tax_withheld - mls_total_tax
                    print(f"Estimated tax refund amount: {tax_refund}")           
                else:
                    tax_owed = mls_total_tax - total_tax_withheld
                    print(f"Estimated amount owed: {tax_owed}")

            # Calculate tax refund higher bracket with MLS considered
            else:
                tti_mls2 = total_taxable_income * 0.0125
                #Determine if taxpayer needs to pay MLS
                if person_PHIC == 'N':
                    mls_total_tax = tti_mls + total_tax
                else:
                    mls_total_tax = total_tax

                # Determine if tax refund or amount owed depending on
                # Total tax withheld vs total tax owed
                if total_tax_withheld >= mls_total_tax:
                    tax_refund = total_tax_withheld - mls_total_tax
                    print(f"Estimated tax refund amount: {tax_refund}")           
                else:
                    tax_owed = mls_total_tax - total_tax_withheld
                    print(f"Estimated amount owed: {tax_owed}")

        # Parameters for 120000-180000 income earners 
        elif 120000 < total_taxable_income <= 180000:
            print(f"TFN: {tfn}")
            print(f"Annual Taxable Income: {total_taxable_income}")
            print(f"Total Tax Withheld: {total_tax_withheld}")
            
            # Calculate total net income
            net_income = total_taxable_income - total_tax_withheld
            print(f"Net income: {net_income}")

            # Calculate medicare levy
            medicare_levy = 0.02 * total_taxable_income

            # Calculate tax refund using 2023-2024 criteria
            tax_income_bracket = total_taxable_income - 120000
            bracket4_taxed = tax_income_bracket * 0.37 + 29467
            total_tax = medicare_levy + bracket4_taxed

            # Calculate tax refund with MLS considered
            if 105001 <= total_taxable_income <= 140000:
                tti_mls = total_taxable_income * 0.0125
                #Determine if taxpayer needs to pay MLS
                if person_PHIC == 'N':
                    mls_total_tax = tti_mls + total_tax
                else:
                    mls_total_tax = total_tax

                # Determine if tax refund or amount owed depending on
                # Total tax withheld vs total tax owed
                if total_tax_withheld >= mls_total_tax:
                    tax_refund = total_tax_withheld - mls_total_tax
                    print(f"Estimated tax refund amount: {tax_refund}")           
                else:
                    tax_owed = mls_total_tax - total_tax_withheld
                    print(f"Estimated amount owed: {tax_owed}")
            
            # Calculate tax refund higher bracket with MLS considered
            else:
                tti_mls = total_taxable_income * 0.015
                #Determine if taxpayer needs to pay MLS
                if person_PHIC == 'N':
                    mls_total_tax = tti_mls + total_tax
                else:
                    mls_total_tax = total_tax

                # Determine if tax refund or amount owed depending on
                # Total tax withheld vs total tax owed
                if total_tax_withheld >= mls_total_tax:
                    tax_refund = total_tax_withheld - mls_total_tax
                    print(f"Estimated tax refund amount: {tax_refund}")           
                else:
                    tax_owed = mls_total_tax - total_tax_withheld
                    print(f"Estimated amount owed: {tax_owed}")

        # Parameters for 180000 or more income earners 
        elif total_taxable_income > 180000:
            print(f"TFN: {tfn}")
            print(f"Annual Taxable Income: {total_taxable_income}")
            print(f"Total Tax Withheld: {total_tax_withheld}")
            
            # Calculate total net income
            net_income = total_taxable_income - total_tax_withheld
            print(f"Net income: {net_income}")

            # Calculate medicare levy
            medicare_levy = 0.02 * total_taxable_income

            # Calculate tax refund using 2023-2024 criteria
            tax_income_bracket = total_taxable_income - 180000
            bracket5_taxed = tax_income_bracket * 0.45 + 51667
            total_tax = medicare_levy + bracket5_taxed

            # Calculate tax refund with MLS considered
            tti_mls2 = total_taxable_income * 0.0125
            #Determine if taxpayer needs to pay MLS
            if person_PHIC == 'N':
                mls_total_tax = tti_mls + total_tax
            else:
                mls_total_tax = total_tax
                
            # Determine if tax refund or amount owed depending on
            # Total tax withheld vs total tax owed
            if total_tax_withheld >= mls_total_tax:
                tax_refund = total_tax_withheld - mls_total_tax
                print(f"Estimated tax refund amount: {tax_refund}")           
            else:
                tax_owed = mls_total_tax - total_tax_withheld
                print(f"Estimated amount owed: {tax_owed}")

        else:
            print("Invalid taxable amount")
            print("TFN enetered does not exist")
    
# Setup server 1 and keep it running
daemon = Pyro5.api.Daemon()
uri = daemon.register(PyroService)

print("Ready. Object uri =", uri)
daemon.requestLoop()