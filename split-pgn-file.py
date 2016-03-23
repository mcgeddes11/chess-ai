__author__ = 'jcocks'

import numpy
import chess.pgn

# this script splits the large file into 1000 game chunks
inFile = open("C:\\Projects\\chess-ai\\data\\CCRL-4040.[607599].pgn")
chessGame = 0
gameCounter = 0
fileCounter = 0
positions = []
while chessGame is not None:
    chessGame = chess.pgn.read_game(inFile)
    if gameCounter == 0:
        outFile = open("C:\\Projects\\chess-ai\\data\\games_" + str(fileCounter) + ".pgn" , "w")
        exporter = chess.pgn.FileExporter(outFile)
    if chessGame is None:
        break
    chessGame.export(exporter)
    gameCounter += 1
    if gameCounter > 1000:
        fileCounter += 1
        gameCounter = 0
        outFile.close()
    print("Processing Game: " + str(gameCounter) + " of file: " + str(fileCounter))

inFile.close()