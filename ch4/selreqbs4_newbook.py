import re
from selenium import webdriver
import os, requests, csv, urllib, time
from bs4 import BeautifulSoup
from _MyPath import URL, DRIVER as d
import selenium_upload as upload # --- (1)

url_store = 'https://search.kyobobook.co.kr/search?keyword=%EC%A0%9C%EC%9D%B4%ED%8E%8D&gbCode=TOT&target=total'
url_book = URL+'book'

# 책 스크레이핑 후 업로드하기 --- (2)
def import_book():
    # 책 리스트 가져오기 --- (2a)
    booklist = get_bookinfo()
    print(booklist)
    # 책 업로드하기 --- (2b)
    driver = webdriver.Chrome(d)
    driver.get(url_book)
    upload.login_upload(driver, booklist)

# 책 리스트 가져오기 --- (3)
def get_bookinfo():
    html = requests.get(url_store).text
    soup = BeautifulSoup(html, 'html5lib')
    #slist = soup.select_one('#search_list') #--- (3a)
    slist = soup.select_one("ul.prod_list").find_all("li", class_="prod_item")
    infolist =[]
    # tr 요소 4개만 가져오기 --- (4)
    #for tr in slist.find_all('tr', limit=4):
    for prod in slist[0:4]:
        info ={}
        # 책 제목
        #title = tr.select_one('.title strong').string.strip()
        title = prod.select('div.prod_name_group div.auto_overflow_inner a span')[-1].text.strip()
        info['title'] = title
        # 출간일 --- (4a)
        #author = tr.select_one('.author').text.replace("\n","").replace("\t","")
        #author = prod.select('div.prod_author_info div.auto_overflow_inner a.author.rep ')
        date = prod.select_one('div.prod_publish span.date').string.strip()
        #info['date'] = author.split('|')[-1]
        info['date'] = date
        # 가격
        #info['price'] = tr.select_one('.price .org_price del').string
        price = prod.select_one('div.prod_price span.price span.val').string
        info['price'] = price
        # 이미지 --- (4b)
        save_file = './output/{}.jpg'.format(re.sub(r'[/\\?%*:|"<>]', '_', title))
        info['img']= os.path.abspath(save_file)
        # 이미지 파일로 저장 --- (4c)
        #src = tr.img['src']
        img_elt = prod.select_one("div.prod_area div.prod_thumb_box a span.img_box img")
        src = f"https://contents.kyobobook.co.kr/pdt/{img_elt['data-kbbfn-bid']}.jpg"
        res = requests.get(src)
        with open(save_file, 'wb') as fp:
            fp.write(res.content)
        time.sleep(1)
        # 리스트에 딕셔너리 추가
        infolist.append(info)
    return infolist

if __name__ == '__main__':
        import_book()  
