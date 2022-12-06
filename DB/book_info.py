import os, time
from turtle import onclick
import requests
from bs4 import BeautifulSoup

def get_xls_info(file_path):#xls를 가져오는 함수
    with open(file_path,'r')as f:
            data = f.read()
    soup = BeautifulSoup(data, 'html.parser')
    dict_ = dict()
    for a in soup.find_all('tr',{'bgcolor':'FFFFFF'}):
        _ = a.find_all('td','stext')
        number = _[0].text
        b = _[2].text 
        c = _[3].text
        price = _[4].text
        auth = _[6].text
        pub = _[7].text
        dict_[number]= b,c, price, auth, pub #딕셔너리 상품번호 상품명 상품가격 저자 출판사
    return dict_

def get_file_path(): #파일을 가져오는 함수
    return_value = dict()
    for root, path, file_names in list(os.walk('../file/')):
        for file_name in file_names:
            return_value[file_name.split('.')[0]] = os.path.join(r'..\file',file_name)
    return return_value

def get_ave():
    for a in list(os.walk('../review/')):
        aver=int(a.JUM_1+a.JUM_2)/2
        return aver

import os
import mysql.connector
import json

mydb = mysql.connector.connect(#DB연결
  host="localhost",
  user="root",
  password="dkqkffhs123",
  database="book"
)
mycursor = mydb.cursor()


JUM_1 = "SELECT * FROM review where JUM_1=%s"
JUM_2 = "SELECT * FROM review where JUM_=%s"
#sql = "INSERT INTO B_info (B_Num,B_Pri,B_Name,B_Auth,B_Pub,B_CATE,B_CATE2,B_RAN,B_AVE) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)"
#필드 상품번호 / 상품가격 / 상품명 / 저자 / 출판사 / 카테고리1 / 카테고리2 / 랭크

if __name__ == "__main__": #xls 필요정보들 읽어서 DB에 저장
    select_query = "select b_num from b_info;"

    review_query = "select JUM_1, JUM_2 from review where B_Num = %s"
    update_query = "UPDATE b_info SET B_NUM_1=%s, B_NUM_2=%s, B_AVE=%s where B_NUM = %s";
    mycursor.execute(select_query)
    b_nums = mycursor.fetchall()
    for b_num in b_nums:
        result_num1 = 0
        result_num2 = 0
        print(b_num[0])
        mycursor.execute(review_query, (b_num[0],))
        reviews = mycursor.fetchall()
        for num1, num2 in reviews:
            result_num1 += num1
            result_num2 += num2
        len_ = len(reviews)
        if len_:
            result_num1 = round(result_num1/len_, 2)
            result_num2 = round(result_num2/len_,  2)
            ave = round((result_num1 + result_num2) / 2, 2)
        else:
            result_num1 = 0
            result_num2 = 0
            ave = 0
        parameters = (result_num1, result_num2, ave, b_num[0])
        mycursor.execute(update_query, parameters)
        mydb.commit()
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
    #         B_AVE = get_ave()
    #         val = B_Num, B_Pri, B_NAME, B_AUTH, B_Pub, B_CATE, B_CATE2, B_RAN,B_AVE
    #         #mycursor.execute(sql, val)
    #         mydb.commit()