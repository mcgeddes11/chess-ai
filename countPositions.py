__author__ = 'jcocks'


import chess.pgn
import chess.uci
import time
import subprocess
import random
import json
import numpy

# Iterating over PGN file
pgn = open("C:\Projects\chess-ai\Data\CCRL-4040.[607599].pgn")
chessGame = 0
counter = 0
posCounter = 0
positions = []
while chessGame is not None:
    chessGame = chess.pgn.read_game(pgn)
    if chessGame is None:
        break
    node = chessGame
    while node.variations:
        next_node = node.variation(0)
        node = next_node
        positions.append(node.board().fen())
        posCounter += 1
    counter += 1
    print("Processing Game: " + str(counter))

pgn.close()

positions = numpy.array(positions);
positions = numpy.unique(positions);

print "Total Positions: " + str(posCounter)
print "Total unique positions: " + str(numpy.shape(positions)[0])