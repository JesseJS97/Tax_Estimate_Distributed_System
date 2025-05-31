# Tax_Estimate_Distributed_System
Personal Income Tax Estimate and Owing Distributed System in Python using SQLite3 and Pyro5 libraries

Step-by-step procedure for setting up and running the system
User authentication details if this info is not provided in the user manual section
of the written report

Generate_data.py must be run before any other files in order to populate database
Previous database will be automatically deleted if program is rerun

# Instructions to run distributed system using three-tiered approach
1. Pyro5 must be installed on local machine for RPC communication
2. Python 3.0 must be installed on local machine
3. Run Server_1.py and Object uri must be noted and copied if they do not have TFN
4. Run Server_2.py and Object uri must be noted and copied if they have TFN
4. Open second terminal and run TRE_client.py
5. Follow prompts
6. Outputed results shall be displayed server side
