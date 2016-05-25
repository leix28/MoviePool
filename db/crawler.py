# encoding: utf8
import requests
import logging
import sys
import json
from bs4 import BeautifulSoup


URL = 'https://api.douban.com'


def searchMovieDouban(query, start=0, count=5):
    '''
    This function returns json[subjects].
    visit https://api.douban.com/v2/movie/search?q=%7B%E9%80%9F%E5%BA%A6%E4%B8%8E%E6%BF%80%E6%83%85%7D for an example.
    '''
    data = {'q' : '{' + query + '}',
            'start' : start,
            'count' : count
            }
    try:
        r = requests.get(URL + '/v2/movie/search', params=data)
        assert r.status_code == 200
    except:
        logging.warning(query + 'Search Failed')
        return None

    return json.loads(r.text)['subjects']

def fetchDouban(doubanID):
    try:
        r = requests.get('https://movie.douban.com/subject/' + doubanID)
        assert r.status_code == 200
        soup = BeautifulSoup(r.text, 'lxml')
        info = str(soup.find(id='info'))
        r = requests.get(URL + '/v2/movie/subject/' + doubanID)
        assert r.status_code == 200
        data = json.loads(r.text)
        data.update({'filmInfo': info})
    except:
        logging.warning(doubanID + 'fetchdata failed')
        return None
    return data

def fetchIMDB(IMDBID):
    pass

if __name__ == '__main__':
    print searchMovieDoubanID(u"速度与激情")
