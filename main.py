# -*- coding: utf-8 -*-
import urllib
import urllib2
import base64
import json

def main():
    query = "gates"
    query = raw_input('Please enter the query you want to search for : ')
    preck = raw_input('Please enter the precision you want to search with (0-1) : ')
    bing_search(query)

def bing_search(query):
    bingUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27gates%27&$top=10&$format=json'
    #Provide your account key here
    accountKey = 'JsV9AIVwzY0l654YiaIXAppMcpvpm7lvkcYdmzJrNcs'

    accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
    headers = {'Authorization': 'Basic ' + accountKeyEnc}
    req = urllib2.Request(bingUrl, headers = headers)
    response = urllib2.urlopen(req)
    content = response.read()
    print content
    #content contains the xml/json response from Bing. 
    json_result = json.loads(content)
    result_list = json_result['d']['results']
    print getRelJudmnt(result_list)
    return result_list

def getRelJudmnt(result_list):
    count = 0;
    for result in result_list:
      desc = result[u'Description'].encode("iso-8859-15", "replace")
      title = result[u'Title'].encode("iso-8859-15", "replace")
      url = result[u'Url'].encode("iso-8859-15", "replace")
      print '\nTitle: ' + title + '\n' + 'Url: ' + url + '\n' + 'Desc: ' + desc
      isRel = raw_input('Is this link relevant to your search or not (y or n)?: ')
      if isRel == 'y':
          count = count+1
          
    return count


if __name__ == "__main__":
    main()
