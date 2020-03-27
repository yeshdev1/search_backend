import sqlite3
from sqlite3 import Error
from document_processing import process
from post_index_processing import idf_calculate, document_vector_length
from cosine_similarity import cosine_similarity_calculation
from benchmark_data_processer import make_custom_stop_words_list, benchmark_process
import numpy as np
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import string
from crawler import crawl

def create_tasks_and_insert(conn, invertedIndex):
    for token in invertedIndex:
        idf = invertedIndex[token].getIDF();
        totalDocs = invertedIndex[token].listLength();
        tokenOccurences = invertedIndex[token].getList();
        occurenceString = "";
        for occurence in tokenOccurences:
            occurenceString = occurenceString + str(occurence.getTokenOccurence())+"  ";
        task = (token,idf,totalDocs,occurenceString);
        create_index(conn,task);

def create_index(conn, task):
    cur = conn.cursor();
    cur.execute("INSERT INTO indexes(token,idf,totalDocs,tokenOccurences) VALUES(?,?,?,?)", task);
    conn.commit();

def clear_tables_database(con):
    con.execute('DELETE from indexes');

def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect("invertedIndexes.db");
    except Error as e:
        print(e)
    return conn

def save_invertedIndex(invertedIndex):
    conn = create_connection();
    clear_tables_database(conn);
    create_tasks_and_insert(conn, invertedIndex);
    conn.close();

def run_preprocessing(type):
    if type == 'websites':
        [invertedIndex, totalDocs] = crawl();
    elif type == "pdfs":
        [invertedIndex, totalDocs] = process();
    else:
        [invertedIndex, totalDocs] = benchmark_process();
    idf_calculate(invertedIndex,totalDocs);
    document_vector_length(invertedIndex);
    save_invertedIndex(invertedIndex);

run_preprocessing('test');

def retrieve_query_related_terms(conn, search_query_map):
    cur = conn.cursor();
    token_info = [];
    for token in search_query_map:
        cur.execute('SELECT * from indexes where token=?',(token,));
        for record in cur.fetchall():
            token_info.append(record);
    return token_info;

def convert_list_to_map(query, type = 'not test'):
    search_query_map = {};
    split_query = query.split();
    ps = PorterStemmer();
    stop_words = {};
    if type == 'test':
        stop_words = make_custom_stop_words_list();
    else:
        stop_words = set(stopwords.words('english'));
    for word in split_query:
        finalWord = ps.stem(word.lower());
        finalWord = finalWord.strip(string.punctuation);
        if finalWord not in string.punctuation and finalWord not in stop_words:
            if finalWord not in search_query_map:
                search_query_map[finalWord] = 1;
            else:
                search_query_map[finalWord] += 1;
    return search_query_map;

def extract_links_only(link_and_ranks):
    links = [];
    for pair in link_and_ranks:
        links.append(pair);
    return links;

def load_inverted_index(user_query, type = 'none'):
    conn = create_connection();
    query = user_query;
    search_query_map = convert_list_to_map(query, type);
    relevant_rows = retrieve_query_related_terms(conn, search_query_map);
    query_terms = [];
    for row in relevant_rows:
        tokenOccurences = row[4].split("  ");
        del tokenOccurences[len(tokenOccurences) - 1];
        row = list(row);
        del row[4];
        row.append(tokenOccurences);
        query_terms.append(row);
    rankings = cosine_similarity_calculation(query_terms, search_query_map);
    return rankings;
    conn.close();
