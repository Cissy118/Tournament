#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    db_cursor = db.cursor()
    query = "DELETE FROM matches"
    db_cursor.execute(query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    db_cursor = db.cursor()
    query = "DELETE FROM players"
    db_cursor.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    db_cursor = db.cursor()
    query = "SELECT COUNT (*) as number FROM players"
    db_cursor.execute(query)
    rows = db_cursor.fetchone()
    db.close()
    return rows[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    db_cursor = db.cursor()
    query = "INSERT INTO players (name) VALUES (%s)"
    db_cursor.execute(query, (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or 
    a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    db_cursor = db.cursor()
    query = "SELECT * FROM standings"
    db_cursor.execute(query)
    result = db_cursor.fetchall()
    db.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    db_cursor = db.cursor()
    query = "INSERT INTO matches (winner, loser) VALUES (%s, %s)"
    db_cursor.execute(query, (winner, loser))
    db.commit()
    db.close()
 

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings. There won't be rematches between players.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standingsList = playerStandings()
    result = []
    j = 1
    while len(standingsList) >= 2 and j < len(standingsList):
        id1 = standingsList[0][0]
        id2 = standingsList[j][0]
        name1 = standingsList[0][1]
        name2 = standingsList[j][1]
        if rematched(id1, id2):
            j = j + 1
            print str(id1) + ' ' + str(id2) + ' have been rematched'
        else:
            result.append((id1, name1, id2, name2))
            standingsList.pop(j)
            standingsList.pop(0)
            j = 1
    return result


def rematched(id1, id2):
    """return TRUE if two players have already played with each other
  
    Args:
      id1: the id number of one player
      id2: the id number of another player going to play with the player of id1
    """
    db = connect()
    db_cursor = db.cursor()
    query = "SELECT * FROM matches WHERE (winner = %s AND loser = %s) OR (winner = %s AND loser = %s)"
    db_cursor.execute(query, (id1, id2, id2, id1))
    matchesList = db_cursor.fetchall()
    db.close()
    return len(matchesList) != 0
