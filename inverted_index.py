from sys import stdin
import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from objects import TokenInfo, TokenOccurence, DocumentReference
from nltk.stem import PorterStemmer

def accumulate(words_dictionary, inverted_index, document_reference_location):
    documentReference = DocumentReference(document_reference_location, 0.0);
    for word in words_dictionary:
        if word not in inverted_index:
            tokenInfo = TokenInfo();
            inverted_index[word] = tokenInfo;
        tokenOccurence = TokenOccurence(documentReference, words_dictionary[word]);
        inverted_index[word].appendList(tokenOccurence);

def process_websites(tokens):
    words_cleaned = [];
    ps = PorterStemmer();
    stop_words = stopwords.words('english');
    punctuations = string.punctuation;
    for token in tokens:
        token = token.lower();
        token = ps.stem(token);
        token.strip(string.punctuation);
        if len(token) > 0 and token not in punctuations and token not in stop_words:
            words_cleaned.append(token);
    return words_cleaned;

def process_pdfwords(tokens):
    ps = PorterStemmer();
    stop_words = stopwords.words('english');
    punctuations = string.punctuation;
    lower_tokens = (word.lower() for word in tokens);
    keywords = [word for word in lower_tokens if not word in stop_words and not word in punctuations];
    keywords = [word for word in keywords if word.isalnum() == True];
    return keywords;

def choose_word_processor(type, tokens):
    if type == 'pdfs':
        return process_pdfwords(tokens);
    elif type == 'websites':
        return process_websites(tokens);

#mapper usuallty gets the word count in a document.#
def mapper(type, tokens):
    keywords = choose_word_processor(type, tokens);
    words_dictionary = {};
    for keyword in keywords:
        if keyword not in words_dictionary:
            words_dictionary[keyword] = 1;
        else:
            words_dictionary[keyword] += 1;
    return words_dictionary;

def reducer(words_dictionary, inverted_index, document_reference):
    #accumulate
    accumulate(words_dictionary, inverted_index, document_reference);
