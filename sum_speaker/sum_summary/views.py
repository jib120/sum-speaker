#sum_summary/views.py

from django.shortcuts import render
from sum_summary.naver_collections import show_top_issue
from django.shortcuts import redirect

from django.http import HttpResponse

from sum_summary.models import Candidate,Member,Keyword

import urllib
import time

# for unescape
import html

#from django.core.exceptions import ObjectDoesNotExist

from .rss_parse import gather_rss

def index(request):
    top10 = show_top_issue()
    context = {'top10' : top10}
    return render(request, 'sum_summary/index.html', context)


def cleardb(request):
    Keyword.objects.all().delete()
    return redirect('/')



def unescape(s):
    #return html.unescape(s)
    s_utf8 = bytes(s, 'utf-8')
    return ''.join(["\\u%04x" % (ord(c)) for c in s_utf8])


def search(request):

    KEYWORD_MAX_COUNT = 10

    current_keyword = request.GET.get('keyword')
    print(current_keyword)

    # Check caching data in database about keyword
    keywords = Keyword.objects.filter(keyword=current_keyword).order_by('reg_date')[:20]

    if len(keywords) > 0:
        print("already exist! Use cached item in db")
    else:
        #print(urllib.parse.unquote(current_keyword))

        for summary, link, title, author in gather_rss(current_keyword, KEYWORD_MAX_COUNT):
            obj, created = Keyword.objects.get_or_create(
                # unique key temporary
                id = int(time.time() * 100000),
                keyword = current_keyword,
                link = link,
                title = title,
                author = author,
                summary = summary
            )
            obj.save()
            #print(summary)

        # TODO : paging도...
        keywords = Keyword.objects.filter(keyword=current_keyword).order_by('reg_date')

    context = {
        'Keywords' : keywords,
        'current_keyword' : current_keyword,
        'Keywords_max' : len(keywords)
    }

    return render(request, 'sum_summary/view.html', context)
  
