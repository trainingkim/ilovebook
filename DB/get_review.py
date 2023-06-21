#책 리뷰를 분석
import mysql.connector
import json, os
from collections import defaultdict

def get_category():#카테고리를 받아오는 함수
    return_value = defaultdict(list)
    for file_name in list(os.walk(r'C:\Users\train\Desktop\ilovebook\file'))[0][2]:
        return_value[file_name.split('-')[0]].append(file_name.split('-')[1].replace('.xls',''))
    return return_value

def category_get_reviews(cate1, cate2 = None): #카테고리의 리뷰를 MySQL에서 가져오는 함수
    if cate2:
        sql = 'select * from review where CATE=%s and CATE2 = %s'
        mycursor.execute(sql, (cate1,cate2))
    else:
        sql = 'select * from review where CATE=%s'
        mycursor.execute(sql, (cate1,))
    print(len(mycursor.fetchall()))

mydb = mysql.connector.connect(#Database 연결
   host="localhost",
   user="root",
   password="1234",
   database="book"
 )
mycursor = mydb.cursor() #mysql
category_get_reviews("초등참고서")

#1. Cate 선택 (완)
#2. 동일한 Cate 책 중 리뷰를 작성한 사람 리스트를 얻어 온다. (완)
#3. 얻어온 리스트 중 작성한 리뷰에서 동일한 카테고리가 많은 사람을 5명~10명을 뽑는다.
#4. 해당 사람들이 작성한 리뷰에서 평점이 제일 좋은 책을 추천한다. 특이 케이스. 리뷰가 없는 경우는 스킵-> 제일 랭크가 높은거 1개씩 추천한다.