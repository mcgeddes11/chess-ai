import numpy, os, pandas, uuid, re
from subprocess import check_output

def createOutputDirectoryFromFilename(fileName):
    dirName = os.path.dirname(fileName)
    if not os.path.exists(dirName):
        os.makedirs(dirName)

def ping(host):
    import os, platform
    if platform.system().lower() == "windows":
        ping_str = "-n 1"
    else:
        ping_str = "-c 1"
    return os.system("ping " + ping_str + " " + host) == 0

def ismember(a, b):
    bind = {}
    for elt in b:
        if elt not in bind:
            bind[elt] = True
    return numpy.array([bind.get(itm, False) for itm in a])

def get_file_list(config):
    n_files = int(numpy.ceil(config["n_games"]/config["data_file_chunks"]))
    file_list = []
    for n in range(0,n_files):
        file_list.append(os.path.join(config["data_repository"],"split_data",str(n).zfill(4) + ".pgn"))
    return file_list

def processFeatures(board):
    d = {"SideToMove": 0,
         "CastlingRights": numpy.zeros((4, 1)),
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
         "BlackPawnLocs": {"Rows": numpy.zeros((8, 1)), "Cols": numpy.zeros((8, 1))},
         "WhitePawnLocs": {"Rows": numpy.zeros((8, 1)), "Cols": numpy.zeros((8, 1))},
         "BlackRookLocs": {"Rows": numpy.zeros((2, 1)), "Cols": numpy.zeros((2, 1))},
         "WhiteRookLocs": {"Rows": numpy.zeros((2, 1)), "Cols": numpy.zeros((2, 1))},
         "BlackKnightLocs": {"Rows": numpy.zeros((2, 1)), "Cols": numpy.zeros((2, 1))},
         "WhiteKnightLocs": {"Rows": numpy.zeros((2, 1)), "Cols": numpy.zeros((2, 1))},
         "BlackBishopLocs": {"Rows": numpy.zeros((2, 1)), "Cols": numpy.zeros((2, 1))},
         "WhiteBishopLocs": {"Rows": numpy.zeros((2, 1)), "Cols": numpy.zeros((2, 1))},
         "BlackQueenLocs": {"Rows": 0, "Cols": 0},
         "WhiteQueenLocs": {"Rows": 0, "Cols": 0},
         "BlackKingLocs": {"Rows": 0, "Cols": 0},
         "WhiteKingLocs": {"Rows": 0, "Cols": 0}}
    # Set side to move


    if (board.turn):
        d["SideToMove"] = 1
        # Assign castling rights in this order:
        # White kingside
        # White queenside
        # Black kingside
        # Black queenside
    d["CastlingRights"] = numpy.array(
        [int(board.has_kingside_castling_rights(1)), int(board.has_kingside_castling_rights(0)),
         int(board.has_queenside_castling_rights(1)), int(board.has_queenside_castling_rights(0))])

    for ix in range(0, 64):
        colRef = int(ix % 8) + 1
        rowRef = int(ix / 8) + 1
        piece = board.piece_at(ix)
        # Statement order:
        # - Piece position
        # - Piece count
        # - Attacker
        # - Defender

        if piece is not None:
            if (piece.symbol() == "p"):
                # print "Black pawn found, location: " + str(rowRef) + " , " + str(colRef)
                d["BlackPawnLocs"]["Rows"][d["BlackPawns"]] = rowRef
                d["BlackPawnLocs"]["Cols"][d["BlackPawns"]] = colRef
                d["BlackPawns"] += 1
            elif (piece.symbol() == "P"):
                # print "White pawn found, location: " + str(rowRef) + " , " + str(colRef)
                d["WhitePawnLocs"]["Rows"][d["WhitePawns"]] = rowRef
                d["WhitePawnLocs"]["Cols"][d["WhitePawns"]] = colRef
                d["WhitePawns"] += 1
            elif (piece.symbol() == "r"):
                # print "Black rook found, location: " + str(rowRef) + " , " + str(colRef)
                if d["BlackRooks"] < len(d["BlackRookLocs"]["Rows"]):
                    d["BlackRookLocs"]["Rows"][d["BlackRooks"]] = rowRef
                    d["BlackRookLocs"]["Cols"][d["BlackRooks"]] = colRef
                d["BlackRooks"] += 1
            elif (piece.symbol() == "R"):
                # print "White rook found, location: " + str(rowRef) + " , " + str(colRef)
                if d["WhiteRooks"] < len(d["WhiteRookLocs"]["Rows"]):
                    d["WhiteRookLocs"]["Rows"][d["WhiteRooks"]] = rowRef
                    d["WhiteRookLocs"]["Cols"][d["WhiteRooks"]] = colRef
                d["WhiteRooks"] += 1
            elif (piece.symbol() == "n"):
                # print "Black knight found, location: " + str(rowRef) + " , " + str(colRef)
                if d["BlackKnights"] < len(d["BlackKnightLocs"]["Rows"]):
                    d["BlackKnightLocs"]["Rows"][d["BlackKnights"]] = rowRef
                    d["BlackKnightLocs"]["Cols"][d["BlackKnights"]] = colRef
                d["BlackKnights"] += 1
            elif (piece.symbol() == "N"):
                # print "White knight found, location: " + str(rowRef) + " , " + str(colRef)
                if d["WhiteKnights"] < len(d["WhiteKnightLocs"]["Rows"]):
                    d["WhiteKnightLocs"]["Rows"][d["WhiteKnights"]] = rowRef
                    d["WhiteKnightLocs"]["Cols"][d["WhiteKnights"]] = colRef
                d["WhiteKnights"] += 1
            elif (piece.symbol() == "b"):
                # print "Black bishop found, location: " + str(rowRef) + " , " + str(colRef)
                if d["BlackBishops"] < len(d["BlackBishopLocs"]["Rows"]):
                    d["BlackBishopLocs"]["Rows"][d["BlackBishops"]] = rowRef
                    d["BlackBishopLocs"]["Cols"][d["BlackBishops"]] = colRef
                d["BlackBishops"] += 1
            elif (piece.symbol() == "B"):
                # print "White bishop found, location: " + str(rowRef) + " , " + str(colRef)
                if d["WhiteBishops"] < len(d["WhiteBishopLocs"]["Rows"]):
                    d["WhiteBishopLocs"]["Rows"][d["WhiteBishops"]] = rowRef
                    d["WhiteBishopLocs"]["Cols"][d["WhiteBishops"]] = colRef
                d["WhiteBishops"] += 1
            elif (piece.symbol() == "q"):
                # print "Black queen found, location: " + str(rowRef) + " , " + str(colRef)
                if d["BlackQueens"] < 1:
                    d["BlackQueenLocs"]["Rows"] = rowRef
                    d["BlackQueenLocs"]["Cols"] = colRef
                d["BlackQueens"] += 1
            elif (piece.symbol() == "Q"):
                # print "White queen found, location: " + str(rowRef) + " , " + str(colRef)
                if d["WhiteQueens"] < 1:
                    d["WhiteQueenLocs"]["Rows"] = rowRef
                    d["WhiteQueenLocs"]["Cols"] = colRef
                d["WhiteQueens"] += 1
            elif (piece.symbol() == "k"):
                # print "Black king found, location: " + str(rowRef) + " , " + str(colRef)
                d["BlackKingLocs"]["Rows"] = rowRef
                d["BlackKingLocs"]["Cols"] = colRef
                d["BlackKings"] += 1
            elif (piece.symbol() == "K"):
                # print "White king found, location: " + str(rowRef) + " , " + str(colRef)
                d["WhiteKingLocs"]["Rows"] = rowRef
                d["WhiteKingLocs"]["Cols"] = colRef
                d["WhiteKings"] += 1

    cols = []
    data = []
    for k in d.keys():
        el = d[k]
        if "Locs" in k and type(el["Rows"]) != int:
            for ix, r in enumerate(el["Rows"]):
                cols.append(k + "_" + str(ix) + "_" + "Row")
                data.append(r[0])
            for ix, r in enumerate(el["Cols"]):
                cols.append(k + "_" + str(ix) + "_" + "Col")
                data.append(r[0])
        elif "Locs" in k and type(el["Rows"]) == int:
            cols.append(k + "_1_" + "Row")
            data.append(el["Rows"])
            cols.append(k + "_1_" + "Col")
            data.append(el["Cols"])
        elif "Castling" in k:
            cols.append("White_kingside_castling_right")
            data.append(el[0])
            cols.append("White_queenside_castling_right")
            data.append(el[1])
            cols.append("Black_kingside_castling_right")
            data.append(el[2])
            cols.append("Black_queenside_castling_right")
            data.append(el[3])
        else:
            cols.append(k)
            data.append(el)


    return cols, data;