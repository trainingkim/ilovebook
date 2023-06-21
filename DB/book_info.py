#YES24에서 책 정보를 수집 -> DB에 저장
import requests
from bs4 import BeautifulSoup
import re

base_url = 'http://www.yes24.com/'


def get_xls_info(file_path):  # xls를 가져오는 함수
    with open(file_path, 'r') as f:
        data = f.read()
    soup = BeautifulSoup(data, 'html.parser')
    dict_ = dict()
    for a in soup.find_all('tr', {'bgcolor': 'FFFFFF'}):
        _ = a.find_all('td', 'stext')
        number = _[0].text
        b = _[2].text
        c = _[3].text
        price = _[4].text
        auth = _[6].text
        pub = _[7].text
        dict_[number] = b, c, price, auth, pub  # 딕셔너리 상품번호 상품명 상품가격 저자 출판사
    return dict_


def get_file_path():  # 파일을 가져오는 함수
    return_value = dict()
    for root, path, file_names in list(os.walk('../file/')):
        for file_name in file_names:
            return_value[file_name.split('.')[0]] = os.path.join(r'..\file', file_name)
    return return_value


def create_dir(path):
    """
    디렉토리가 존재하지 않을 경우 디렉토리를 생성하는 함수
    :param path: 디렉토리 위치 경로
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print('Error: Creating directory. ' + path)


# def get_category1(CategoryNumber, sumgb):
#     """
#     대 카테고리 데이터를 가져오는 함수
#     """
#     result = []
#     _CategoryNumber = 'CategoryNumber=' + CategoryNumber
#     _sumgb = 'sumgb=' + sumgb
#     url = base_url + '/24/category/bestseller?' + _CategoryNumber + "&" + _sumgb

#     response = requests.get(url)

#     if response.status_code == 200:
#         html = response.text
#         soup = BeautifulSoup(html, 'html.parser')
#         category1_list = soup.select("#bestMenu .dpth1 #category001 .dpth2 li")

#         for category1_item in category1_list:
#             category1_link = category1_item.select_one("a")
#             category1_text = category1_link.text
#             category1_id = category1_item["id"].replace("category", "")

#             result.append([category1_id, category1_text])

#     return result


# def get_category2(category1_id):
#     """
#     중 카테고리 데이터를 가져오는 함수
#     """
#     result = []

#     url = base_url + '24/category/BestSellerSubCategory/' + category1_id + "?SumGb=06"
#     response = requests.get(url)

#     if response.status_code == 200:
#         html = response.text
#         soup = BeautifulSoup(html, 'html.parser')
#         category2_list = soup.select(".dpth2 li")

#         for category2_item in category2_list:
#             category2_link = category2_item.select_one("a")
#             category2_text = category2_link.text
#             category2_id = category2_item["id"].replace("category", "")

#             result.append([category2_id, category2_text])
#     return result


# def get_category3(category2_id):
#     """
#     소 카테고리 데이터를 가져오는 함수
#     :return:
#     """
#     result = []

#     url = base_url + '24/category/BestSellerSubCategory/' + category2_id + "?SumGb=06"
#     response = requests.get(url)

#     if response.status_code == 200:
#         html = response.text
#         soup = BeautifulSoup(html, 'html.parser')
#         category3_list = soup.select(".dpth2 li")

#         for category3_item in category3_list:
#             category3_link = category3_item.select_one("a")
#             category3_text = category3_link.text
#             category3_id = category3_item["id"].replace("category", "")

#             result.append([category3_id, category3_text])

#     return result


def get_book_list(category_id, page, fetch_size): #dict로 반환
    result = []

    _CategoryNumber = "CategoryNumber=" + category_id
    _Page = "PageNumber=" + page
    _FetchSize = "FetchSize=" + fetch_size
    _sumgb = "sumgb=06"
    url = base_url + "24/category/bestsellerExcel?" + _CategoryNumber + "&" + _sumgb + "&" + _Page + "&" + _FetchSize

    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all('tr')[1:]

        for row in rows:
            cells = row.find_all('td')
            product_number = cells[2].text.strip()
            price = int(re.sub(r'\D', '', cells[4].text.strip()))
            product_name = cells[3].text.strip()
            author = cells[6].text.strip()
            publisher = cells[7].text.strip()
            rank = int(cells[0].text.strip())

            item = {
                'product_number': product_number,
                'price': price,
                'product_name': product_name,
                'author': author,
                'publisher': publisher,
                'rank': rank
            }

            result.append(item)

    return result


def save_book_list(path, filename, datas): #json으로 저장
    with open(path + filename, 'a', encoding='utf-8') as f:
        json.dump(datas, f, indent="\t", ensure_ascii=False)


import os
import mysql.connector
import json

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  database="book"
)

mycursor = mydb.cursor()

JUM_1 = "SELECT * FROM review where JUM_1=%s"
JUM_2 = "SELECT * FROM review where JUM_=%s"
sql = "INSERT INTO b_info_1 (B_Num,B_Pri,B_Name,B_Auth,B_Pub,B_CATE,B_CATE2,B_CATE3, B_RAN,B_AVE) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"
# 필드 상품번호 / 상품가격 / 상품명 / 저자 / 출판사 / 카테고리1 / 카테고리2 / 랭크

if __name__ == "__main__":  # xls 필요정보들 읽어서 DB에 저장
    book_ids = []
    data_list = []

    """
        카테고리 데이터 맵 만들기
    """
    # 환경 변수
    fetchSize = 20  # 80

    # 카테고리 가져오는 작업
    product_ids = []

    # 파일 디렉토리 존재하는지 확인 후 생성
    filePath = "../file"
    create_dir(filePath)

    # #카테고리 1 가져오는 작업
    # for [c1_id, c1_text] in get_category1("001", "06"):
    #     books = []
    #     print("### 카테고리 1 : " + c1_text + " 시작")
    
    #     for [c2_id, c2_text] in get_category2(c1_id):
    #         print("### 카테고리 2 : " + c2_text + " 시작")
    
    #         for [c3_id, c3_text] in get_category3(c2_id):
    #             print("### 카테고리 3 : " + c3_text + " 시작")
    #             c3_page = 1
    
    #             while True:
    #                 c3_books = get_book_list(c3_id, str(c3_page), str(fetchSize))
    #                 time.sleep(1)
    
    #                 for c3_book in c3_books:
    #                     if c3_book["product_number"] not in product_ids:
    #                         product_ids.append(c3_book["product_number"])
    #                         books.append({
    #                             "B_Num": c3_book["product_number"],
    #                             "B_Pri": c3_book["price"],
    #                             "B_Name": c3_book["product_name"],
    #                             "B_Auth": c3_book["author"],
    #                             "B_Pub": c3_book["publisher"],
    #                             "B_RAN": (fetchSize * (c3_page - 1)) + c3_book["rank"],
    #                             "B_CATE": c1_text,
    #                             "B_CATE2": c2_text,
    #                             "B_CATE3": c3_text,
    #                             "B_AVE": 0,
    #                             "B_NUM_1": None,
    #                             "B_NUM_2": None,
    #                         })
    #                 if len(c3_books) == 0:
    #                     break
    #                 else:
    #                     c3_page = c3_page + 1
    
    #                 # TODO : 이 부분을 주석처리하면 페이지 끝까지 처리 가능
    #                 break
    #                 # TODO : 이 부분을 주석처리하면 페이지 끝까지 처리 가능
    
    #             print("### 카테고리 3 : " + c3_text + " 끝")
    
    #         c2_page = 1
    
    #         while True:
    #             c2_books = get_book_list(c2_id, str(c2_page), str(fetchSize))
    #             time.sleep(1)
    
    #             for c2_book in c2_books:
    #                 if c2_book["product_number"] not in product_ids:
    #                     product_ids.append(c2_book["product_number"])
    #                     books.append({
    #                         "B_Num": c2_book["product_number"],
    #                         "B_Pri": c2_book["price"],
    #                         "B_Name": c2_book["product_name"],
    #                         "B_Auth": c2_book["author"],
    #                         "B_Pub": c2_book["publisher"],
    #                         "B_RAN": (fetchSize * (c2_page - 1)) + c2_book["rank"],
    #                         "B_CATE": c1_text,
    #                         "B_CATE2": c2_text,
    #                         "B_CATE3": None,
    #                         "B_AVE": 0,
    #                         "B_NUM_1": None,
    #                         "B_NUM_2": None,
    #                     })
    
    #             if len(c2_books) == 0:
    #                 break
    #             else:
    #                 c2_page = c2_page + 1
    
    #             # TODO : 이 부분을 주석처리하면 페이지 끝까지 처리 가능
    #             break
    #             # TODO : 이 부분을 주석처리하면 페이지 끝까지 처리 가능
    
    #         print("### 카테고리 2 : " + c2_text + " 끝")
    
    #     c1_page = 1
    
    #     while True:
    #         c1_books = get_book_list(c1_id, str(c1_page), str(fetchSize))
    #         time.sleep(1)
    
    #         for c1_book in c1_books:
    #             if c1_book["product_number"] not in product_ids:
    #                 product_ids.append(c1_book["product_number"])
    #                 books.append({
    #                     "B_Num": c1_book["product_number"],
    #                     "B_Pri": c1_book["price"],
    #                     "B_Name": c1_book["product_name"],
    #                     "B_Auth": c1_book["author"],
    #                     "B_Pub": c1_book["publisher"],
    #                     "B_RAN": (fetchSize * (c1_page - 1)) + c1_book["rank"],
    #                     "B_CATE": c1_text,
    #                     "B_CATE2": None,
    #                     "B_CATE3": None,
    #                     "B_AVE": 0,
    #                     "B_NUM_1": None,
    #                     "B_NUM_2": None,
    #                 })
    
    #         if len(c1_books) == 0:
    #             break
    #         else:
    #             c1_page = c1_page + 1
    
    #         # TODO : 이 부분을 주석처리하면 페이지 끝까지 처리 가능
    #         break
    #         # TODO : 이 부분을 주석처리하면 페이지 끝까지 처리 가능
    
    #     save_book_list(filePath + "/", c1_text.replace("/", "_") + ".json", books)
    #     print("### 카테고리 1 : " + c1_text + " 끝")

    """
        DB에 데이터 넣는 작업
    """
    dataFileList = os.listdir(os.path.abspath(filePath))

    for dataFile in dataFileList:
        print(dataFile)
        with open(filePath + "/" + dataFile, 'r', encoding="UTF8") as file:
            books = json.load(file)
            for book in books:
                B_Num = book["B_Num"]
                B_Pri = book["B_Pri"]
                B_Name = book["B_Name"]
                B_Auth = book["B_Auth"]
                B_Pub = book["B_Pub"]
                B_CATE = book["B_CATE"]
                B_CATE2 = book["B_CATE2"]
                B_RAN = book["B_RAN"]
                B_AVE = book["B_AVE"]
                B_NUM_1 = book["B_NUM_1"]
                B_NUM_2 = book["B_NUM_2"]
                B_CATE3 = book["B_CATE3"]
    
                val = B_Num, B_Pri, B_Name, B_Auth, B_Pub, B_CATE, B_CATE2, B_CATE3, B_RAN, B_AVE
                mycursor.execute(sql, val)
                mydb.commit()

    '''
    DB에 b_info 데이터를 넣는 작업1
    '''
    # for key, value in list(get_file_path().items()):
    #     print(f"{key} GET")
    #     product = get_xls_info(value)
    #     for rank, product_info in list(product.items())[:10]:
    #         B_Num = int(product_info[0])
    #         B_Pri = int(product_info[2].replace(',','').replace("원", ""))
    #         B_NAME = product_info[1]
    #         B_AUTH = product_info[3]
    #         B_Pub = product_info[4]
    #         if len(key.split('-')) == 2:
    #             B_CATE, B_CATE2 = key.split('-')
    #         else:
    #             B_CATE = key.split('-')[0]
    #             B_CATE2 = '-'.join(key.split('-')[1:])
    #         B_CATE2 = B_CATE2.replace("_", "/")
    #         B_RAN = rank
    #         B_AVE = 0
    #         val = B_Num, B_Pri, B_NAME, B_AUTH, B_Pub, B_CATE, B_CATE2, B_RAN,B_AVE
    #         mycursor.execute(sql, val)
    #         mydb.commit()
    '''
    DB에 넣은 review 데이터를 통해서 평균을 구하는 작업2
    '''
    # select_query = "select b_num from b_info_1;"
    
    # review_query = "select JUM_1, JUM_2 from review where B_Num = %s"
    # update_query = "UPDATE b_info_1 SET B_NUM_1=%s, B_NUM_2=%s, B_AVE=%s where B_NUM = %s"
    # mycursor.execute(select_query) #execute
    # b_nums = mycursor.fetchall()
    # for b_num in b_nums:
    #     result_num1 = 0
    #     result_num2 = 0
    #     print(b_num[0])
    #     mycursor.execute(review_query, (b_num[0],))
    #     reviews = mycursor.fetchall()
    #     for num1, num2 in reviews:
    #         result_num1 += num1
    #         result_num2 += num2
    #     len_ = len(reviews)
    #     if len_:
    #         result_num1 = round(result_num1/len_, 2)
    #         result_num2 = round(result_num2/len_,  2)
    #         ave = round((result_num1 + result_num2) / 2, 2)
    #     else:
    #         result_num1 = 0
    #         result_num2 = 0
    #         ave = 0
    #     parameters = (result_num1, result_num2, ave, b_num[0])
    #     mycursor.execute(update_query, parameters)
    #     mydb.commit()
