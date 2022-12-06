from ast import Num
import string
from pkg_resources import ensure_directory
import requests 
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as BF

def get_cate():#카테고리의 이름과 링크를 받는 함수
    url = "http://www.yes24.com/Mall/Main/Book/001?CategoryNumber=001"
    html = requests.get(url).text 
    soup = BeautifulSoup(html, 'html.parser')
    main_dict = dict() 
    for main_li_tag in soup.find_all("li","cate2d"): 
        cate = main_li_tag.find('em').get_text() 
        main_dict[cate] = list()
        for li_tag in main_li_tag.find_all('li'):
            a_tag = li_tag.find('a')
            cate_name = a_tag.get_text()
            cate_link = a_tag['href']
            main_dict[cate].append((cate_name, cate_link))
    return main_dict 

def get_book_rank(url):
    url = url + "?fetchsize=100&ParamSortTp=05"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    if not soup.find('div','cCont_sortArea'):
        url=url.replace('Display','More')
        url = url + "&ElemNo=104&ElemSeq=1"
        r=requests.get(url)
        soup=BeautifulSoup(r.text,"html.parser")
    book_rank = dict()
    rank = 1
    if True:
        for a in soup.find_all('div','goods_info')[1:]:
            b = a.find('div','goods_name')
            b = b.find('a')
            c = a.find('span','goods_auth')
            d = a.find('span','goods_pub')
            e = a.find('span','goods_date')
            f = a.find('em','yes_b')
            g = a.find('span','gd_rating')
            aa = a.find('div','goods_name')
            h = 'http://www.yes24.com'+aa.find('a')['href']
            _bname = b.get_text()
            if c:
                _bauth = c.get_text()
            else:
                _bauth = ""
            if d:
                _bpub = d.get_text()
            else:    
                _bpub = ""
            if e:
                _byear = e.get_text()
            else:
                _byear = ""
                
            _bprice = f.get_text()
            _bpage = h
            try:
                _brank = g.get_text()
            except :
                _brank = ''
            book_dict = dict()
            book_dict['name'] = _bname.strip()
            book_dict['auth'] = _bauth.strip()
            book_dict['pub'] = _bpub.strip()
            book_dict['year'] = _byear.strip()
            book_dict['price'] = int(_bprice.strip().replace(',',''))
            book_dict['rank'] = _brank.strip()
            book_dict['page'] = _bpage
            book_rank[rank] = book_dict
            rank+=1
    return book_rank

def file_download(url,file_name):#엑셀파일 다운로드
    download_url = "http://yes24.com/24/category/bestsellerExcel?CategoryNumber={}&sumgb=09&FetchSize=100".format(url.split('/')[-1])
    r = requests.get(download_url)
    with open('file//{}'.format(file_name), 'wb')as f:
        if len(r.content) == 0:
            print("ERROR", file_name)
            exit()
        f.write(r.content)



def get_comment(url,file_name):#엑셀불러오기
    html = requests.get(url)
    soup = BeautifulSoup(html, 'html.parser')
    numurl = dict()
    with open(r'C:\Users\olalu\Desktop\ilovebook\file\가정 살림-결혼_가족.xls','r')as f:
        data = f.read
    for a in soup.find_all('tbody'):
        b = a.find('td','stext')

    for urls in len(b): #url리스트에 상품번호 삽입
            numurl = "http://www.yes24.com/Product/communityModules/GoodsReviewList/{}".format(b).strip()
    
    
def get_id(url): 
    html = requests.get(url)
    soup = BeautifulSoup(html, 'html.parser')
    for a in soup.find_all('div','review_lnk'): #ID
            b= a.find('a')['href']

import json
import time
cate = get_cate() 
book_comment = dict()
book_id = dict()

for key, value in cate.items(): 
    print("{}/{}\t{}".format(list(cate.keys()).index(key)+1,len(cate.keys()), key))
    book_comment[key] = dict()
    index = 1
    len_ = len(value)
    for cate_key, link in value:
        file_name = key.replace('/',',') + "-" + cate_key.replace('/','_') + ".xls"
        print("\t{}:{}/{}".format(key+"-"+cate_key,index, len_))
        file_download(link, file_name)
        book_comment[key][cate_key] = get_comment(link)
        index += 1
    time.sleep(0.5)

with open('comment.jason','r',encoding ='utf-8')as fd:
    json.dump(book_comment, fd, ensure_ascii=False, indent = 3)

with open('id_list.jason','r',encoding ='utf-8')as fd: #ID를 JSON 에 저장
    json.dump(book_id, fd, ensure_ascii=False, indent = 3)