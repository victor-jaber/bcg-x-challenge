# ========================================================================== #
### Common functions used in the project
# ========================================================================== #

## Importing libraries
import os
import ast
import PyPDF2
import duckdb
import logging
from pathlib import Path
from datetime import datetime


def get_dir_proj():
    '''
    Returns the absolute path to the main.py
    '''
    dir_proj, _ = os.path.split(os.path.abspath(__file__))
    dir_proj = dir_proj.replace(os.sep, "/")
    dir_proj = "/".join(dir_proj.split("/")[:-1])
    return dir_proj


def get_dir_config():
    '''
    Returns the absolute path to the config.ini
    '''
    dir_proj, _ = os.path.split(os.path.abspath(__file__))
    dir_proj = dir_proj.replace(os.sep, "/")
    dir_proj = "/".join(dir_proj.split("/")[:-1])
    ini_config = str(Path(dir_proj, "config", "config.ini").resolve()).replace("\\", "/")
    return ini_config


def log(config):
    '''
    Writes the execution log in a txt file
    '''
    # Configuration for execution log
    dt = datetime.now().strftime('%Y%m%d_%H%M%S')
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[logging.FileHandler(f'{get_dir_proj()}/log/{dt}_log.txt'),   # write in a txt file
                                 logging.StreamHandler()                                       # print in the terminal
                                 ]
                        )
    logging.getLogger("httpx").setLevel(logging.WARNING) # disable hhtp request message in the log file
    logging.info(f'Configured the log function. Log file in {get_dir_proj()}/log/{dt}_log.txt')
    # Only keeps the recent logs files
    num_files = ast.literal_eval(config["LOG"]["NUM_FILES"]) # number of files that will be stored
    keep_recent_logs(num_files, logging)
    return logging


def keep_recent_logs(num_files, logger):
    '''
    Only keeps the recent logs files.
    num_files is the number of files that will be kept
    '''
    # File path
    log_path = f'{get_dir_proj()}/log'

    # Sort files in descending order by name
    log_list = [f for f in os.listdir(log_path) if os.path.isfile(os.path.join(log_path, f).replace("\\", "/"))]
    log_list.sort(reverse=True)

    # Keeps only the most recent files
    to_remove = log_list[num_files:]
    for f in to_remove:
        try:
            os.remove(os.path.join(log_path, f).replace("\\", "/"))
            logger.info(f"Only keeps the last {num_files} log files. Files removed: {to_remove}")
        except Exception as err:
            logger.error(f'Unable to delete log file. Error: {err}')


def read_pdf(file_name, logger):
    '''
    Read the PDF file
    '''
    dir_proj = get_dir_proj()
    try:
        file = open(f'{dir_proj}/database/raw_data/{file_name}', 'rb')
        reader = PyPDF2.PdfReader(file)
        logger.info('>>> PDF file read successfully')
        return reader.pages, file
    except Exception as err:
        logger.error(f'>>> Unable to read PDF file. Error: {err}')
        exit()


def database_connection(database_name):
    """
    Creates the connection with de duckdb database
    """
    dir_proj = get_dir_proj()
    conn = duckdb.connect(f'{dir_proj}/database/{database_name}')
    return conn


def database_exists(logger):
    '''
    Check if the duckdb database already exists
    '''
    database_path = f'{get_dir_proj()}/database'
    if 'datalake.db' in os.listdir(database_path):
        logger.info('duckdb database already exists!')
        return True
    logger.info('duckdb database does not exists')
    return False