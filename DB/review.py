import os, time
from turtle import onclick
import requests
from bs4 import BeautifulSoup
import json

def get_file_path():#리뷰DB
    for file_name in list(os.walk('../review/')):
        return file_name[2]

def get_jason(path):#제이슨파일 
    f = open(path)
    try:
        data = json.load(f)
    except:
        data = dict()
    f.close()
    return data



reviews = dict()
for j_p in get_file_path():
    reviews[j_p.split('.')[0]] = get_jason('../review/'+j_p)
#print(j_p)


import mysql.connector
import json

mydb = mysql.connector.connect(#Database 연결
   host="localhost",
   user="root",
   password="dkqkffhs123",
   database="book"
 )
mycursor = mydb.cursor() #mysql
sql = "INSERT INTO review (USER, B_NUM, RAN, CATE, CATE2,JUM_1,JUM_2) VALUES (%s,%s,%s,%s,%s,%s,%s)"

if __name__ == "__main__":#select * from b_info where B_Num = {} order by B_RAN ASC;
     for book_num, reviews_dict in reviews.items():
        print(f"{book_num} review get")
        mycursor.execute("select B_RAN, B_CATE, B_CATE2  from b_info where B_Num = {} order by B_RAN ASC limit 1;".format(book_num))
        try:
            book_info = mycursor.fetchall()[0]
        except:
            continue
        for id, score in list(reviews_dict.items()):
            USER = id
            RAN = int(book_info[0])
            CATE = book_info[1]
            CATE2 = book_info[2]
            JUM_1 = score[0]
            JUM_2 = score[1]
            val = USER, book_num,RAN, CATE, CATE2, JUM_1, JUM_2
            mycursor.execute(sql, val)
            mydb.commit()