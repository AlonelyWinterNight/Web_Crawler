# 웹 크롤러 연습삼아 만드는 중.
# 추후 기사 스크랩 자동화시키려고 만드는거임.
# 테스트베드로 일베를 저 격 한 다 ▄︻̿┻̿═━
import requests
from bs4 import BeautifulSoup
import re

global flag
flag = 1
global li
li = []

def crawlIlbe(max_pages,flag,li):
    page = 1
    while page!=max_pages+1:
        url = 'http://www.ilbe.com/index.php?mid=ilbe&page=' + str(page)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'lxml')
        soup.find('tr')

        print("---"+str(page)+" PAGE")
        # for link in soup.find_all(href=re.compile("http://www.ilbe.com/9")) :
        for link in soup.find_all('tr') :
            url = link.get('href') # URL
            title = link.text# Title
            title = re.sub("\n","",title)
            if title in li :
                continue
            else:
                print("["+str(flag)+"] " + title + "\t" + str(url))
                # print(link) # print the link information
                flag+=1
                if flag >= 23 & flag <= 27:
                    li.append(title)
        page+=1

crawlIlbe(3,flag,li)