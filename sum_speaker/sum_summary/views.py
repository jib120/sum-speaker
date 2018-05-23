from django.shortcuts import render
from django.http import HttpResponse
from .models import Candidate,Member,Keyword

def index(request):
    candidates = Candidate.objects.all() #해당 테이블에 모든 row를 다 불러온다.
    context = {'candidates' : candidates,
                'candidate_len': len(candidates),
                }
    return render(request, 'sum_summary/index.html', context)

def search(request):
    keywords = Keyword.objects.all() #해당 테이블에 모든 row를 다 불러온다.
    context = {'Keywords' : keywords}
    return render(request, 'sum_summary/view.html', context)
