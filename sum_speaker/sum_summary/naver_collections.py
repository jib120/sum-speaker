import requests
from bs4 import BeautifulSoup

def show_top_issue():
    html_result = requests.get("https://www.naver.com").text
    soup = BeautifulSoup(html_result, "html.parser")

    title_list = soup.select('.PM_CL_realtimeKeyword_rolling span.ah_k')
    #top 10만 보여준다
    top10 =[]
    for idx, title in enumerate (title_list, 1):
        if idx==13:
            break
        top10.append(title.text)

    return top10
