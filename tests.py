from run import load_inverted_index;
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt1
import statistics
import collections

test_queries = open('BenchmarkDatasets/nyt/TIME.QUE','r');
test_queries_lines = test_queries.readlines();

test_rel_docs = open('BenchmarkDatasets/nyt/TIME.REL','r');
test_rel_docs_lines = test_rel_docs.readlines();

def time_dataset_test():
    queries = {};
    query_num = 0;
    for line in test_queries_lines:
        cur_line = line.split();
        if len(cur_line) > 0 and cur_line[0] == "*FIND":
            query_num += 1;
            continue;
        if len(cur_line) > 0 and query_num != 0:
            if query_num not in queries:
                queries[query_num] = " ".join(cur_line);
            else:
                queries[query_num] = queries[query_num] + " " + " ".join(cur_line);
    return queries;

def time_dataset_relevant_docs():
    rel_docs_map = {};
    for rel_doc in test_rel_docs_lines:
        rel_docs_list = rel_doc.split();
        if len(rel_docs_list) > 0:
            rel_docs_map[int(rel_docs_list[0])] = [];
            for doc_num in rel_docs_list:
                if int(doc_num) not in rel_docs_map:
                    rel_docs_map[int(rel_docs_list[0])].append(int(doc_num));
    return rel_docs_map;

def evaluator(docs_ranking, relevent_docs_list, relevance_matrix, query_num, precisions_vector, recalls_vector, all_relevant_docs_lengths):
    average_vector = [];
    for doc_number in docs_ranking:
        if int(doc_number) in relevent_docs_list:
            if query_num not in relevance_matrix:
                relevance_matrix[query_num] = [];
            relevance_matrix[query_num].append(1);
        else:
            if query_num not in relevance_matrix:
                relevance_matrix[query_num] = [];
            relevance_matrix[query_num].append(0);
    counter = 1;
    ones = 1;
    for val in relevance_matrix[query_num]:
        if val == 1:
            precision = ones/counter;
            average_vector.append(precision);
            ones += 1;
        counter += 1;

    if len(average_vector) > 0:
        precisions_vector.append(sum(average_vector) / len(average_vector))
    else:
        precisions_vector.append(0);
    recall_calculator(docs_ranking, relevent_docs_list,recalls_vector, all_relevant_docs_lengths);

def plot(precisionVector = []):
    plt.plot(precisionVector)
    plt.ylabel('average query precision');
    plt.xlabel('query number');
    plt.show()

def plot_recalls(recallVector):
    plt1.plot(recallVector)
    plt1.ylabel('best recalls for each query');
    plt1.xlabel('query number');
    plt1.show()

def plot_average_precision_or_recall_distribution(list, xLabel):
    plt.hist(list, bins='auto', color='#0504aa');
    plt1.ylabel('frequency');
    plt1.xlabel(xLabel);
    plt1.show()

def plot_average_precision_against_lengths(precisions_vector, lengths, xLabel):
    plt.scatter(precisions_vector, lengths);
    plt.ylabel('query length and number');
    plt.xlabel('average query precision');
    plt.show()

def recall_calculator(docs_ranking, relevent_docs_list,recalls_vector,all_relevant_docs_lengths):
    total_relevant_docs = len(relevent_docs_list);
    all_relevant_docs_lengths.append(total_relevant_docs);
    recall_count = 0;
    for doc in docs_ranking:
        if int(doc) in relevent_docs_list:
            recall_count += 1;
    if len(relevent_docs_list) > 0:
        recalls_vector.append(recall_count/total_relevant_docs);
    else:
        recalls_vector.append(1);

def performance_evaluations(queries_map, relevent_docs_map):
    relevance_matrix = {};
    precisions_vector = [];
    recalls_vector = [];
    all_relevant_docs_lengths = [];
    for i in range(len(queries_map)):
        docs_ranking = load_inverted_index(queries_map[i+1], 'test');
        evaluator(docs_ranking, relevent_docs_map[i+1], relevance_matrix, i+1, precisions_vector, recalls_vector, all_relevant_docs_lengths);
        # recall_calculator(docs_ranking, relevent_docs_map[i+1], relevance_matrix, i+1, recall_vector);
    print(sum(precisions_vector)/len(precisions_vector));
    plot(precisions_vector);
    plot_recalls(recalls_vector);
    plot_average_precision_or_recall_distribution(precisions_vector, 'average precision values');
    plot_average_precision_or_recall_distribution(recalls_vector, 'final recall values');
    plot_average_precision_against_lengths(precisions_vector, all_relevant_docs_lengths, 'average query precision');
    plot_average_precision_against_lengths(recalls_vector, all_relevant_docs_lengths, 'final recall values')
    print("median of precisions: ",statistics.median(precisions_vector));
    print("median of recall values: ",statistics.median(recalls_vector));
    print("mode of precisions: ",statistics.mode(precisions_vector));
    print("Total number of majority values: ", precisions_vector.count(statistics.mode(precisions_vector)));
    print("mode of recall values: ",statistics.mode(recalls_vector));

def perform_test_action():
    performance_evaluations(time_dataset_test(), time_dataset_relevant_docs());

perform_test_action()
