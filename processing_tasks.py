import luigi, pandas, urllib, os, subprocess, numpy
import chess.pgn
import chess.uci
from project_utils import *

# Get the games file
class DownloadRawData(luigi.Task):
    config = luigi.Parameter()
    file_name = luigi.Parameter()

    def output(self):
        local_file = self.file_name.split("/")[-1].replace(".7z","").replace("%5b","[").replace("%5d","]")
        return luigi.LocalTarget(os.path.join(self.config["data_repository"],"raw_data",local_file))

    def run(self):
        archive_name = self.output().path + ".7z"
        createOutputDirectoryFromFilename(self.output().path)
        urllib.urlretrieve(self.file_name, archive_name)
        cmd = "'" + self.config["7z_path"] + "' x '" + archive_name + "' -o'" + os.path.join(self.config["data_repository"],"raw_data") + "'"
        print cmd
        subprocess.call(cmd,shell=True)
        os.remove(archive_name)


class ExtractUniquePositions(luigi.Task):
    config = luigi.Parameter()
    file_name = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(self.input().path.replace("raw_data","position_data").replace(".pgn",".csv"))

    def requires(self):
        return DownloadRawData(self.config, self.file_name)

    def run(self):
        # Iterating over PGN file
        createOutputDirectoryFromFilename(self.output().path)
        with open(self.input().path) as pgn:
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
                    # Drop move counters
                    posn = node.board().fen()
                    positions.append(posn)
                    node = next_node
                counter += 1
                print("Processing Game: " + str(counter) + ", Unique positions: " + str(len(positions)))
        positions = numpy.unique(positions);
        d = {"position": positions}
        df = pandas.DataFrame(d)
        df.to_csv(self.output().path, index=False)


# Compute the position scores for every position in this file
class ComputePositionScores(luigi.Task):
    config = luigi.Parameter()
    file_name = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(self.input().path.replace("position_data", "target_data"))

    def requires(self):
        return ExtractUniquePositions(self.config, self.file_name)

    def run(self):
        createOutputDirectoryFromFilename(self.output().path)
        # Feeding input to and getting output from stockfish binary
        positions = pandas.read_csv(self.input().path)
        positions = positions["position"].values.tolist()

        stockfish_cmd = self.config["stockfish_path"]
        engine = subprocess.Popen(stockfish_cmd, universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)

        def put(command):
            # print('\nyou:\n\t'+command)
            engine.stdin.write(command + '\n')

        def get():
            # using the 'isready' command (eng has to answer 'readyok')
            # to indicate current last line of stdout
            t = "";
            engine.stdin.write('isready\n')
            # print('\nengine:')
            while True:
                text = engine.stdout.readline().strip()
                if text == 'readyok':
                    break
                if text != '':
                    # print('\t'+text)
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
            #sprint("Evaluating position:" + str(ix) + " of " + numPos)

        engine.kill()

        # Save to csv
        d = {"position": positions, "score": evals}
        df = pandas.DataFrame(d)
        df.to_csv(self.output().path, index=False)

# Generate feature matrix for every unique position in this file
class GenerateFeatureMatrix(luigi.Task):
    config = luigi.Parameter()
    file_name = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(self.input().path.replace("target_data", "feature_data"))

    def requires(self):
        return ComputePositionScores(self.config, self.file_name)

    def run(self):
        createOutputDirectoryFromFilename(self.output().path)
        data = pandas.read_csv(self.input().path)
        # Generate features
        features = []
        for ix, row in data.iterrows():
            print "processing board: " + str(ix)
            board = chess.Board(row["position"])

            fenString = row["position"].split(" ")
            positionString = fenString[0]

            position_features = { "IsWhite": [] , "IsBlack": [], "P": [], "R": [], "N": [], "B": [], "Q": [], "K": []}

            for ix, char in enumerate(positionString):
                if char == "/":
                    continue
                if isnumeric(char):
                    count = 0
                    while count < int(char):
                        for k in position_features.keys():
                            position_features[k].append(0)
                        count += 1
                else:
                    # Assign white/black first
                    if char.lower() == char:
                        position_features["IsBlack"].append(1)
                        position_features["IsWhite"].append(0)
                    else:
                        position_features["IsBlack"].append(0)
                        position_features["IsWhite"].append(1)
                    # Assign individual piece
                    for k in position_features.keys():
                        # Assign 1 to the appropriate column
                        if k.lower() == char.lower():
                            position_features[k].append(1)
                        # Assign zero if it's a piece, but not this piece
                        elif len(k) == 1:
                            position_features[k].append(0)
            thisObs = []
            for k in position_features.keys():
                thisObs = thisObs + position_features[k]

            if fenString[1] == "b":
                thisObs = thisObs + [0,1]
            else:
                thisObs = thisObs + [1, 0]

            print "Position:  " + positionString + " processed"
            features.append(thisObs)


        colnames = []
        for i in range(0,64):
            for k in position_features.keys():
                colnames.append(k + "_" + str(i))
        colnames = colnames + ["IsWhiteTurn","IsBlackTurn"]

        out = numpy.array(features)
        df = pandas.DataFrame(data=out,columns=colnames)
        df["label"] = data["score"]
        df.to_csv(self.output().path, index=False)
        print "done"

