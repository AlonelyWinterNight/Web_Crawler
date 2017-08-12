# 웹 크롤러 연습삼아 만드는 중.
# 목표 : 프로파일러
# ㄴ 추후 기사 스크랩 자동화시킬수있을것임.
# ㄴ 일베 예비범죄자 / 반동분자 프로파일러로 사용 가능할것임.
# ㄴ 일베 트렌드 파악 십가능 ㅎㅎ
# 테스트베드로 일베를 저 격 한 다 ▄︻̿┻̿═━

import requests
import MySQLdb
from bs4 import BeautifulSoup
import re

def save_record(con_num, con_title, con_url):
    # Open database connection
    db = MySQLdb.connect(host="", user="root", passwd="rhf0128", db="test")
    db.set_character_set('utf8') # Prepare a cursor object using cursor() method
    cursor = db.cursor()
    #  Prepare SQL query to INSERT a record into the database
    sql = "INSERT INTO board (con_num, con_title, con_url)" \
          "VALUES (%s, %s, %s)"%\
        ("'"+str(con_num)+"'", "'"+str(con_title)+"'", "'"+str(con_url)+"'")
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit changes in the database
        db.commit()
        # cursor.execute("""SELECT title, article, date, writer, vcnt FROM document""")
        # print(cursor.fetchall())
    except Exception as e:
        print(str(e))
        #  Rollback in case there is any error
        db.rollback()
        #  Disconnect from database
        db.close()

#-------------------------------------------------------------------------------------------------------------------
# 크롤릴베 : 일간베스트 게시물 최근 10페이지 크롤링, 링크
# Extract values from bs4.element.tag 의 과정을 좀 더 이해해야함.
#------------------------------------------------------이슈---------------------------------------------------------
# 인기게시물을 배제한 크롤링 필요.
# ㄴ 불가피하여 list 중복검사를 통해 회피함. 글번호?
# ㄴ dictonary 이용한 frequency filter 적용 가능할 것.
#------------------------------------------------------과제---------------------------------------------------------
# 1. 타이틀 기준 핫 키워드 빈도 검사, 실제 핫키워드 Arabogi 기능 츄가
# ㄴ 트렌드 분석 ~ 토픽 분석 까지.
#-------------------------------------------------------------------------------------------------------------------
def crawlIlbe(max_pages):
    page = 1
    global flag
    flag = 1
    global li
    li = []
    while page!=max_pages+1:
        url = 'http://www.ilbe.com/index.php?mid=ilbe&page=' + str(page)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'lxml')

        print("---"+str(page)+" PAGE")
        for link in soup.find_all(href=re.compile("http://www.ilbe.com/9")) :
        # for link in soup.find_all("tr",re.compile("bg")) :
            url = link.get('href') # URL
            title = link.text# Title
            title = re.sub("\n","",title)
            if title in li :
                continue
            else:
                print("["+str(flag)+"] " + title + "\t" + str(url))
                save_record(int(flag),title,str(url))
                # print(link) # print the link information
                flag+=1
                if flag >= 23 & flag <= 27:
                    li.append(title)
        page+=1

#-------------------------------------------------------------------------------------------------------------------
# 서치인일베 : 일간베스트 中 키워드 검색 기능
# 속도 개선 필요.
#------------------------------------------------------이슈---------------------------------------------------------
# 1. 검색량이 적을 때 ( 검색 결과가 2페이지 이상 나오지 않거나 1페이지에 게시물 22개 미만)
# ㄴ 전체 검색 결과를 한 data set에 저장하고, 후출력 하는게 좋겠음.
# ㄴ 속도 개선 후에 알맞게 적용.
#------------------------------------------------------과제---------------------------------------------------------
# 1. 속도 개선
# 현재 : 검색 -> 파싱 -> 예외처리하여 타이틀 , URL 출력
# 개선 방안 : 검색 -> 파싱 -> 예외처리하여 타이틀 , URL 각각 리스트/스택에 저장 -> 출력
# 2. 키워드 추출과 토픽 분석 , 자연어처리
# 현재 : 자료구조 변경 필요. 전체 검색결과를 data set으로 저장해야 함.
# 도입 방안 : 자연어처리 -> 데이터 시각화 방안 마련 필요. 그리고 이걸 web에서 어떻게 보여줄지?
# 자연어처리 : KoNLP 사용. 알고리즘에 유의하자.
#-------------------------------------------------------------------------------------------------------------------

def searchInIlbe(max_pages):
    search = input("검색어가 뭐이노? : ")
    page = 1
    flag = 1
    num = 1
    li = []
    while page!=max_pages+1:
        url = "http://www.ilbe.com/index.php?_filter=search&mid=ilbe&search_target=title&search_keyword="+search+"&page=" + str(page)
        source_code = requests.get(str(url))
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'lxml')

        print("---"+str(page)+" PAGE")
        for link in soup.find_all(href=re.compile("&document_srl=")) :
            url = link.get('href')  # URL
            title = link.text  # Title
            if page==1 & (flag==1 or flag==2 or flag>=25):
                li.append(title)
                flag+=1
                continue
            if title in li:
                continue
            else:
                print("[" + str(num) + "] " + title + " " + url)
                flag += 1
                num += 1
        page+=1

#-------------------------------------------------------------------------------------------------------------------
# 메인 프로그램 구동부
#-------------------------------------------------------------------------------------------------------------------
state = 1
while state!=0:
    asdf = input("\n-------------------------------\n"+"일베뚞딲(1) 일베검색(2) 스돕(0)"+"\n-------------------------------\n")
    asdf = int(asdf)
    if asdf == 0:
        state=0
        break;

    elif asdf == 1:
        crawlIlbe(10)

    elif asdf == 2:
        searchInIlbe(10)