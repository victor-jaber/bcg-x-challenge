import ast
import numpy as np
from configparser import ConfigParser
from functions.utils import get_dir_config, database_connection
from functions.embedding import embedding_doc


def gold_data_ingestion(table_name, silver_data, logger):
    '''
    Data ingestion in the gold layer
    '''
    # Get the parameters for embedding function
    ini_config = get_dir_config()
    config = ConfigParser()
    config.read(ini_config, encoding="utf8")

    open_api_key =  config['EMBEDDING']['OPEN_API_KEY']
    model = config['EMBEDDING']['MODEL']
    chunk_size = ast.literal_eval(config["EMBEDDING"]["CHUNK_SIZE"])
    chunk_overlap = ast.literal_eval(config["EMBEDDING"]["CHUNK_OVERLAP"])

    # Applies the embedding function to all silver layer data
    embeddings_list = embedding_doc(silver_data, chunk_size, chunk_overlap, model, open_api_key)
    logger.info('>>> Get the list of data after embedding function')

    # Organizes the data that will be ingested in the gold layer
    ingestion_data = []
    for page in range(1, len(embeddings_list)+1):
        try:
            doc_tuple = (page, np.array(embeddings_list[page-1][0]))
        except:
            doc_tuple = (page, [])
        ingestion_data.append(doc_tuple)
    logger.info('>>> The data that will be ingested into the gold layer were organized')
    
    # Connects to the database
    conn = database_connection("datalake.db")
    cursor = conn.cursor()

    # Create the gold schema
    create_schema = config["CREATE_SCHEMA"]["GOLD"]
    cursor.execute(create_schema)
    conn.commit()

    # Add the table name in the SQL command
    create_table = (config["CREATE_TABLE"]["GOLD"]).replace("#TABLE#", table_name)
    insert_table = (config["INSERT_TABLE"]["GOLD"]).replace("#TABLE#", table_name)

    # Create the silver table
    cursor.execute(create_table)
    conn.commit()
    logger.info('>>> Gold table created')

    # Insert data into the gold table
    conn.executemany(insert_table, ingestion_data)
    logger.info(f'>>> Data inserted into the gold table (gold.{table_name}) successfully')

    # Closes the connection
    cursor.close()
    conn.close()
    logger.info('----------------------------------------------------------------------')

