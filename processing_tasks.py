import luigi, pandas, urllib2, os

from project_utils import *

# Get the games file
class DownloadRawData(luigi.Task):
    config = luigi.Parameter()

    def output(self):
        return os.path.join(self.config["data_repository"],"raw_data","CCRL_4040_all.pgn")

    def run(self):
        createOutputDirectoryFromFilename(self.output())
        response = urllib2.urlopen(self.config["data_url"])
        file_contents = response.read()
        with open(self.output(),"w") as f:
            f.write(file_contents)

# Split raw data into a list of files each containing n games
class SplitRawData(luigi.Task):
    config = luigi.Parameter()

    def output(self):
        return []

    def requires(self):
        return DownloadRawData(self.config)

    def run(self):
        return []

class ExtractUniquePositions(luigi.Task):
    config = luigi.Parameter()
    file_name = luigi.Parameter()

    def output(self):
        return []

    def requires(self):
        return DownloadRawData(self.config)

    def run(self):
        return []


# Compute the position scores for every position in this file
class ComputePositionScores(luigi.Task):
    config = luigi.Parameter()
    file_name = luigi.Parameter()

    def output(self):
        return []

    def requires(self):
        return []

    def run(self):
        return []

# Generate feature matrix for every unique position in this file
class GenerateFeatureMatrix(luigi.Task):
    config = luigi.Parameter()
    file_name = luigi.Parameter()

    def output(self):
        return []

    def requires(self):
        return []

    def run(self):
        return []

# Remove duplicate records from input data; output feature matrices and position scores with duplicates removed
class ReduceInputData(luigi.Task):
    config = luigi.Parameter()


    def output(self):
        return []

    def requires(self):
        return []

    def run(self):
        return []