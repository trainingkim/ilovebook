import os, time
from turtle import onclick
import requests
from bs4 import BeautifulSoup

sess = requests.Session() 
sess.proxies = {'http':'socks5://127.0.0.1:9150', 'https':'socks5://127.0.0.1:9150'}#토르를 쓰기위한 프록시 설정
adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
sess.mount("http://", adapter)

def get_xls_info(file_path): #xls파일 정보를 딕셔너리에 저장하는 함수
    with open(file_path,'r')as f:
            data = f.read()
    soup = BeautifulSoup(data, 'html.parser')
    dict_ = dict()
    for a in soup.find_all('tr',{'bgcolor':'FFFFFF'}):
        _ = a.find_all('td','stext')
        number = _[0].text
        b = _[2].text 
        c = _[3].text
        dict_[number]= b,c  
    return dict_

def make_link(p_num):#리뷰링크들 가져오는 함수
    m_num = p_num
    murl = "http://www.yes24.com/Product/communityModules/GoodsReviewList/{}".format(m_num)
    #http://www.yes24.com/Product/communityModules/GoodsReviewList/상품번호
    return murl

def get_file_path():#파일경로 받아오는 함수
    return_value = dict()
    for file_name in list(os.walk('./file/'))[0][2]:
        return_value[file_name.split('.')[0]] = os.path.join(r'.\file',file_name)
    return return_value

def rank_info(info):#평점 정보수집하는 함수
    html = sess.get(info)
    soup = BeautifulSoup(html, 'html.parser')
    for a in soup.find_all('div','review_etc'):
        rank = a.find('span','rating rating_5 bgGD')
    return rank

def get_id(code):#블로그의 아이디를 얻는 함수
    url = "http://www.yes24.com/Member/FTGoMemBlog.aspx?mem_no={}&type=blog".format(code)
    html = sess.get(url).text.split('.com/')[-1].split('"')[0]
    return html

def get_review(url):#아이디와 평점을 가져오는 함수
    html = sess.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    all_review = dict()
    try:
        max_page = int(soup.find("a", class_="bgYUI end").attrs['href'].split('=')[-1])
    except:
        max_page = 1
    for i in range(1, max_page+1):
        _ = f"{url}?PageNumber={i}"
        html_2 = sess.get(_).text
        soup = BeautifulSoup(html_2, 'html.parser')
        for j in soup.find_all('div','review_etc'):
            _ = j.find('span','review_rating').find_all('span')
            score = int(_[0].get_text()[2]), int(_[1].get_text()[2])
            txt_id = j.find('em', 'txt_id').find('a').attrs['onclick'].split(', ')[1].replace("'", '')
            all_review[get_id(txt_id)]=score
        time.sleep(0.5)
    return all_review

import os
import json

if __name__ == "__main__":
    for key, value in list(get_file_path().items())[31:]:
        print(f"{key} GET")
        product = get_xls_info(value)
        for rank, product_info in list(product.items())[:10]:
            url = make_link(product_info[0])
            print("│ {}-{}({}/{})".format(product_info[0], product_info[1], rank, 10))
            with open(f'review/{product_info[0]}.json', 'w')as f:
                json.dump(get_review(url), f, ensure_ascii=False, indent = 3)