import string
import math
stopwords = ['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am', 'among', 'an', 'and', 'any', 'are', 'as',
             'at', 'be', 'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear', 'did', 'do', 'does', 'either', 'else',
             'ever', 'every', 'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however',
             'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may', 'me', 'might', 'most', 'must', 'my',
             'neither', 'no', 'nor', 'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather', 'said', 'say', 'says', 'she',
             'should', 'since', 'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'this', 'tis', 'to', 'too',
             'twas', 'us', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet',
             'you', 'your']


def keyWordEngine(query,targetPrec,relevant,nonrel):
    query = query.replace('+',' ')

    # finding N for calculating IDF
    N_Rel = len(relevant)
    N_Nonrel = len(nonrel)

    #finding TF
    tfRel,titleRel = findTF(relevant)
    print 'Rel title list'
    print titleRel
    
    tfNonRel,titleNonRel = findTF(nonrel)
    
    tfQuery = findQueryTF(query)
    print 'Non Rel title list'
    print titleNonRel
    
    #finding IDF
    idfRel = findIDF(tfRel, N_Rel)
    idfNonRel = findIDF(tfNonRel, N_Nonrel)
    
    #finding Relevant weights
    weightsRel = {}
    weightsRel = findWeights(tfRel, idfRel, titleRel, N_Rel)

    print "weights relevant"
    print weightsRel
    
    #finding Nonrelevant weights
    weightsNonRel = {}
    weightsNonRel = findWeights(tfNonRel, idfNonRel, titleNonRel, N_Nonrel)

    print "weights non relevant "
    print weightsNonRel

    #implementing Rochio to find the new query
    (first,second) = findWords(weightsRel, weightsNonRel, tfQuery)

    
    print 'New words added to query are - ' + first + ' ' + second
    #original query modified
    return query + ' '+ first + ' '+ second


def findWords(RelDoc, NonrelDoc, query):
    alpha = 1
    beta = 0.75
    gamma = -0.15

    finalWeight = {}
    first = ''
    second = ''
    finalWeight[first]=0
    finalWeight[second]=0
    print "Query is "
    print query
    for word in RelDoc:
        finalWeight[word] = beta * RelDoc[word]
    for word in query:
        if word in finalWeight:
            finalWeight[word] = finalWeight[word] + alpha * query[word]
        else:
            finalWeight[word] = alpha * query[word]
                        
    for word in NonrelDoc:
        if word in finalWeight:
            finalWeight[word] = finalWeight[word] + gamma * NonrelDoc[word]
        else:
            finalWeight[word] = gamma * NonrelDoc[word]

    for word in finalWeight:    
        if finalWeight[word] > finalWeight[first] and word not in query:
            first = word
        elif finalWeight[word]<=finalWeight[first] and finalWeight[word] >= finalWeight[second] and word not in query:
            second = word


    print "final weights"
    import operator
    sorted_x = sorted(finalWeight.iteritems(), key=operator.itemgetter(1))
    print sorted_x
    return first,second
    


    
def findWeights(tfDict, idfDict, titleDict, N):
    weight = {}
    for word in tfDict:
        idf = idfDict[word]
        tfTotal = 0
        for doc in tfDict[word]:
            tfTotal = tfTotal + tfDict[word][doc]
        weight[word] = tfTotal * idf
        if word in titleDict: # give more weightage to title words
            weight[word] = weight[word]*(1 + (float(titleDict[word])/float(N))*0.2)
        
    return weight


def findIDF(tf,N):
    idf = {}
    for word in tf:
        df = len(tf[word]) # document freq is can be the size of posting list for that term
        idf[word] = math.log10(float(N)/float(df))+1
    return idf
    
def findQueryTF(query):
    tf = {}
    vocab = query
    #Converting to lowercase
    vocab = vocab.lower()
    #Removing punctuation
    vocab = vocab.translate(string.maketrans("",""), string.punctuation)
    #Tokenize into word list
    vocabList = vocab.split()
    for word in vocabList:
      #Adding to dictionary
        if word in tf:
            tf[word] = tf[word] + 1
        else:
            tf[word] = 1
    return tf

def findTF(docs):
    tf = {}
    docId = 1
    titleDocTF = {}
    #x = nltk.porter.PorterStemmer()
    
    for doc in docs:
        vocab = doc['Description']+' '+doc['Title']
        title = doc['Title']
        #Converting to lowercase
        title = title.lower()
        #Removing punctuation
        title = title.translate(string.maketrans("",""), string.punctuation)
        titleList = title.split()
        repeat ={}
        for word in titleList:
            if word in titleDocTF and word not in repeat:
                titleDocTF[word] = titleDocTF[word] + 1
                repeat[word] = 1
                
            elif word not in repeat:
                titleDocTF[word] = 1
                repeat[word] = 1
        
        #### Try to figure out how we can give more weightage to title
        #### Also may be give wikiperdia url more weightage

        #Converting to lowercase
        vocab = vocab.lower()

        #Removing punctuation
        vocab = vocab.translate(string.maketrans("",""), string.punctuation)

        #Tokenize into word list
        vocabList = vocab.split()

        #Remove stop words
        vocabList= [w for w in vocabList if not w in stopwords]
        
        for word in vocabList:
           #Adding to dictionary
            if word in tf:
                if docId in tf[word]:
                    tf[word][docId] = tf[word][docId] + 1
                else:
                    tf[word][docId] = 1
            else:
                tf[word] = {}
                tf[word][docId] = 1


        docId = docId + 1 

    return tf, titleDocTF
    
    
