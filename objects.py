import math

class TokenInfo:
    # Initializer / Instance Attributes
    def __init__(self):
        self.idf = 0.0
        self.occList = [];
        self.arrayLength = 0;

    def appendList(self, val):
        self.occList.append(val);
        self.arrayLength += 1;

    def getList(self):
        return self.occList;

    def setIDF(self, idfVal):
        self.idf = idfVal;

    def getIDF(self):
        return self.idf;

    def listLength(self):
        return self.arrayLength;

class TokenOccurence:
    def __init__(self, docRef, count):
        self.docRef = docRef;
        self.count = count;

    def getTokenOccurence(self):
        return [self.docRef.getDocInfo(), self.count];

    def getDocumentReference(self):
        return self.docRef;

    def getDocumentTermCount(self):
        return self.count;

class DocumentReference:
    def __init__(self, file, length):
        self.file = file;
        self.length = length;

    def getDocInfo(self):
        return [self.file, self.length];

    def getDocLength(self):
        return self.length;

    def addDocLength(self, val):
        raw_length = math.pow(self.length, 2);
        squared_val = math.pow(val, 2);
        self.length = math.sqrt(raw_length + val);
