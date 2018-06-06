#sum_summary/views.py

from django.shortcuts import render
from sum_summary.naver_collections import show_top_issue
from django.shortcuts import redirect
from django.http import HttpResponse
from sum_summary.models import Keyword, Bookmark
from django.contrib.auth.decorators import login_required
import urllib
import time

# for unescape
import html

#from django.core.exceptions import ObjectDoesNotExist

from .rss_parse import gather_rss_async

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
    order_text_dic = ['첫', '두', '세', '네', '다섯', '여섯', '일곱', '여덟', '아홉', '열']
    KEYWORD_MAX_COUNT = 10

    current_keyword = request.GET.get('keyword')
    #print(current_keyword)

    # Check caching data in database about keyword
    keywords = Keyword.objects.filter(keyword=current_keyword).order_by('reg_date')[:20]
    tts_for_text = " 오늘 {}에 대한 기사들을 말씀드리겠습니다. \n ".format(current_keyword)

    if len(keywords) > 0:
        print("already exist! Use cached item in db")
    else:
        #print(urllib.parse.unquote(current_keyword))

        for summary, link, title, author in enumerate(gather_rss_async(current_keyword, KEYWORD_MAX_COUNT)):
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

    for i, keyword in enumerate(keywords):
        tts_for_text += "{} 번쨰 기사는 {} 입니다. \n ".format(order_text_dic[i], keyword.title)
        tts_for_text += "{} . \n ".format(keyword.summary)

    tts_for_text += "  이상입니다.  애청해 주셔서 감사합니다. \n "
    tts_for_text = tts_for_text.replace('\n', ' \\n')
    print(tts_for_text)
    context = {
        'Keywords' : keywords,
        'current_keyword' : current_keyword,
        'Keywords_len' : len(keywords),
        'tts_for_text' : tts_for_text
    }

    return render(request, 'sum_summary/view.html', context)
  

@login_required
def bookmark_list(request):
    # check user_id and connected with bookmark list
    username = request.GET.get('user')
    bookmarks = Bookmark.objects.filter(username=username, status='1').order_by('reg_date')

    context = { 'username'      : username,
                'bookmarks'     : bookmarks,
                'bookmark_len' : len(bookmarks)
               }

    return render(request, 'sum_summary/bookmark_list.html', context)

@login_required
def bookmark_register(request):
    print(request)
    current_keyword = request.POST['current_keyword']
    username = request.POST['username']
    keywords = Keyword.objects.filter(keyword=current_keyword).order_by('reg_date')

    keywords_id=""
    for idx, keyword in enumerate(keywords):
        if(idx == len(keywords)-1 ):
            keywords_id += str(keyword.id)
            break;
        else:
            keywords_id += str(keyword.id) + ","

    obj, created = Bookmark.objects.get_or_create(keyword=current_keyword, keywords_id=keywords_id, username=username, status="1")
    obj.save()

    context = {
        'Keywords'          : keywords,
        'current_keyword'  : current_keyword,
        'Keywords_len'     : len(keywords)
    }
    return render(request, 'sum_summary/view.html', context)

@login_required
def bookmark_view(request):
    bookmark_id = request.GET.get('id')
    bookmarks = Bookmark.objects.get(id=bookmark_id)
    bookmarks_keywords = bookmarks.keywords_id
    keyword_id = bookmarks_keywords.split(',')

    Keyword_info =[]
    for idx, id in enumerate(keyword_id):
        Keyword_info.append(Keyword.objects.get(id=id))

    context = {
        'Keywords'          : Keyword_info,
        'current_keyword'  : bookmarks.keyword,
        'Keywords_len'     : len(keyword_id)
    }
    return render(request, 'sum_summary/bookmark_view.html', context)

def get_keyword_info(keyword_id):
    return Keyword.objects.filter(id=keyword_id)

#@login_required
def bookmark_remove(request):
    bookmark_id = request.GET.get('id')
    username    = request.GET.get('user')

    Bookmark.objects.filter(id=bookmark_id).update(status='0')
    bookmarks = Bookmark.objects.filter(username=username, status='1').order_by('reg_date')

    context = { 'username'      : username,
                'bookmarks'     : bookmarks,
                'bookmark_len'  : len(bookmarks),
              }
    #url = '/search/bookmark_list?user=' + username
    #return HttpResponseRedirect(url)
    return render(request, 'sum_summary/bookmark_list.html',context)
