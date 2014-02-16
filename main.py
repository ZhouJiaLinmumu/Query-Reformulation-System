# -*- coding: utf-8 -*-
import urllib
import urllib2
import base64
import json
import sys
from engine import keyWordEngine

def main():
    while True:
        query = raw_input('Please enter the query you want to search for : ')
        if len(query)!=0:
            break
        else:
            print 'Please enter a valid query'

    while True:
        try:
            targetPrec = float(raw_input('Please enter the precision(@10) you want to search with (0-1) : '))
            if targetPrec<0.0 or targetPrec>1.0:
                print 'Please enter a valid precision value'
            else:
                break
        except ValueError:
            print 'Please enter a valid precision value'
    
    bing_search(query, targetPrec)

def bing_search(query,targetPrec):
    query = query.replace(" ",'+')
    print 'Updated query - ' + query
    print '==============================================================='
    bingUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27' + query + '%27&$top=10&$format=json'
    print bingUrl
    #Provide your account key here
    accountKey = 'JsV9AIVwzY0l654YiaIXAppMcpvpm7lvkcYdmzJrNcs'

    accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
    headers = {'Authorization': 'Basic ' + accountKeyEnc}
    req = urllib2.Request(bingUrl, headers = headers)
    response = urllib2.urlopen(req)
    content = response.read()
    #print content
    #content contains the json response from Bing. 
    json_result = json.loads(content)
    result_list = json_result['d']['results']
    print getRelevantFB(query, result_list,targetPrec)

def getRelevantFB(query, result_list, targetPrec):
    userPrec = 0.0;
    relevant = []
    nonrel = []
    if len(result_list)<10:
        print 'There are less than 10 results to this query. So exiting.'
        sys.exit()
        
    for result in result_list:
        desc = result[u'Description'].encode("iso-8859-15", "replace")
        title = result[u'Title'].encode("iso-8859-15", "replace")
        url = result[u'Url'].encode("iso-8859-15", "replace")
        print '\nTitle: ' + title + '\n' + 'Url: ' + url + '\n' + 'Desc: ' + desc
        entry = {}
        entry['Title'] = title
        entry['Description'] = desc
        entry['Url'] = url            
        
        while True:
            isRel = raw_input('Is this link relevant to your search or not (y or n)?: ')
            if isRel == 'y' or isRel == 'Y':
                userPrec = userPrec+1
                relevant.append(entry)
                break;
            elif isRel == 'n' or isRel == 'N':
                nonrel.append(entry)
                break;
            else :
                print 'Please provide a feedback(y or n)'

            
    userPrec = userPrec/10
    print 'Precision from user relevance feedback - ' +str(userPrec)
    print 'Target Precision - ' + str(targetPrec)
    # If targetPrecision is achieved
    if userPrec == 0:
        print "Quitting as the relevance feedback score is zero."
        sys.exit()
    elif userPrec >= targetPrec:
        print "Target precision achieved."
        sys.exit()
    else:
        query = keyWordEngine(query,targetPrec,relevant,nonrel)
        bing_search(query,targetPrec)



if __name__ == "__main__":
    main()
