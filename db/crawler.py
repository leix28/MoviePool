# encoding: utf8
import requests
import logging
import sys
import json
import traceback
from bs4 import BeautifulSoup
import re

URL = 'https://api.douban.com'
BYR_SEARCH_URL = 'http://bt.byr.cn/torrents.php'
BYR_COOKIE = {'Cookie': 'Hm_lvt_9ea605df687f067779bde17347db8645=1463235397,1463305118,1463663039,1463885401; Hm_lpvt_9ea605df687f067779bde17347db8645=1464697392; c_secure_uid=MTgyNzAz; c_secure_pass=e27cebdda92981ed700ee16cab8efa99; c_secure_ssl=bm9wZQ%3D%3D; c_secure_tracker_ssl=bm9wZQ%3D%3D; c_secure_login=bm9wZQ%3D%3D'}

def searchByrResources(imdbId):
    try:
        arg = {'search': imdbId, 'search_area': 4}
        r = requests.get(BYR_SEARCH_URL, params=arg, headers=BYR_COOKIE)
        assert r.status_code == 200

        result = []
        soup = BeautifulSoup(r.text, "html.parser")
        for row in soup.select('table.torrents tr'):
            cols = row.find_all('td', class_='rowfollow')
            if not len(cols) or len(cols)<9:
                continue
            name = cols[1].select('a b')[0].contents[0]
            size = ''.join(filter(lambda s:isinstance(s, unicode), cols[4].contents))
            up = (cols[5].find_all('font') or cols[5].find_all('a') or cols[5].find_all('span'))[0].contents[0]
            down = (cols[6].find_all('a') or [cols[6]])[0].contents[0]
            result.append({
                'name': name,
                'size': size,
                'uploading': up,
                'downloading': down
            })

        return result
    except Exception, e:
        logging.warning('searchByrResources {} {}'.format(imdbId, e))
        traceback.print_exc()
    return []

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

def getMoviePopDouban(count=8):
    try:
        r = requests.get(URL + '/v2/movie/in_theaters')
        assert r.status_code == 200
    except:
        logging.warning('getMoviePopDouban Failed')
        return None
    return json.loads(r.text)['subjects'][:count]

def fetchDouban(doubanID):
    try:
        r = requests.get(URL + '/v2/movie/subject/' + doubanID)
        assert r.status_code == 200
        data = json.loads(r.text)
        try:
            r = requests.get('https://movie.douban.com/subject/' + doubanID)
            assert r.status_code == 200
            soup = BeautifulSoup(r.text, 'lxml')
            imdb = soup.find(id='info').find('a', text=re.compile("tt\\d*")).text
            data.update({'IMDB': imdb})
        except:
            logging.warning("ERROR in load IMDB ID")
    except:
        logging.warning(doubanID + 'fetchdata failed')
        return None
    return data

def fetchIMDB(IMDBID):
    try:
        r = requests.get('http://www.imdb.com/title/' + IMDBID)
        assert r.status_code == 200
        soup = BeautifulSoup(r.text, 'lxml')
        imdbScore = soup.find(class_='ratingValue').text
        data = {'score' : imdbScore.split('/')[0] }
    except:
        logging.warning("ERROR in IMDB Score")
    return data

if __name__ == '__main__':
    print searchMovieDoubanID(u"速度与激情")
