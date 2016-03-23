# -*- coding: utf-8 -*-
"""
Created on Sun Oct 04 15:15:58 2015

@author: jcocks
"""

import chess.pgn
import chess.uci
import time
import subprocess
import random

engine = chess.uci.popen_engine("/Projects/chess-ai/stockfish")
engine.uci()
engine.author

# Get best moves
board = chess.Board("1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - 0 1")
engine.position(board)
engine.go(movetime=2000,depth=0) # Gets tuple of bestmove and ponder move.


# Iterating over PGN file
pgn = open("C:\Projects\chess-ai\movestest.pgn")
first_game = chess.pgn.read_game(pgn)
pgn.close()

positions = []

node = first_game
while node.variations:
    next_node = node.variation(0)
    positions.append(node.board().fen())
    node = next_node
    
    
# Feeding input to and getting output from stockfish binary
def put(command):
    print('\nyou:\n\t'+command)
    engine.stdin.write(command+'\n')

def get():
    # using the 'isready' command (eng has to answer 'readyok')
    # to indicate current last line of stdout
    t = "";
    engine.stdin.write('isready\n')
    print('\nengine:')
    while True:
        text = engine.stdout.readline().strip()
        if text == 'readyok':
            break
        if text !='':
            print('\t'+text)
            t = t + "\n" + text
    return t

# Pass the above game to stockfish's eval function
stockfish_cmd = 'C:\\Projects\\chess-ai\\stockfish'
engine = subprocess.Popen( stockfish_cmd, universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
for posn in positions:
    put("position fen " + posn)
    put("eval")

s = get()
engine.kill()

# Get the position scores
sList = s.split("\n")
totals = []
for ln in sList:
    if ln.startswith("Total E"):
        
        totals.append(ln)











