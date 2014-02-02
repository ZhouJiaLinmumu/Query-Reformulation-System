# -*- coding: utf-8 -*-
import urllib
import urllib2
import json

def main():
    query = "gates"
    query = raw_input('Please enter the query you want to search for : ')
    preck = raw_input('Please enter the precision you want to search with (0-1) : ')
    bing_search(query)

def bing_search(query):
    key= 'JsV9AIVwzY0l654YiaIXAppMcpvpm7lvkcYdmzJrNcs'
    query = urllib.quote(query)
    # create credential for authentication
    user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1;Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'
    credentials = (':%s' % key).encode('base64')[:-1]
    auth = 'Basic %s' % credentials
    url = 'https://api.datamarket.azure.com/Bing/SearchWeb/v1/Web?Query=%27'+query+'%27&$top=10&$format=json'
    request = urllib2.Request(url)
    request.add_header('Authorization', auth)
    request.add_header('User-Agent', user_agent)
    request_opener = urllib2.build_opener()
    response = request_opener.open(request)
    response_data = response.read()
    json_result = json.loads(response_data)
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
