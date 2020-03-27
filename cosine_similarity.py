import math;
import operator;

def document_ranking(document_scores,length_of_query,doc_length):
    doc_ranking = {};
    for doc in document_scores:
        s = document_scores[doc];
        y = doc_length[doc];
        doc_ranking[doc] = s/(y*length_of_query);
    #Sorting map here
    sorted_doc_ranking = dict(sorted(doc_ranking.items(), key=operator.itemgetter(1),reverse=True));
    return sorted_doc_ranking;

def query_length(query_terms):
    final_length = 0;
    for term in query_terms:
        final_length = final_length + math.pow(term[2], 2);
    return math.sqrt(final_length);

def retrieval_algorithm(query_terms, search_query_map):
    #Setting the term weight for each of the terms in the query retrieved array itself#
    document_scores = {};
    doc_length = {};
    for term in query_terms:
        idf = term[2];
        term[2] = term[2]*search_query_map[term[1]];
        for tokenOccurence in term[4]:
            split_tokenOccurence = tokenOccurence.split(",");
            doc_name = split_tokenOccurence[0].replace("[", "");
            if doc_name not in doc_length:
                doc_length[doc_name] = float(split_tokenOccurence[1].replace(" ", "").replace("]",""));
            if doc_name not in document_scores:
                document_scores[doc_name] = 0.0;
            term_count = int(split_tokenOccurence[2].replace(" ", "").replace("]",""));
            document_scores[doc_name] += term[2]*idf*term_count;
    return [document_scores, doc_length];

def cosine_similarity_calculation(query_terms, search_query_map):
    [document_scores,doc_length] = retrieval_algorithm(query_terms, search_query_map);
    length_of_query = query_length(query_terms);
    return document_ranking(document_scores,length_of_query,doc_length);
