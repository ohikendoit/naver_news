#coding utf-8
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import re

#크롤링 결과를 저장하기 위한 리스트 선언
title_text = []
link_text = []
source_text = []
date_text = []
article_text = []
contents_text = []
result = {}

#요청 해더 추가 - Get요청 차단시 변경 필요
headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}

#결과 엑셀 저장하기 위한 변수
RESULT_PATH = '/Users/ohikendoit/Downloads/'
now = datetime.now()

#날짜 정제화 함수
def date_cleaning(test):
    try:
        pattern = '\d+.(\d+).(\d+).'

        r = re.compile(pattern)
        match = r.search(test).group(0)
        date_text.append(match)

    except AttributeError:
        pattern = '\w* (\d\w*)'

        r = re.compile(pattern)
        match = r.search(test).group(1)
        date_text.append(match)

#내용 정제화 함수
def contents_cleaning(contents):
    first_cleaning_contents = re.sub('<dl>.*?</a> </div> </dd> <dd>', '',
                                      str(contents)).strip()  #앞에 필요없는 부분 제거
    second_cleaning_contents = re.sub('<ul class="relation_lst">.*?</dd>', '',
                                       first_cleaning_contents).strip()#뒤에 필요없는 부분 제거 (새끼 기사)
    third_cleaning_contents = re.sub('<.+?>', '', second_cleaning_contents).strip()
    contents_text.append(third_cleaning_contents)

#최대페이지 수 구하는 함수; Pagination Crawling Module
def max_page(query):
    max_page=0

    for i in range(1, 4000, 10):
        url = "https://search.naver.com/search.naver?where=news&query="+str(query)+"&sort=1&pd=0&ds=&de=&mynews=1&office_type=1&office_section_code=2&news_office_checked=1001&nso=so:dd,p:all,a:all&start="+int(i)
        response = requests.get(url, headers=headers)
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')

#크롤링 함수
def crawler(maxpage, query):
    page = 1
    maxpage_t = (int(maxpage)-1)*10+1

    while page <= maxpage_t:
        #연합뉴스 매체만 선택함: mynews, office_type, office_section_code, news_office_checked 변수값 지정됨
        #기간설정 디폴트값음 전체
        url = "https://search.naver.com/search.naver?where=news&query="+query+"&sort=1&pd=0&ds=&de=&mynews=1&office_type=1&office_section_code=2&news_office_checked=1001&nso=so:dd,p:all,a:all&start="+str(page)

        response = requests.get(url, headers=headers)
        html = response.text

        #뷰티풀수프의 인자값 지정
        soup = BeautifulSoup(html, 'html.parser')

        #<a>태그에서 제목과 링크주소 추출
        atags = soup.select('.news_tit')
        for atag in atags:
            title_text.append(atag.text)
            link_text.append(atag['href'])

        #찾은 링크를 기반으로 본문 내용을 가져오기
        article_content = ''
        atags = soup.select('.news_tit')
        for atag in atags:
            main_url = atag['href']

            if ('://yna' in main_url) | ('app.yonhapnews' in main_url):
                req = requests.get(main_url)
                req.encoding = None
                soup_article = BeautifulSoup(req.text, 'html.parser')

                main_article = soup_article.find('article', {'class': 'story-news article'})
                if main_article is not None:
                    for line in main_article.select('p'):
                        article_content += line.get_text()
                        article_content_clean = article_content.replace('\n', '').replace('\r', '').replace('<br>', '').replace('\t', '')
                    article_text.append(article_content_clean)
                else:
                    pass
            else:
                pass


        #신문사 추출
        source_lists = soup.select('.info_group > .press')
        for source_list in source_lists:
            source_text.append(source_list.text)

        #날짜 추출
        date_lists = soup.select('.info_group > span.info')
        for date_list in date_lists:
            if date_list.text.find("면") == -1:
                date_text.append(date_list.text)

        #본문 요약본
        contents_list = soup.select('.news_dsc')
        for contents_list in contents_list:
            contents_cleaning(contents_list)

        #모든 리스트 요소를 딕셔너리형태로 저장
        result = {"date_published": date_text, "company": query, "news_title": title_text, "source_media": source_text, "contents_summary": contents_text, "article": article_text, "url_link": link_text}
        print(page)
        print(result)
        df = pd.DataFrame(result)
        page += 10

    #새로 만들 파일이름 지정
    outputFileName = '%s-%s-%s %s시 %s분 %s초 merging.xlsx' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    df.to_excel(RESULT_PATH+outputFileName,sheet_name='sheet1')

def main():
    info_main = input("="*50 + "\n" + "입력 형식에 맞게 입력해주세요." + "\n" + "시작하시려면 Enter를 눌러주세요." + "\n" + "="*50)

    maxpage = input("최대 크롤링할 페이지 수 를 입력하시오: ")
    query = input("검색어 입력: ")
    crawler(maxpage, query)

main()