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

from textrankr import TextRank

import asyncio

# workaround preloading kkma in konlpy
# kkma 형태소 분석기 로딩이 엄청 오래 걸림... ( 10초? )
#########################################
if jpype.isJVMStarted():
    jpype.attachThreadToJVM()

_textrank = TextRank("test")
#########################################

# reference code(related newspaper lib) : http://newspaper.readthedocs.io/en/latest/

def print_with_timestamp(t):
    print("[{}] {}".format(time.time(), t))

def summarize_text(text):
    # < workaround cooes > for crash problem with django and konlpy
    # - related issue : https://github.com/konlpy/konlpy/issues/104
    if jpype.isJVMStarted():
        jpype.attachThreadToJVM()
    # < workaround codes end!!! >

    _textrank = TextRank(text)
    return _textrank.summarize()

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
            article = newspaper.Article(e['link'])

            article.download()
            # wait for a moment
            # sleep(0.1)
            article.parse()

            text = article.text

            # text count check : threshold 200? 400?
            if len(text) < ARTICLE_SIZE_THRESHOLD:
                max_count += 1
                continue

            # remove absent lines
            text = text.replace('\n\n', '\n')
            # text = re.sub("(\[.*기자\])", '', text)

            text_summary = summarize_text(text)

            # 제목에서 [포토], [사진] 등의 문구 제거
            title = re.sub("\[.*\]", '', e['title'])

            yield text_summary, e['link'], title, e['author']
        except:
            continue

        #print(len(text))
        #print(text_summary)

def get_article(e):
    # boundary values
    ARTICLE_SIZE_THRESHOLD = 50

    try:
        article = newspaper.Article(e['link'])
        #loop = asyncio.get_event_loop()
        #await loop.run_in_executor(article, download)
        article.download()
        # wait for a moment
        # sleep(0.1)
        #await loop.run_in_executor(article, parse)
        article.parse()
        text = article.text

        # text count check : threshold 200? 400?
        if len(text) < ARTICLE_SIZE_THRESHOLD:
            return ()

        # remove absent lines
        text = text.replace('\n\n', '\n')
        # text = re.sub("(\[.*기자\])", '', text)

        text_summary = summarize_text(text)
        # 제목에서 [포토], [사진] 등의 문구 제거
        title = re.sub("\[.*\]", '', e['title'])

        #yield text_summary, e['link'], title, e['author']
        return text_summary, e['link'], title, e['author']

    except:
        return ()

def gather_rss_async(keyword, max_count=20):
    url = "http://newssearch.naver.com/search.naver?where=rss&query=" \
          + urllib.request.quote(keyword)

    print_with_timestamp("start rss gather !")
    data = feedparser.parse(url)
    print("url={}, data len={}".format(url, len(data.entries)))

    keywords_list = []
    futures = []

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def coroutines():
        futures = [
            loop.run_in_executor(
                None,
                get_article,
                e
            )
            for e in data.entries[:10]
        ]
        for res in await asyncio.gather(*futures):
            if res:
                keywords_list.append(res)

    loop.run_until_complete(coroutines())

    print_with_timestamp("end rss gather - {}!".format(max_count))
    return keywords_list

if __name__ == "__main__":
    for t in gather_rss(sys.argv[1]):
        print(t)



