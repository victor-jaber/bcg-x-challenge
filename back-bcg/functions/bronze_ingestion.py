from functions.utils import read_pdf, database_connection, get_dir_config
from configparser import ConfigParser


def bronze_data_ingestion(pdf_name, table_name, logger):
    '''
    Data ingestion in the bronze layer
    '''
    # Read the PDF file
    doc, file = read_pdf(pdf_name, logger)

    # Read the text of each page and stores it in a tuple
    ingestion_data = []
    i = 1
    for page in doc:
        doc_tuple = (i, page.extract_text())
        ingestion_data.append(doc_tuple)
        i += 1
    logger.info('>>> File content stored in a tuple')

    # Creates the database
    conn = database_connection("datalake.db")
    cursor = conn.cursor()

    # Read the config.ini file in order to get the create/insert table command
    ini_config = get_dir_config()
    config = ConfigParser()
    config.read(ini_config, encoding="utf8")

    # Create the bronze schema
    create_schema = config["CREATE_SCHEMA"]["BRONZE"]
    cursor.execute(create_schema)
    conn.commit()

    # Add the table name in the SQL command
    create_table = (config["CREATE_TABLE"]["BRONZE"]).replace("#TABLE#", table_name)
    insert_table = (config["INSERT_TABLE"]["BRONZE"]).replace("#TABLE#", table_name)

    # Create the bronze table
    cursor.execute(create_table)
    conn.commit()
    logger.info('>>> Bronze table created')

    # Insert data into the bronze table
    conn.executemany(insert_table, ingestion_data)
    logger.info(f'>>> Data inserted into the bronze table (bronze.{table_name}) successfully')

    # Closes the file and connection
    file.close()
    cursor.close()
    conn.close()
    logger.info('----------------------------------------------------------------------')