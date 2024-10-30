from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import NLTKTextSplitter


def text_splitter(text, chunk_size, chunk_overlap):
    '''
    Function to divide text into smaller parts
    '''
    text_split = NLTKTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    if len(text_split.split_text(text)) == 0:
        return [' ']
    return text_split.split_text(text)


def embedding_func(embedding, text):
    '''
    Function to transform a string into a vector of numbers
    '''
    return embedding.embed_query(text) 


def create_embbedings(text, chunk_size, chunk_overlap, embedding):
    '''
    Applies the embedding to each part of the text
    '''
    embedding_chunk_list = []
    text_split = text_splitter(text, chunk_size, chunk_overlap)
    for t in text_split:
        emb = embedding_func(embedding, t)
        embedding_chunk_list.append(emb)

    return embedding_chunk_list


def embedding_doc(doc, chunk_size, chunk_overlap, model, open_api_key):
    '''
    Returns a float vector corresponding to the document text
    '''
    # Instance embedding function
    embedding = OpenAIEmbeddings(model=model,
                                openai_api_key = open_api_key
                                )

    # Iterates over the document pages to return the float vector
    embeddings_list = []
    for index in range(len(doc)):
        try:
            emb = create_embbedings(doc[index][1], chunk_size, chunk_overlap, embedding)
            embeddings_list.append(emb)
        except:
            print(f"Error while retriving embeddings for document number {index}.")
    return embeddings_list