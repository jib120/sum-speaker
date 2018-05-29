#sum_summary/views.py

from django.shortcuts import render
from sum_summary.naver_collections import show_top_issue
from django.http import HttpResponse

from sum_summary.models import Candidate,Member,Keyword

def index(request):
    top10 = show_top_issue()
    context = {'top10' : top10}
    return render(request, 'sum_summary/index.html', context)


def search(request):
    keywords = Keyword.objects.all() #해당 테이블에 모든 row를 다 불러온다.
    context = {'Keywords' : keywords}
    return render(request, 'sum_summary/view.html', context)


