import feedparser
import urllib
import newspaper

import time
import sys
import re
# from time import sleep
import jpype

# for textrankr : https://github.com/theeluwin/textrankr

# install - pip install textrankr
# encoding error on installing in windows
# - chcp 65001 -> after again -> pip install textrankr

import os

sys.path.append('./sum_summary/textrankr')
sys.path.append('./sum_summary/lexrankr')

### for test using main
sys.path.append('./textrankr')
sys.path.append('./lexrankr')

from textrankr import TextRank
from lexrankr import LexRank

import asyncio
from contextlib import suppress


#from html2text import html2text

# workaround preloading kkma in konlpy
# kkma 형태소 분석기 로딩이 엄청 오래 걸림... ( 10초? )

#########################################
if jpype.isJVMStarted():
    jpype.attachThreadToJVM()

_textrank = TextRank("test")
#########################################

def summarize_text(text):
    # < workaround cooes > for crash problem with django and konlpy
    # - related issue : https://github.com/konlpy/konlpy/issues/104
    if jpype.isJVMStarted():
        jpype.attachThreadToJVM()
    # < workaround codes end!!! >

    #print_with_timestamp("textrank init")
    _textrank = TextRank(text)
    #print_with_timestamp("textrank init end")
    return _textrank.summarize()


def summarize_text_with_lexrank(text):
    lexrank = LexRank(n_clusters=1)
    lexrank.summarize(text)
    summaries = lexrank.probe(3)

    if len(summaries)  == 0:
        return ""

    return ". ".join(summaries)
# reference code(related newspaper lib) : http://newspaper.readthedocs.io/en/latest/

def print_with_timestamp(t):
    print("[{}] {}".format(time.time(), t))


def gather_rss(keyword, max_count=20):
    url = "http://newssearch.naver.com/search.naver?where=rss&query=" \
          + urllib.request.quote(keyword)

    # boundary values
    ARTICLE_SIZE_THRESHOLD = 50

    print_with_timestamp("start rss gather !")
    data = feedparser.parse(url)
    print("url={}, data len={}".format(url, len(data.entries)))

    for i, e in enumerate(data.entries):
        # print(e['link'])

        if i >= max_count:
            break

        print("link = {}".format(e['link']))

        try:
            res = get_article(e)

            # text count check : threshold 200? 400?
            if not res:
                max_count += 1
                continue

            yield res
        except:
            continue

        #print(len(text))
        #print(text_summary)
    print_with_timestamp("end rss gather !")

def get_article(e, use_lexrank=False):
    # boundary values
    ARTICLE_SIZE_THRESHOLD = 50

    try:
        ##########################
        # by newspaer lib ########
        article = newspaper.Article(e['link'])
        #loop = asyncio.get_event_loop()
        #await loop.run_in_executor(article, download)
        article.download()
        # wait for a moment
        # sleep(0.1)
        #await loop.run_in_executor(article, parse)
        article.parse()
        text = article.text
        ##########################
        '''
        url = e['link']
        link = urllib.request.urlopen(url)
        dat = link.read()
        dat = dat.decode('utf-8', 'backslashreplace')
        text = html2text(dat, url)

        #print("dat={}, text= {}".format(dat, text))
        '''
        ##########################

        # text count check : threshold 200? 400?
        if len(text) < ARTICLE_SIZE_THRESHOLD:
            return ()

        # remove absent lines
        text = text.replace('\n\n', '\n')
        # text = re.sub("(\[.*기자\])", '', text)

        if(use_lexrank):
            text_summary = summarize_text_with_lexrank(text)
        else:
            text_summary = summarize_text(text)
        # 제목에서 [포토], [사진] 등의 문구 제거
        title = re.sub("\[.*\]", '', e['title'])

        #yield text_summary, e['link'], title, e['author']
        return text_summary, e['link'], title, e['author']

    except Exception as ex:
        print('exception occured {}'.format(ex))
        return ()

def gather_rss_async(keyword, max_count=20):
    url = "http://newssearch.naver.com/search.naver?where=rss&query=" \
          + urllib.request.quote(keyword)

    print_with_timestamp("start rss gather !")
    start_time = time.time()

    data = feedparser.parse(url)
    print("url={}, data len={}".format(url, len(data.entries)))

    keywords_list = []

    loop = asyncio.new_event_loop()

    async def coroutines():
        futures = [
            loop.run_in_executor(
                None,
                get_article,
                e
            )
            for e in data.entries[:max_count]
        ]
        
        for res in await asyncio.gather(*futures):
            if res:
                keywords_list.append(res)
    try:
        #loop.run_until_complete(asyncio.wait(unfinished))
        loop.run_until_complete(coroutines())
        loop.close()
    except Exception as ex:
        print('exception occured {}'.format(ex))

    print_with_timestamp("end rss gather - {} : {} elapsed!".format(max_count, time.time()-start_time))
    return keywords_list[:max_count]

'''
futures = [
    loop.run_in_executor(
        None,
        get_article,
        e
    )
    for e in data.entries[:max_count + 20]
]

unfinished = futures
for i in range(max_count):
    finished, unfinished = loop.run_until_complete(
        asyncio.wait(unfinished, return_when=asyncio.FIRST_COMPLETED))
    for res in finished:
        if res.result():
            keywords_list.append(res.result())

for task in unfinished:
    task.cancel()
    with suppress(asyncio.CancelledError):
        loop.run_until_complete(task)

#loop.run_until_complete(coroutines())
'''


if __name__ == "__main__":
    print_with_timestamp("start!")
    start_time = time.time()

    for t in gather_rss_async(sys.argv[1], 10):
        print(t)

    print_with_timestamp("end![{} elapsed!]".format(time.time()-start_time))


