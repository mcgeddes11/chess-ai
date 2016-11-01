if __name__ == "__main__":

    # Some required luigi imports
    import luigi, os, logging, pandas, json, sys
    import luigi.scheduler
    import luigi.worker
    from datetime import date, datetime, timedelta
    from project_utils import *



    if len(sys.argv) < 2:
        raise Exception("No config file path provided, exiting")
    else:
        configPath = sys.argv[1]

    # Load config
    with open(configPath) as f:
        config = json.load(f)

    # Should get this from config
    config["n_games"] = 664473
    # get list of files based on number of games and split number

    # Create data repository if it doesn't yet exist
    createOutputDirectoryFromFilename(os.path.join(config["data_repository"],"fu.txt"))

    # Set up logging
    log_path = os.path.join(config["data_repository"], "process_log.log")
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    log_handle = logging.FileHandler(log_path)
    log_handle.setFormatter(formatter)
    logger = logging.getLogger('luigi-interface')
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handle)


    tasks = []

    # TASKS:
    # 1.  Download input file
    # 2.  Split file into chunks
    # 3.  Generate list of unique positions
    # 3.  Generate feature matrix for each unique position (and it's permutation?)
    # 4.  Run Stockfish to generate position scores
    # 5.  Build some models
    # 6.  Evaluate the models


    luigi.build(tasks, local_scheduler=True,workers=2)
