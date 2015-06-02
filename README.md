Tournament
---------------------
The project includes a database schema to store the game matches between players and APIs that could be used to rank the players and pair them up in matches in a tournament.

Files explanation
-----------
tournament.sql
---- Database schema and SQL queris to create database and tables for players and matches

tournament.py
---- Python modules used to achieve the functionalities such as player registration, reporting matches, ranking the players, pairing players for next matches.

tournament_test.py
---- Unit tests for the functions in tournament.py

Instruction
-----------
1. Run the Vagrant VM in the terminal.
2. To create the database and connect to it, running psql and using the command:
  \i tournament.sql
3. To test the functions in tournament.py running unit tests file tournament_test.py:
  python tournament_test.py


