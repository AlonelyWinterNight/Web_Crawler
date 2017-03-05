# 웹 크롤러 연습삼아 만드는 중.
# 추후 기사 스크랩 자동화시키려고 만드는거임.
# 테스트베드로 일베를 저 격 한 다 ▄︻̿┻̿═━
import requests
from bs4 import BeautifulSoup
import re

#-------------------------------------------------------------------------------------------------------------------
# 서치인일베 : 일간베스트 中 키워드 검색 기능
#-------------------------------------------------------------------------------------------------------------------
def searchInIlbe(max_pages):
    # search = input("검색어가 뭐이노? : ")
    search = "씨발년아"
    page = 1
    flag = 1
    li=[]
    while page!=max_pages+1:
        url = str("http://www.ilbe.com/index.php?_filter=search&mid=ilbe&search_target=title&search_keyword=" + str(search) + "&page=" + str(page))
        source_code = requests.get(str(url))
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'lxml')
        # 속도 개선 필요.
        # 현재 : 검색 -> 파싱 -> 예외처리하여 타이틀 , URL 출력
        # 개선 : 검색 -> 파싱 -> 예외처리하여 타이틀 , URL 각각 리스트/스택에 저장 -> 출력
        print("---"+str(page)+" PAGE")
        for link in soup.find_all(href=re.compile("&document_srl=")) :
            url = link.get('href')  # URL
            title = link.text  # Title

            if page==1 & (flag==1 or flag==2 or flag>=25):
                print("[" + str(flag) + "] " + title + " " + url)
                flag += 1
                li.append(title)
                continue

            if title in li:
                continue
            else:
                print("[" + str(flag) + "] " + title + " " + url)
                flag += 1
        page+=1

searchInIlbe(3)