import ssl
import string
import urllib
import urllib.request
import urllib.parse
import time
from bs4 import BeautifulSoup


def create_url(keyword: str) -> str:
    '''
    Create url through keywords
    Args:
        keyword: the keyword you want to search
        kind: a string indicating the kind of search result
            type: 读书; num: 1001
            type: 电影; num: 1002
            type: 音乐; num: 1003
    Returns: url
    '''
    url = 'https://www.douban.com/search?cat=1001&q=' + keyword
    return url


def get_html(url: str) -> str:
    '''send a request'''

    headers = {
        # 'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
        'Connection': 'keep-alive'
    }
    ssl._create_default_https_context = ssl._create_unverified_context  # ssl645，证书不受信

    s = urllib.parse.quote(url, safe=string.printable)  # safe表示可以忽略的部分
    req = urllib.request.Request(url=s, headers=headers)
    req = urllib.request.urlopen(req)
    content = req.read().decode('utf-8')
    return content


def get_content(search_url) -> str:
    # url = create_url(keyword=keyword)
    html = get_html(search_url)
    # print(html)
    soup_content = BeautifulSoup(html, 'html.parser')
    contents = soup_content.find_all('h3', limit=1)
    result = str(contents[0])
    return result


def find_sid(raw_str: str) -> str:
    '''
    find sid in raw_str
    Args:
        raw_str: a html info string contains sid
    Returns:
        sid
    '''
    assert type(raw_str) == str, \
        '''the type of raw_str must be str'''
    start_index = raw_str.find('sid:')
    end_index = raw_str.find('qcat')
    sid = raw_str[start_index + 5: end_index-2]
    # sid = raw_str[start_index + 5: start_index + 14]
    sid.strip(',')
    return sid


def search_sid(keywords: str):
    '''在豆瓣里查找书名相对的sid'''
    search_url = create_url(keywords)
    raw_str = get_content(search_url)
    sid = find_sid(raw_str)
    # print(sid)
    return sid


if __name__ == "__main__":
    start = time.time()
    sid = search_sid('红楼梦')
    print(sid)
    print('爬取、存储、解析所有内容一共需要:{0}秒'.format(time.time()-start))
