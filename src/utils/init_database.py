import sqlite3
import chess
import chess.pgn

# Connect to the database
conn = sqlite3.connect('test.db')
cursor = conn.cursor()


# Create the table
cursor.execute('''CREATE TABLE games
                  (id INTEGER PRIMARY KEY,
                   fen TEXT,
                   mate BIT,
                   eval FLOAT);''')


# Open the PGN file and read the games
with open('src/utils/game.pgn') as pgn_file:
    game = chess.pgn.read_game(pgn_file)

    n_move = 0
    # Loop through each game in the PGN file
    while game is not None:
      board = game.board()

      for node in game.mainline():
            
        evaluation = node.eval()
        if evaluation is None: break

        board.push(node.move)
        fen = board.fen()

        int_score = node.eval().white()
        is_mate = int_score.is_mate() 
        evaluation = 0
        # if it is mate in n moves, evalaute is the number of moves
        if is_mate:
          evaluation = int_score.mate()
        else:
          evaluation = int_score.score()

        # Insert the data into the database
        cursor.execute("INSERT INTO games (id, fen, mate, eval) VALUES (?, ?, ?, ?)",
                      (n_move, fen, int(is_mate), evaluation))

        n_move += 1

      # Read the next game in the PGN file
      game = chess.pgn.read_game(pgn_file)

# Commit the changes and close the connection
conn.commit()
conn.close()
