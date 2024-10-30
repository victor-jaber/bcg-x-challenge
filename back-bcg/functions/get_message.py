from configparser import ConfigParser
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from functions.data_cleaning import cleaning_user_query
from functions.utils import database_connection, get_dir_config
from functions.embedding import embedding_func

import time
from database import get_messages_dict

def get_embeddings(text, model, openai_api_key):
    '''
    Function to transform a string into a vector of numbers
    '''
    embedding = OpenAIEmbeddings(model=model,
                                openai_api_key = openai_api_key
                                )
    emb = embedding_func(embedding, text)
    return emb


def retrive_similar_docs(query_embedding, conn, limit=10):
    '''
    Retrieve similar documents based on user input.
    The search is done using cosine similarity
    '''
    cur = conn.cursor()
    query = f"""
        SELECT content, embedding <=> {query_embedding} as cos_sim FROM 
            (
            SELECT 
                content, embedding
            FROM
            silver.enfrentamento_nacional t1
            LEFT JOIN gold.enfrentamento_nacional t2 ON (t1.page_number = t2.page_number)

            UNION 

            SELECT 
                content, embedding
            FROM
            silver.plano_curitiba t1
            LEFT JOIN gold.plano_curitiba t2 ON (t1.page_number = t2.page_number)

            UNION 


            SELECT 
                content, embedding
            FROM
            silver.plano_agro t1
            LEFT JOIN gold.plano_agro t2 ON (t1.page_number = t2.page_number)

            UNION 

            SELECT 
                content, embedding
            FROM
            silver.plano_nacional t1
            LEFT JOIN gold.plano_nacional t2 ON (t1.page_number = t2.page_number)

            UNION 

            SELECT 
                content, embedding
            FROM
            silver.plano_sp t1
            LEFT JOIN gold.plano_sp t2 ON (t1.page_number = t2.page_number)

            UNION 

            SELECT 
                content, embedding
            FROM
            silver.plano_federal t1
            LEFT JOIN gold.plano_federal t2 ON (t1.page_number = t2.page_number)

            UNION 

            SELECT 
                content, embedding
            FROM
            silver.plano_itabirito t1
            LEFT JOIN gold.plano_itabirito t2 ON (t1.page_number = t2.page_number)

            UNION 

            SELECT 
                content, embedding
            FROM
            silver.plano_joao_pessoa t1
            LEFT JOIN gold.plano_joao_pessoa t2 ON (t1.page_number = t2.page_number)
            )
        ORDER BY (embedding <=> {query_embedding}) LIMIT {limit}
        """
    cur.execute(query)
    top_docs = cur.fetchall()
    return top_docs


from configparser import ConfigParser
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from functions.data_cleaning import cleaning_user_query
from functions.utils import database_connection, get_dir_config
from functions.embedding import embedding_func


def get_embeddings(text, model, openai_api_key):
    '''
    Function to transform a string into a vector of numbers
    '''
    embedding = OpenAIEmbeddings(model=model,
                                  openai_api_key=openai_api_key)
    emb = embedding_func(embedding, text)
    return emb


def retrive_similar_docs(query_embedding, conn, limit=10):
    '''
    Retrieve similar documents based on user input.
    The search is done using cosine similarity
    '''
    cur = conn.cursor()
    query = f"""
        SELECT content, embedding <=> {query_embedding} as cos_sim FROM 
            (
            SELECT 
                content, embedding
            FROM
            silver.enfrentamento_nacional t1
            LEFT JOIN gold.enfrentamento_nacional t2 ON (t1.page_number = t2.page_number)

            UNION 

            SELECT 
                content, embedding
            FROM
            silver.plano_curitiba t1
            LEFT JOIN gold.plano_curitiba t2 ON (t1.page_number = t2.page_number)

            UNION 

            SELECT 
                content, embedding
            FROM
            silver.plano_agro t1
            LEFT JOIN gold.plano_agro t2 ON (t1.page_number = t2.page_number)

            UNION 

            SELECT 
                content, embedding
            FROM
            silver.plano_nacional t1
            LEFT JOIN gold.plano_nacional t2 ON (t1.page_number = t2.page_number)

            UNION 

            SELECT 
                content, embedding
            FROM
            silver.plano_sp t1
            LEFT JOIN gold.plano_sp t2 ON (t1.page_number = t2.page_number)

            UNION 

            SELECT 
                content, embedding
            FROM
            silver.plano_federal t1
            LEFT JOIN gold.plano_federal t2 ON (t1.page_number = t2.page_number)

            UNION 

            SELECT 
                content, embedding
            FROM
            silver.plano_itabirito t1
            LEFT JOIN gold.plano_itabirito t2 ON (t1.page_number = t2.page_number)

            UNION 

            SELECT 
                content, embedding
            FROM
            silver.plano_joao_pessoa t1
            LEFT JOIN gold.plano_joao_pessoa t2 ON (t1.page_number = t2.page_number)
        )
        ORDER BY (embedding <=> {query_embedding}) LIMIT {limit}
    """
    cur.execute(query)
    top_docs = cur.fetchall()
    return top_docs

def format_response(response):
    """
    Formata a resposta do chatbot em HTML.
    """
    response = response.replace("**", "<strong>").replace("<strong>", "<strong>", 1).replace("</strong>", "</strong>", 1)
    
    response = response.replace("\n1. ", "<ul><li>").replace("\n2. ", "</li><li>").replace("\n3. ", "</li><li>")
    response += "</li></ul>" 
    
    return response


def get_completion_from_messages(messages, openai_api_key):
    '''
    Model return from system message.
    '''
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        openai_api_key=openai_api_key,
        max_tokens=8000,
        temperature=0.6,
        top_p=0.7)
    
    return llm.invoke(messages)


def process_input_with_retrieval(user_query, logger):
    '''
    Returns the model response to the user query.
    '''
    start_time = time.time()  # Início do monitoramento do tempo total

    # Connects to the database
    conn = database_connection("datalake.db")

    # Processing and cleaning data in the user query
    user_query = cleaning_user_query(user_query)
    logger.info('Processing and cleaning data from the user query completed successfully')

    # Get the parameters for the model
    ini_config = get_dir_config()
    config = ConfigParser()
    config.read(ini_config, encoding="utf8")

    openai_api_key = config['EMBEDDING']['OPEN_API_KEY']
    model = config['EMBEDDING']['MODEL']

    # Retrieve chat history from the database as a list of dictionaries
    chat_history = get_messages_dict()  # Assume this function returns [{'role': 'user', 'content': '...'}, ...]

    # Limit the history to a maximum number of messages for context management.
    max_history_length = 3  # Adjust as necessary for your use case.
    
    messages_to_pass = chat_history[-max_history_length:]  # Get the last N messages

    # Prepare the messages for LLM context.
    messages = [("system", "Você é um assistente de inteligência artificial desenhado para apoiar gestores municipais em uma ampla gama de atividades.")]
    
    # Append previous messages to maintain context.
    for msg in messages_to_pass:
        messages.append((msg['role'], msg['content']))

    # Add current user query to the messages.
    messages.append(("human", user_query))

    # Transforms the user query into a vector.
    emb = get_embeddings(user_query, model, openai_api_key)
    
    logger.info('Transformed the user query into a float vector')

    # Retrieve similar documents based on user input.
    related_docs = retrive_similar_docs(emb, conn, limit=3)
    
    logger.info('Retrieved similar documents based on user input')

    # Ensure there are at least one document.
    if len(related_docs) == 0:
        logger.info('No documents relevant to the question were found')
        return "Desculpe, não foram encontrados documentos relevantes para a sua pergunta"

    # Append related documents to context if necessary (optional).
    for i in range(len(related_docs)):
        messages.append(("system", f"Documento {i + 1}: {related_docs[i][0]}"))

    max_retries = 5  
    final_response = None

    for attempt in range(max_retries + 1):
        final_response = get_completion_from_messages(messages, openai_api_key)

        if final_response.content:
            break  
        
        logger.warning(f'Resposta não recebida na tentativa {attempt + 1}. Tentando novamente...')
        
        time.sleep(2)  # Adiciona um delay de 2 segundos antes da próxima tentativa

    if not final_response or not final_response.content:
        logger.info('Could not generate a response after retries')
        return "Desculpe, não foi possível gerar uma resposta. Por favor, tente novamente."

    logger.info('Final response generated successfully')
    
    elapsed_time = time.time() - start_time  # Tempo total gasto
    logger.info(f'Tempo total gasto: {elapsed_time:.2f} segundos')

    formatted_response = format_response(final_response.content)

    return formatted_response
