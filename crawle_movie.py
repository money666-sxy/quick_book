import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time
from multiprocessing.dummy import Pool

import search_book
import create_picture


def creat_url(sid):
    '''
    input book_sid 
    ouput list of book_urls
    '''
    urls = []
    for page in range(1, 10):
        # url = 'https://book.douban.com/subject/' + \
        #     str(sid) + '/comments/hot?p=' + str(page) + ''
        url = 'https://book.douban.com/subject/' + \
            str(sid) + '/comments/?start='+str(20*page) + \
            '&limit=20&status=P&sort=new_score'
        urls.append(url)
    # print(urls)/
    return urls


def get_html(urls):
    headers = {
        # 'Cookie': 你的cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
        'Connection': 'keep-alive'
    }
    # for url in urls:
    #     print('正在爬取：'+url)
    #     req = urllib.request.Request(url=url, headers=headers)
    #     req = urllib.request.urlopen(req)
    #     content = req.read().decode('utf-8')
    #     # time.sleep(10)
    print('正在爬取：'+urls)
    req = urllib.request.Request(url=urls, headers=headers)
    req = urllib.request.urlopen(req)
    content = req.read().decode('utf-8')
    return content


def parse(html_list):
    soupComment = BeautifulSoup(html_list, 'html.parser')
    comments = soupComment.findAll('span', 'short')
    onePageComments = []
    for comment in comments:
        # print(comment.getText()+'\n')
        onePageComments.append(comment.getText()+'\n')
    # print(onePageComments)
    return onePageComments


def get_comment(movie_name):
    '''
    crawle book comment 
    write in file 
    '''
    search_movie_url = 'https://www.douban.com/search?cat=1002&q=' + movie_name
    raw_str = search_book.get_content(search_movie_url)
    sid = search_book.find_sid(raw_str)
    print(sid)

    book_urls = creat_url(sid)
    pool = Pool(20)
    html_list = pool.map(get_html, book_urls)
    onePageComments = pool.map(parse, html_list)

    f = open('./comment/{0}.txt'.format(movie_name), 'a', encoding='utf-8')
    for sentence in onePageComments:
        f.write(str(sentence))
    f.close()

    create_picture.wordAnalysis(movie_name)


if __name__ == "__main__":
    start = time.time()
    movie_name = input('请输入需要提取评论的电影：')
    # search_movie_url = 'https://www.douban.com/search?cat=1002&q=' + movie_name
    # raw_str = search_book.get_content(search_movie_url)
    # sid = search_book.find_sid(raw_str)
    # print(sid)
    # get_comment(movie_name)
    # urls = creat_url(sid)
    get_comment(movie_name)

    print('爬取、存储、解析所有内容一共需要:{0}秒'.format(time.time()-start))
    # raw_str = crawler_tools.get_content('看见', '读书')
    # sid = crawler_tools.find_sid(raw_str)
    # print('sid:'+sid)
    # get_comment(sid)
