import sqlite3
import chess.pgn

# Connect to the database
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

"""
# Create the table
cursor.execute('''CREATE TABLE games
                  (id INTEGER PRIMARY KEY,
                   fen TEXT,
                   eval FLOAT);''')
"""

# Open the PGN file and read the games
with open('src/utils/game.pgn') as pgn_file:
    game = chess.pgn.read_game(pgn_file)


    n_move = 0
    # Loop through each game in the PGN file
    while game is not None:
        board = game.board()

        # Loop through each move in the game
        for move in game.mainline_moves():
            board.push(move)
            fen = board.fen()

            
            #score = board.pop().eval()
            print(move)
            # Get the evaluation for the current board state
            # Replace this with your own evaluation function
            #eval = evaluate_board(board)

            # Insert the data into the database
            #cursor.execute("INSERT INTO games (id, fen, eval) VALUES (?, ?, ?)",
            #               (n_move, fen, 0))

            n_move += 1

        # Read the next game in the PGN file
        game = chess.pgn.read_game(pgn_file)

# Commit the changes and close the connection
conn.commit()
conn.close()
