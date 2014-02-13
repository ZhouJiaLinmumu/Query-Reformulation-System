import string
import nltk
import math
stopwords = ['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear', 'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may', 'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor', 'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since', 'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet', 'you', 'your']


def keyWordEngine(query,targetPrec,relevant,nonrel):
    # finding N for calculating IDF
    N_Rel = len(relevant)
    N_Nonrel = len(nonrel)

    #finding TF
    tfRel =findTF(relevant)
    tfNonRel = findTF(nonrel)

    #finding IDF
    idfRel = findIDF(tfRel, N_Rel)
    idfNonRel = findIDF(tfNonRel, N_Nonrel)

    #finding terms with most weightage
    (maxRel,secMaxRel) = findWeights(tfRel, idfRel, nltk.word_tokenize(query))
    #(maxNonRel, secMaxNonRel) = findWeights(tfNonRel, idfNonRel)

    print maxRel,secMaxRel

    #original query modified
    return query + maxRel + secMaxRel

def findWeights(tfDict, idfDict, query):
    weight = {}
    first = ''
    second = ''
    weight[first] = 0
    weight[second] = 0

    for word in tfDict:
        idf = idfDict[word]
        tfTotal = 0
        for doc in tfDict[word]:
            tfTotal = tfTotal + tfDict[word][doc]
        weight[word] = tfTotal * idf

        if weight[word]>weight[first] and word not in query:
            first = word
        if weight[word]<weight[first] and weight[word]>weight[second] and word not in query:
            second = word
            
    return (first,second)


def findIDF(tf,N):
    idf = {}
    for word in tf:
        df = len(tf[word])
        idf[word] = math.log10(float(N)/float(df))+1
    return idf
    


def findTF(docs):
    tf = {}
    num = 1
    #x = nltk.porter.PorterStemmer()
    
    for doc in docs:
        vocab = doc['Description']+' '+doc['Title']

        #Converting to lowercase
        vocab = vocab.lower()

        #Removing punctuation
        vocab = vocab.translate(string.maketrans("",""), string.punctuation)

        #Tokenize into word list
        vocabList = nltk.word_tokenize(vocab)

        #Remove stop words
        vocabList= [w for w in vocabList if not w in stopwords]
        
        for word in vocabList:

            #Adding to dictionary
            if word in tf:
                if num in tf[word]:
                    tf[word][num] = tf[word][num] + 1
                else:
                    tf[word][num] = 1
            else:
                tf[word] = {}
                tf[word][num] = 1
                
        num = num + 1 

    return tf
    
    
