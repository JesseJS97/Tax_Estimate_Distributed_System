# Create data to be passed into the database
# Created by Jesse Scully
# Influenced by:
# https://www.geeksforgeeks.org/python-sqlite-create-table/
# https://www.freecodecamp.org/news/work-with-sqlite-in-python-handbook/#heading-how-to-create-database-tables
# https://www.tutorialspoint.com/sqlite/sqlite_python.htm

import sqlite3 
import os

# Delete old database if already existing
if os.path.exists("Taxpayers.db"):
    os.remove("Taxpayers.db")
    print("Old database has been removed.")

# Connecting to database
connect_db = sqlite3.connect('Taxpayers.db')
cursor_obj = connect_db.cursor()

# Generate data for first taxpayer with TFN
connect_db.execute("""CREATE TABLE IF NOT EXISTS TAXTFN (
                employee_ID INTEGER,
                name TEXT,
                TFN INTEGER,
                pay_Period INTEGER,
                gross_Salary INT,
                tax_Withheld INT
            ); """)

print("Table made successfully");

# Establish multiple pay instances for both taxpayers
# Adapted from: https://www.youtube.com/watch?v=1VckrGBY2fE
multiple_entries = [
    (154477,'Jason',14499776,1,60000,5000),
    (154477,'Jason',14499776,2,67000,9100),
    (154477,'Jeff',88888888,1,95000,5000),
    (154477,'Jeff',88888888,2,99999,11000),
]

sql = ''' INSERT INTO TAXTFN 
        (employee_ID,name,TFN,pay_Period,gross_Salary,tax_Withheld)
        VALUES (?, ?, ?, ?, ?, ?);''' 

cursor_obj.executemany(sql, multiple_entries)

connect_db.commit()
print ("Entries made successfully")
connect_db.close()