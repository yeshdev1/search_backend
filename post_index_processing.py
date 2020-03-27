import math

def idf_calculate(invertedIndex, totalDocs):
    for token in invertedIndex:
        numDocsOccurence = invertedIndex[token].listLength();
        invertedIndex[token].setIDF(math.log(totalDocs/numDocsOccurence,2));

def document_vector_length(invertedIndex):
    for token in invertedIndex:
        postings = invertedIndex[token].getList();
        currentIDF = invertedIndex[token].getIDF();
        for posting in postings:
            documentReference = posting.getDocumentReference();
            wordCountInCurrentDocument = posting.getDocumentTermCount();
            currentDocumentLength = currentIDF * wordCountInCurrentDocument;
            documentReference.addDocLength(currentDocumentLength);
