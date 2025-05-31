# Server_2 data transmission logic
# Data transmission server between Server 1 and Taxpayers database
# Created by Jesse Scully

import Pyro5.api
import sqlite3

# Adapted from: https://www.freecodecamp.org/news/work-with-sqlite-in-python-handbook/ (How to Fetch Multiple Records)
@Pyro5.api.expose
class taxpayers(object):
    def get_taxpayerdata(self, tfn):
        with sqlite3.connect('Taxpayers.db') as connection:
            cursor = connection.cursor()
            # Retrieve data from database
            select_taxpayers = "SELECT * FROM TAXTFN WHERE TFN = ?;"

            # Execute selecting command
            cursor.execute(select_taxpayers, (tfn,))

            # Fetch 4 records
            four_entries = cursor.fetchmany(4)

            # Display results
            print("2 entries")
            for entry in four_entries:
                print(entry)
            
            return four_entries


daemon = Pyro5.api.Daemon()             # make a Pyro daemon
uri = daemon.register(taxpayers)    # register the greeting maker as a Pyro object

print("Ready. Object uri =", uri)       # print the uri so we can use it in the client later
daemon.requestLoop()                    # start the event loop of the server to wait for calls