import chess
import logging
import sqlite3
import chess.pgn

#init logging
logging.basicConfig(filename="init_db.log", level=logging.INFO, 
      format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

# Connect to the database
conn = sqlite3.connect('lichess_id_fen_mate_eval_2022-06.db')
cursor = conn.cursor()


# Create the table
cursor.execute('''CREATE TABLE games
                  (id INTEGER PRIMARY KEY,
                   fen TEXT,
                   mate BIT,
                   eval FLOAT);''')


# Open the PGN file and read the games
with open('src/utils/lichess_db_standard_rated_2022-06.pgn') as pgn_file:
    game = chess.pgn.read_game(pgn_file)
    n_game = 0
    n_move = 0 # keep track of moves stored
    # Loop through each game in the PGN file
    while game is not None:
      added_game = False
      board = game.board()
      for node in game.mainline():
        # Check that evaluation was saved for this game else skip
        evaluation = node.eval()
        if evaluation is None: break
        
        # increase game counter
        if not added_game:
          n_game += 1
          added_game = True

        board.push(node.move)
        fen = board.fen()

        score = node.eval().white()
        is_mate = score.is_mate() 
        evaluation = 0
        # if it is mate in n moves, evalaute is the number of moves
        if is_mate:
          evaluation = score.mate()
        else:
          evaluation = score.score()

        # Insert the data into the database
        cursor.execute("INSERT INTO games (id, fen, mate, eval) VALUES (?, ?, ?, ?)",
                      (n_move, fen, int(is_mate), evaluation))
        # log
        logging.info(f"logged {n_move}ith move. Currently in {n_game}th game")

        n_move += 1

      # Read the next game in the PGN file
      game = chess.pgn.read_game(pgn_file)

# Commit the changes and close the connection
conn.commit()
conn.close()
