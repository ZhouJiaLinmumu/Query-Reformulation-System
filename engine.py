import string
import math
import re
import itertools
import heapq

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
    tfNonRel,titleNonRel = findTF(nonrel)
    tfQuery = findQueryTF(query)

    #finding IDF
    idfRel = findIDF(tfRel, N_Rel)
    idfNonRel = findIDF(tfNonRel, N_Nonrel)
    
    #finding Relevant weights
    weightsRel = {}
    weightsRel = findWeights(tfRel, idfRel, titleRel, N_Rel)

    #finding Nonrelevant weights
    weightsNonRel = {}
    weightsNonRel = findWeights(tfNonRel, idfNonRel, titleNonRel, N_Nonrel)

    #implemented Rochio to find the new query
    (first,second) = findWords(weightsRel, weightsNonRel, tfQuery)

    # if no new words to be added
    if first =='' and second =='':
        return ''

    finalList = []
    
    print 'New words added to query are - ' + first + ' ' + second
    print 'Determining the best order of query terms'
    #original query modified
    query = query.split()
    if second=="":
        finalList.extend(query)
        finalList.append(first)
    else:
        finalList.extend(query)
        finalList.append(first)
        finalList.append(second)

    #find the best order of the words in the query        
    finalOrderedList = findPermutations(finalList, relevant)

    modifiedQuery = []
    for wordList in finalOrderedList:
        for word in wordList:
            if word not in modifiedQuery:
                modifiedQuery.append(word)
            
    #clusters are appended
    return " ".join(modifiedQuery)


def searchResults(phrase, docs):
    weight = 0
    for doc in docs:
        content = doc['Title'] + ' ' + doc['Description']
        #Converting to lowercase
        content = content.lower()
        #Removing punctuation
        content = content.translate(string.maketrans("",""), string.punctuation)
        matches = re.findall(re.escape(phrase[0])+'\s'+re.escape(phrase[1]), content)
        weight = weight + len(matches)
    return weight


def findPermutations(queryList,docRel):
    pairWeight = {}
    bestQueryList = []
    useless = set()
    # find all the permutations of the query terms in pairs
    for pair in itertools.permutations(queryList, 2):
        # find the number of times the permutation occurs in relevants docs 
        pairWeight[pair] = searchResults(pair,docRel)
    sortedPairs = sorted(pairWeight.items(), key=lambda x:x[1], reverse = True)
    print sortedPairs
    # combine the pairs in order of decreasing weights.
    N = len(queryList)
    added = 0
    for pair in sortedPairs:
        print '=== Pair '
        print pair
        bestQueryList,added,useless = addPair(0, bestQueryList, pair[0],pair[1], added, useless)
        if added == N: # break if all query terms are added
            break

    bestQueryList.append(useless)        
    print "Best order found is - "
    print bestQueryList
    return bestQueryList

def addPair(index ,QueryList, pair, weight, added, useless):
    print '==== Querylist === '
    print QueryList
    print '==== end QueryList === '
    if len(QueryList)<=index:
        print '=== main if' + ' '+ pair[0] + ' ' + pair[1]
        QueryList.append([])
        QueryList[index].append(pair[0])
        QueryList[index].append(pair[1])
        print '=== main if end'
        added = added + 2
    else:
        n = len(QueryList[index])
        if (not isNewWord(pair[0], QueryList)) and (not isNewWord(pair[1], QueryList)):
            print '===== in 1st'
            return QueryList,added,useless
        if pair[0]==QueryList[index][n-1]:
            if(weight==0):
                useless.add(pair[1])
            else:
                QueryList[index].append(pair[1])
            added = added + 1
            print '===== in 2nd'
        elif pair[1]==QueryList[index][0]:
            if(weight==0):
                useless.add(pair[0])
            else:
                QueryList[index].insert(0,pair[0])
            added = added + 1
            print '===== in 3rd'
        elif pair[0]==QueryList[index][0] and isNewWord(pair[1], QueryList):
            if(weight==0):
                useless.add(pair[1])
            else:
                QueryList[index].append(pair[1])
            added = added + 1
            print '===== in 3.5rd'
        elif isNewWord(pair[0], QueryList) and isNewWord(pair[1],QueryList):
            print '===== in 4th'
            if(weight==0):
                useless.add(pair[0])
                useless.add(pair[1])
            else:
                QueryList,added,useless = addPair(index+1, QueryList,pair, weight, added, useless)
        else:
            print '==== in 5th'                
            if isNewWord(pair[0],QueryList):
                print '==== in 6th'
                useless.add(pair[0])
            elif isNewWord(pair[1],QueryList):
                print '==== in 7th'
                useless.add(pair[1])
            #else if only one word of the pair is in the middle of the query then ignore that pair and leave the other word </3
            #else if first word in pair equals first word inquerylist, or vice versa, ignore

    print '==== Return Querylist === '
    print QueryList
    print useless
    print '==== Return end QueryList === '
    return QueryList,added,useless

def isNewWord(word, QueryList):
    for wordlist in QueryList:
        if word in wordlist:
            return False
    return True

def findWords(RelDoc, NonrelDoc, query):
    alpha = 1
    beta = 0.75
    gamma = -0.15

    finalWeight = {}
    first = ''
    second = ''
    finalWeight[first]=0
    finalWeight[second]=0

    #finding the final weights based on Rochio algorithm
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

    # find top 10 words(excluding query terms) from the finalweights using a heap, runs faster than sorting the whole list
    #sortWeights = sorted(finalWeight.items(), key=lambda x:x[1], reverse = True)
    sortWeights = heapq.nlargest(10 + len(query),finalWeight,key=finalWeight.get);
    print sortWeights

    #Finding top two words by weigths such that the word is not in query
    i = 0
    while i < len(sortWeights):
        if sortWeights[i] not in query:
            first = sortWeights[i]
            break
        else:
            i = i+1

    i = i+1
    while i < len(sortWeights):
        if sortWeights[i] not in query:
            second = sortWeights[i]
            break
        else:
            i = i+1
    
    # If top two words have similar weights then take both
    # NOTE - in case first and second are empty then we will return in this check
    if checkSimilarWeights(finalWeight[first],finalWeight[second]):
        return first,second

    # Choosing whether to add one or two new words to the query
    # Taking the avg of top 10 weigths. Take the avg of first term and this avg.
    # Lets call it threshold. if the second term weight is greater than this threshold then take it as well.
    count = 0
    total = 0
    for word in sortWeights:
        if finalWeight[word] < 0:
            break
        count = count + 1
        total = total + finalWeight[word]
    avg = float(total) / float(count)
    threshold = (avg + finalWeight[first])/2.0;

    if finalWeight[second] >= threshold:
        return first, second
    else:
        return first, ""

    
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
    replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
    #x = nltk.porter.PorterStemmer()
    wikiFactor = 1
    for doc in docs:
        url = doc['Url']
        if re.match(r'.*wikipedia\.org.*', url):
            wikiFactor = 1.2
            print "wiki factor changed"
        else:
            wikiFactor = 1
        vocab = doc['Description']+' '+doc['Title']
        title = doc['Title']
        #Converting to lowercase
        title = title.lower()
        #Removing punctuation
        title = title.translate(replace_punctuation)

        
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
        #### Also may be give wikipedia url more weightage

        #Converting to lowercase
        vocab = vocab.lower()

        #Removing punctuation
        vocab = vocab.translate(replace_punctuation)

        #Tokenize into word list
        vocabList = vocab.split()

        #Remove stop words
        vocabList= [w for w in vocabList if not w in stopwords]


        
        for word in vocabList:
           #Adding to dictionary
            if word in tf:
                if docId in tf[word]:
                    tf[word][docId] = tf[word][docId] + 1 * wikiFactor
                else:
                    tf[word][docId] = 1
            else:
                tf[word] = {}
                tf[word][docId] = 1


        docId = docId + 1 

    return tf, titleDocTF
    
def checkSimilarWeights(first, second):
    # check if second and first are close values
    # close is defined by 5% tolerance
    if (first - 0.05*first) <= second:
        return True
    else:
        return False
        
