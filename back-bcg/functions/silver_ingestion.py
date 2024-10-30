import ast
from configparser import ConfigParser
from functions.utils import read_pdf, database_connection, get_dir_config
from functions.data_cleaning import remove_end, remove_header, remove_unwanted_chr, remove_stopwords, lemmatize_text, remove_white_space


def silver_data_ingestion(pdf_name, table_name, logger):
    '''
    Data ingestion in the silver layer
    '''
    # Read the PDF file
    doc, file = read_pdf(pdf_name, logger)

    # Read the config.ini file in order to get the create/insert table command and 
    # some variables for data cleaning
    ini_config = get_dir_config()
    config = ConfigParser()
    config.read(ini_config, encoding="utf8")

    # Read de variables for data cleaning
    unnecessary_pages = ast.literal_eval(config["PROCESSING"][table_name])["unnecessary_pages"] # list of unnecessary pages
    correct_header = ast.literal_eval(config["PROCESSING"][table_name])["correct_header"] # list of pages with correct header
    header = ast.literal_eval(config["PROCESSING"][table_name])["header"] # number of characters that should be ignored at the beginning of each page
    unwanted_chr = ast.literal_eval(config["PROCESSING"][table_name])["unwanted_chr"] # list of unwanted characters
    end = ast.literal_eval(config["PROCESSING"][table_name])["end"] # number of characteres that should be ignored at the end of each page

    # Read the text of each page, applies data cleaning and stores it in a tuple
    ingestion_data = []
    i = 1
    for page in doc:
        # Unnecessary pages are converted to empty string
        if i in unnecessary_pages:
            page_content = ' '
        # Data cleaning
        else:
            page_content = page.extract_text()
            if i not in correct_header:
                page_content = remove_header(page_content, header)
            page_content = remove_unwanted_chr(page_content, unwanted_chr)
            page_content = remove_end(page_content, end)
            page_content = remove_stopwords(page_content)
            page_content = lemmatize_text(page_content)
            page_content = remove_white_space(page_content)
        
        # Store the data in a tuple
        doc_tuple = (i, page_content)
        ingestion_data.append(doc_tuple)
        i += 1
    logger.info('>>> Processed data stored in a tuple')
    
    # Connects to the database
    conn = database_connection("datalake.db")
    cursor = conn.cursor()

    # Create the silver schema
    create_schema = config["CREATE_SCHEMA"]["SILVER"]
    cursor.execute(create_schema)
    conn.commit()

    # Add the table name in the SQL command
    create_table = (config["CREATE_TABLE"]["SILVER"]).replace("#TABLE#", table_name)
    insert_table = (config["INSERT_TABLE"]["SILVER"]).replace("#TABLE#", table_name)

    # Create the silver table
    cursor.execute(create_table)
    conn.commit()
    logger.info('>>> Silver table created')

    # Insert data into the silver table
    conn.executemany(insert_table, ingestion_data)
    logger.info(f'>>> Data inserted into the silver table (silver.{table_name}) successfully')

    # Closes the file and connection
    file.close()
    cursor.close()
    conn.close()
    logger.info('----------------------------------------------------------------------')
    return ingestion_data
    