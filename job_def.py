if __name__ == "__main__":

    # Some required luigi imports
    import luigi, os, logging, pandas, json, sys, requests
    import luigi.scheduler
    import luigi.worker
    from datetime import date, datetime, timedelta
    from project_utils import *
    from processing_tasks import *
    from bs4 import BeautifulSoup, SoupStrainer



    if len(sys.argv) < 2:
        raise Exception("No config file path provided, exiting")
    else:
        configPath = sys.argv[1]

    # Load config
    with open(configPath) as f:
        config = json.load(f)

    # use beautiful-soup to get a list of files
    file_list = []
    response = requests.get(config["data_url"])
    soup = BeautifulSoup(response.text)
    for link in soup.find_all('a'):
        if link.has_attr('href'):
            if "7z" in link["href"] and "CCRL-4040" not in link["href"]:
                file_list.append(config["data_url"].replace("games.html","") + link['href'])
    config["file_list"] = file_list[0:2]  # For testing

    # Create data repository if it doesn't yet exist
    createOutputDirectoryFromFilename(os.path.join(config["data_repository"],"fu.txt"))

    # Set up logging
    log_path = os.path.join(config["data_repository"], "process_log.log")
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    log_handle = logging.FileHandler(log_path)
    log_handle.setFormatter(formatter)
    logger = logging.getLogger('luigi-interface')
    logger.setLevel(logging.ERROR)
    logger.addHandler(log_handle)


    tasks = []

    # TASKS:
    # 1.  Download input files
    # 2.  Generate list of unique positions
    # 3.  Generate feature matrix for each unique position (and it's permutation?)
    # 4.  Run Stockfish to generate position scores
    # 5.  Build some models
    # 6.  Evaluate the models
    for fl in config["file_list"]:
        tasks.append(DownloadRawData(config, fl))
        tasks.append(ExtractUniquePositions(config, fl))
        tasks.append(ComputePositionScores(config, fl))
        tasks.append(GenerateFeatureMatrix(config, fl))


    luigi.build(tasks, local_scheduler=True,workers=1)
