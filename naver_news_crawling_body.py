import sys, os
import requests
import selenium
from selenium import webdriver
import requests
from pandas import DataFrame
from bs4 import BeautifulSoup
import re
from datetime import datetime
import pickle, progressbar, json, glob, time
from tqdm import tqdm


#날짜 저장
date = str(datetime.now())
date = date[:date.rfind(':')].replace(' ', '_')
date = date.replace(':', '시') + '분'

sleep_sec = 0.5


#언론사별 본문 위치 태그 파싱 함수
print('분문 크롤링에 필요한 함수를 로딩하고있습니다...\n' + '-' * 100)
def crawling_main_text(url):

    req = requests.get(url)
    req.encoding = None
    soup = BeautifulSoup(req.text, 'html.parser')

    #연합뉴스
    if ('://yna' in url) | ('app.yonhapnews' in url):
        main_article = soup.find('div', {'class': 'story-news article'})
        if main_article == None:
            main_article = soup.find('div', {'class': 'article-txt'})

        text = main_article.text

    else:
        text == None

    return text.replace('\n', '').replace('\r', '').replace('<br>', '').replace('\t', '')

press_nm = '연합뉴스'

print('검색할 언론사 : {}'.format(press_nm))


#브라우저를 켜고 검색 키워드 입력
query = input('검색할 키워드 : ')
news_num = int(input('수집 뉴스의 수(숫자만 입력) : '))

print('\n' + '=' * 100 + '\n')

print('브라우저를 실행시킵니다(자동 제어)\n')
chrome_path = '/Users/ohikendoit/chromedriver'
browser = webdriver.Chrome(chrome_path)

news_url = 'https://search.naver.com/search.naver?where=news&query={}'.format(query) + "&sort=1&photo=0&field=0&pd=0&ds=&de=&mynews=1&office_type=1&office_section_code=2&news_office_checked=1001"
browser.get(news_url)
time.sleep(sleep_sec)


#뉴스 크롤링
print('\n크롤링을 시작합니다.')
# ####동적 제어로 페이지 넘어가며 크롤링
news_dict = {}
idx = 1
cur_page = 1

pbar = tqdm(total=news_num ,leave = True)

while idx < news_num:

    table = browser.find_element_by_xpath('//ul[@class="list_news"]')
    li_list = table.find_elements_by_xpath('./li[contains(@id, "sp_nws")]')
    area_list = [li.find_element_by_xpath('.//div[@class="news_area"]') for li in li_list]
    a_list = [area.find_element_by_xpath('.//a[@class="news_tit"]') for area in area_list]

    for n in a_list[:min(len(a_list), news_num-idx+1)]:
        n_url = n.get_attribute('href')
        news_dict[idx] = {'title' : n.get_attribute('title'),
                          'url' : n_url,
                          'text' : crawling_main_text(n_url)}

        idx += 1
        pbar.update(1)

    if idx < news_num:
        cur_page +=1

        pages = browser.find_element_by_xpath('//div[@class="sc_page_inner"]')
        next_page_url = [p for p in pages.find_elements_by_xpath('.//a') if p.text == str(cur_page)][0].get_attribute('href')

        browser.get(next_page_url)
        time.sleep(sleep_sec)
    else:
        pbar.close()

        print('\n브라우저를 종료합니다.\n' + '=' * 100)
        time.sleep(0.7)
        browser.close()
        break


#데이터 전처리
print('데이터프레임 변환\n')
news_df = DataFrame(news_dict).T

folder_path = os.getcwd()
xlsx_file_name = '네이버뉴스_본문_{}개_{}_{}.xlsx'.format(news_num, query, date)

news_df.to_excel(xlsx_file_name)

print('엑셀 저장 완료 | 경로 : {}\\{}\n'.format(folder_path, xlsx_file_name))

os.startfile(folder_path)

print('=' * 100 + '\n결과물의 일부')
news_df