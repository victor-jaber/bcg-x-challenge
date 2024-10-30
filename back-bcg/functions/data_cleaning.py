# ========================================================================== #
### Auxiliary functions for cleaning and processing data
# ========================================================================== #

import re
import spacy
from nltk.corpus import stopwords


def remove_header(text, start):
    '''
    Remove the header, that is, starts the extraction from the position 
    specified in the variable start 
    '''
    return text[start:]


def remove_end(text, end):
    '''
    Remove end of file. In general, it is the page number (page footer)
    '''
    if end == 0:
        return text
    return text[:end]


def remove_unwanted_chr(text, chr):
    '''
    Replaces all occurrences of chr in the text with ' '
    '''
    for x in chr:
        text = re.sub(x, ' ', text)
    return text


def remove_stopwords(text):
    '''
    Remove stop words from text
    '''
    stop_words = set(stopwords.words('portuguese'))
    word_tokens = text.split(' ')
    text_filt = [word for word in word_tokens if word.lower() not in stop_words]
    text_filt = " ".join(text_filt)
    return text_filt


def lemmatize_text(text):
    '''
    Function for text lemmatization
    '''
    # Upload the model to Portuguese
    nlp = spacy.load('pt_core_news_sm')
    
    # Returns the lemma
    text = nlp(text)
    lemmas = [token.lemma_ for token in text]
    return ' '.join(lemmas)


def remove_white_space(text):
    '''
    Removes additional whitespace in the string.
    '''
    return ' '.join(text.split())


def cleaning_user_query(text):
    '''
    Cleaning and treatment of user query text
    '''
    text = remove_unwanted_chr(text, ["\n", "\xa0"])
    text = remove_stopwords(text)
    text = lemmatize_text(text)
    text = remove_white_space(text)
    return text