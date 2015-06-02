-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- players' table

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE players(
	id serial primary key,
	name text
);

CREATE TABLE matches(
	id serial primary key,
	winner integer REFERENCES players(id),
	loser integer REFERENCES players(id)
);

-- The number of wins for each player
CREATE VIEW num_wins AS 
  SELECT players.id AS winner, COUNT(winner) AS wins 
  FROM players LEFT JOIN matches 
  ON players.id = matches.winner
  GROUP BY players.id 
  ORDER BY wins DESC;

-- The number of loses for each player
CREATE VIEW num_loses AS 
  SELECT players.id AS loser, COUNT(loser) AS loses 
  FROM players LEFT JOIN matches 
  ON players.id = matches.loser
  GROUP BY players.id 
  ORDER BY loses;

-- The number of matches each player has played
CREATE VIEW num_matches AS
  SELECT winner, wins, (wins + loses) AS total
  FROM num_wins, num_loses
  WHERE winner = loser
  ORDER BY winner;

-- Player standings sorted by wins
CREATE VIEW standings AS
  SELECT players.id, players.name, wins, total
  FROM players LEFT JOIN num_matches
  ON num_matches.winner = players.id
  ORDER BY wins DESC




