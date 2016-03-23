# -*- coding: utf-8 -*-
"""
Created on Mon Oct 05 10:01:08 2015

@author: jcocks
"""

import chess.pgn
import chess.uci
import time
import subprocess
import random
import json
import numpy

# Iterating over PGN file
pgn = open("C:\\Projects\\chess-ai\\data\\CCRL-4040.[607599].pgn")
chessGame = 0
counter = 0
positions = []
while chessGame is not None:
    chessGame = chess.pgn.read_game(pgn)
    if chessGame is None:
        break
    node = chessGame
    while node.variations:
        next_node = node.variation(0)
        positions.append(node.board().fen())
        node = next_node
    counter += 1
    positions = numpy.unique(positions).tolist();
    print("Processing Game: " + str(counter) + ", Unique positions: " + str(len(positions)))

pgn.close()

positions = numpy.unique(numpy.array(positions)).tolist()
print "All games processed.  Unique positions:  " + str(len(positions))
# Feeding input to and getting output from stockfish binary
stockfish_cmd = 'C:\\Projects\\chess-ai\\stockfish'
engine = subprocess.Popen( stockfish_cmd, universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
def put(command):
    #print('\nyou:\n\t'+command)
    engine.stdin.write(command+'\n')

def get():
    # using the 'isready' command (eng has to answer 'readyok')
    # to indicate current last line of stdout
    t = "";
    engine.stdin.write('isready\n')
    #print('\nengine:')
    while True:
        text = engine.stdout.readline().strip()
        if text == 'readyok':
            break
        if text !='':
            #print('\t'+text)
            t = t + "\n" + text
    return t
evals = []
numPos = str(len(positions))
for ix, posn in enumerate(positions):
    put("position fen " + posn)
    put("eval")
    s = get()
    # Convert score strings to numbers
    sList = s.split("\n")
    scoreLine = sList[-1]
    st = scoreLine.index(":") + 1
    ed = scoreLine.index("(") - 1
    score = scoreLine[st:ed].strip()
    score = float(score)
    evals.append(score)
    print("Evaluating position:" + str(ix) + " of " + numPos)


engine.kill()

# Save to json array
j = []
for ix, p in enumerate(positions):
    d = {"FenString": p, "EvaluationScore": evals[ix]}
    j.append(d)



with open('C:\\Projects\\chess-ai\\Data\\testScores.json', 'w') as outfile:
    json.dump(json.dumps(j), outfile)





