# -*- coding: utf-8 -*-
"""
Created on Mon Oct 05 10:50:04 2015

@author: jcocks
"""

import json
import chess
import numpy
import sys


def processFeatures(board):
    d = {"SideToMove": 0,
         "CastlingRights": numpy.zeros((4,1)),
         "WhitePawns": 0,
         "WhiteRooks": 0,
         "WhiteKnights": 0,
         "WhiteBishops": 0,
         "WhiteQueens": 0,
         "WhiteKings": 0,
         "BlackPawns": 0,
         "BlackRooks": 0,
         "BlackKnights": 0,
         "BlackBishops": 0,
         "BlackQueens": 0,
         "BlackKings": 0,
         "BlackPawnLocs":numpy.zeros((16,1)),
         "WhitePawnLocs":numpy.zeros((16,1)),
         "BlackRookLocs":numpy.zeros((4,1)),
         "WhiteRookLocs":numpy.zeros((4,1)),
         "BlackKnightLocs":numpy.zeros((4,1)),
         "WhiteKnightLocs":numpy.zeros((4,1)),
         "BlackBishopLocs":numpy.zeros((4,1)),
         "WhiteBishopLocs":numpy.zeros((4,1)),
         "BlackQueenLocs":numpy.zeros((2,1)),
         "WhiteQueenLocs":numpy.zeros((2,1)),
         "BlackKingLocs":numpy.zeros((2,1)),
         "WhiteKingLocs":numpy.zeros((2,1))}
    # Set side to move
    if (board.turn):
        d["SideToMove"] = 1
    # Assign castling rights in this order:
    # White kingside
    # White queenside
    # Black kingside
    # Black queenside
    d["CastlingRights"] = numpy.array([int(board.has_kingside_castling_rights(1)), int(board.has_kingside_castling_rights(0)), int(board.has_queenside_castling_rights(1)), int(board.has_queenside_castling_rights(0))])

    for ix in range(0,64):
        colRef = int(ix % 8) + 1;
        rowRef = int(ix / 8) + 1;
        piece = board.piece_at(ix)
        # Statement order:
        # - Piece position
        # - Piece count
        # - Attacker
        # - Defender

        if piece is not None:
            if (piece.symbol() == "p"):
                #print "Black pawn found, location: " + str(rowRef) + " , " + str(colRef)
                d["BlackPawnLocs"][2*d["BlackPawns"]:2*d["BlackPawns"]+2] = numpy.array([[rowRef/8],[colRef/8]])
                d["BlackPawns"] += 1
            elif (piece.symbol() == "P"):
                #print "White pawn found, location: " + str(rowRef) + " , " + str(colRef)
                d["WhitePawnLocs"][2*d["WhitePawns"]:2*d["WhitePawns"]+2] = numpy.array([[rowRef/8],[colRef/8]])
                d["WhitePawns"] += 1
            elif (piece.symbol() == "r"):
                #print "Black rook found, location: " + str(rowRef) + " , " + str(colRef)
                if 2*d["BlackRooks"] < len(d["BlackRookLocs"]):
                    d["BlackRookLocs"][2*d["BlackRooks"]:2*d["BlackRooks"]+2] = numpy.array([[rowRef/8],[colRef/8]])
                d["BlackRooks"] += 1
            elif (piece.symbol() == "R"):
                #print "White rook found, location: " + str(rowRef) + " , " + str(colRef)
                if 2*d["WhiteRooks"] < len(d["WhiteRookLocs"]):
                    d["WhiteRookLocs"][2*d["WhiteRooks"]:2*d["WhiteRooks"]+2] = numpy.array([[rowRef/8],[colRef/8]])
                d["WhiteRooks"] += 1                 
            elif (piece.symbol() == "n"):
                #print "Black knight found, location: " + str(rowRef) + " , " + str(colRef)
                if 2*d["BlackKnights"] < len(d["BlackKnightLocs"]):
                    d["BlackKnightLocs"][2*d["BlackKnights"]:2*d["BlackKnights"]+2] = numpy.array([[rowRef/8],[colRef/8]])
                d["BlackKnights"] += 1
            elif (piece.symbol() == "N"):
                #print "White knight found, location: " + str(rowRef) + " , " + str(colRef)
                if 2*d["WhiteKnights"] < len(d["WhiteKnightLocs"]):
                    d["WhiteKnightLocs"][2*d["WhiteKnights"]:2*d["WhiteKnights"]+2] = numpy.array([[rowRef/8],[colRef/8]])
                d["WhiteKnights"] += 1
            elif (piece.symbol() == "b"):
                #print "Black bishop found, location: " + str(rowRef) + " , " + str(colRef)
                if 2*d["BlackBishops"] < len(d["BlackBishopLocs"]):
                    d["BlackBishopLocs"][2*d["BlackBishops"]:2*d["BlackBishops"]+2] = numpy.array([[rowRef/8],[colRef/8]])
                d["BlackBishops"] += 1
            elif (piece.symbol() == "B"):
                #print "White bishop found, location: " + str(rowRef) + " , " + str(colRef)
                if 2*d["WhiteBishops"] < len(d["WhiteBishopLocs"]):
                    d["WhiteBishopLocs"][2*d["WhiteBishops"]:2*d["WhiteBishops"]+2] = numpy.array([[rowRef/8],[colRef/8]])
                d["WhiteBishops"] += 1
            elif (piece.symbol() == "q"):
                #print "Black queen found, location: " + str(rowRef) + " , " + str(colRef)
                if 2*d["BlackQueens"] < len(d["BlackQueenLocs"]):
                    d["BlackQueenLocs"][2*d["BlackQueens"]:2*d["BlackQueens"]+2] = numpy.array([[rowRef/8],[colRef/8]])
                d["BlackQueens"] += 1  
            elif (piece.symbol() == "Q"):
                #print "White queen found, location: " + str(rowRef) + " , " + str(colRef)
                if 2*d["WhiteQueens"] < len(d["WhiteQueenLocs"]):
                    d["WhiteQueenLocs"][2*d["WhiteQueens"]:2*d["WhiteQueens"]+2] = numpy.array([[rowRef/8],[colRef/8]])
                d["WhiteQueens"] += 1  
            elif (piece.symbol() == "k"):
                #print "Black king found, location: " + str(rowRef) + " , " + str(colRef)
                d["BlackKingLocs"][2*d["BlackKings"]:2*d["BlackKings"]+2] = numpy.array([[rowRef/8],[colRef/8]])
                d["BlackKings"] += 1  
            elif (piece.symbol() == "K"):
                #print "White king found, location: " + str(rowRef) + " , " + str(colRef)
                d["WhiteKingLocs"][2*d["WhiteKings"]:2*d["WhiteKings"]+2] = numpy.array([[rowRef/8],[colRef/8]])
                d["WhiteKings"] += 1                 
                  
    return d;

with open('C:\\Projects\\chess-ai\\Data\\testScores.json') as inFile:
    s = json.load(inFile)
data = json.loads(s)

# Generate features
y = []
features = []
data = data[0:100]
for ix, el in enumerate(data):
    board = chess.Board(el["FenString"])
    d = processFeatures(board)
    features.append(d)
    y.append(el["EvaluationScore"])
    
key = features[0].keys()
X = []
for obs in features:
    thisObs = []
    for k in key:
        if (type(obs[k]) is not int):
            thisObs.append(obs[k].flatten().tolist())
        else:
            thisObs.append([obs[k]])
    thisObs = [item for sublist in thisObs for item in sublist]
    X.append(thisObs)

print "Done!"
y = numpy.reshape(numpy.array(y),(numpy.shape(y)[0],1))
X = numpy.array(X)

# Test model
from sklearn import svm
from sklearn import cross_validation
from sklearn import linear_model
from sklearn.tree import DecisionTreeRegressor
y = y.flatten()
#clf = svm.SVR()
#clf = linear_model.LinearRegression()
clf = DecisionTreeRegressor()
#clf.fit(X, y)
scores = cross_validation.cross_val_score(clf, X, y, cv=10)



print "Done again"
print scores