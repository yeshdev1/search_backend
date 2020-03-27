from nltk.stem import PorterStemmer
import string
from objects import TokenInfo, TokenOccurence, DocumentReference
from inverted_index import accumulate
from nltk.stem import WordNetLemmatizer

documents = open('BenchmarkDatasets/nyt/TIME.ALL','r');
documents_lines = documents.read();

stopwords = open('BenchmarkDatasets/nyt/TIME.STP','r');
stopwords_lines = stopwords.read();

def process_benchmark_sets(documents_list):
    stop_words = make_custom_stop_words_list();
    ps = PorterStemmer();
    punctuations = string.punctuation;
    words_dictionary = {};
    invertedIndex = {};
    document_numbers = 1;
    totalDocs = 0;
    offset = 0;
    for keyword in documents_list:
        if keyword != '*TEXT':
            keyword = ps.stem(keyword.lower());
            keyword = keyword.strip(string.punctuation);
            if keyword not in stop_words and keyword not in punctuations:
                if keyword not in words_dictionary:
                    words_dictionary[keyword] = 0;
                words_dictionary[keyword] += 1;
        elif (keyword == '*TEXT' and (not words_dictionary) == False) or (keyword == '*STOP'):
            accumulate(words_dictionary,invertedIndex,document_numbers);
            words_dictionary = {};
            totalDocs = document_numbers;
            document_numbers += 1;
    return [invertedIndex,totalDocs];

def make_custom_stop_words_list():
    stopwords_list = stopwords_lines.split();
    stopwords_list = [x.lower() for x in stopwords_list];
    return stopwords_list;

def benchmark_process():
    documents_list = documents_lines.split();
    return process_benchmark_sets(documents_list);
