#Flask 서버 정보
from flask import Flask
from flask import render_template, url_for, request

from api.book_recommend import *

import json
import mysql.connector
from collections import defaultdict

# +---------+-----------+------+-----+---------+-------+
# | Field   | Type      | Null | Key | Default | Extra |
# +---------+-----------+------+-----+---------+-------+
# | B_Num   | int(11)   | YES  |     | NULL    |       |
# | B_Pri   | int(11)   | YES  |     | NULL    |       |
# | B_Name  | char(100) | YES  |     | NULL    |       |
# | B_Auth  | char(255) | YES  |     | NULL    |       |
# | B_Pub   | char(100) | YES  |     | NULL    |       |
# | B_CATE  | char(100) | YES  |     | NULL    |       |
# | B_CATE2 | char(100) | YES  |     | NULL    |       |
# | B_CATE3 | char(100) | YES  |     | NULL    |       |
# | B_RAN   | int(11)   | YES  |     | NULL    |       |
# | B_AVE   | float     | YES  |     | NULL    |       |
# | B_NUM_1 | float     | YES  |     | NULL    |       |
# | B_NUM_2 | float     | YES  |     | NULL    |       |
# +---------+-----------+------+-----+---------+-------+

class Book_Search(object): #DB <-> 파이썬 통신 시 필요한 함수들만 빠르게 사용할 수 있도록 만들어둔 임시 클래스
    def __init__(self):
        self.mydb = None #DB
        self.mycursor = None #DB_Cursor

        self.mydb = mysql.connector.connect(#Database 연결
        host="localhost",
        user="root",
        password="1234",
        database="book"
        )
        self.mycursor = self.mydb.cursor() #mysql
    def Get_Book_Info_Search(self, book_name): #책 이름을 기준으로 책 정보를 가져오는 코드
        sql = f"select * from b_info_1 where B_Name LIKE \"%{book_name}%\""
        self.mycursor.execute(sql)
        book_info = self.mycursor.fetchall()
        if not book_name:
            return []
        return book_info
    def Get_Rank_Top_Pick(self, cate_list): #카테고리가 주어졌을때 해당 카테고리를 기준으로 Rank과 평점으로 정렬한 뒤 리턴하는 코드
        temp = []
        for cate in cate_list:
            sql = f"select * from b_info_1 where B_CATE=\"{cate}\" order by B_Ran asc, B_AVE desc limit 1"
            self.mycursor.execute(sql)
            book_info = self.mycursor.fetchall()
            temp.extend(book_info)
        return temp
    def Get_Num_Pick(self, book_list): #책 번호를 기준으로 검색해서 리턴하는 코드
        temp = []
        for book in book_list:
            sql = f"select * from b_info_1 where B_NUM=\"{book}\" limit 1"
            self.mycursor.execute(sql)
            book_info = self.mycursor.fetchall()
            temp.extend(book_info)
        return temp
    def Get_Rank_Top_Cate_Pick(self, cate): #카테고리가 주어졌을때 5위 아래의 것들만 출력하는 코드
        sql = f"select * from b_info_1 where B_CATE=\"{cate}\" AND B_RAN < 5 order by B_RAN ASC"
        self.mycursor.execute(sql)
        book_info = self.mycursor.fetchall()
        return book_info
    def Get_Rank_Top_Cate2_Pick(self, cate): #세부 카테고리가 주어졌을때 랭킹을 기준으로 정렬하는 코드
        sql = f"select * from b_info_1 where B_CATE2=\"{cate}\" order by B_RAN ASC"
        self.mycursor.execute(sql)
        book_info = self.mycursor.fetchall()
        return book_info
    def Get_Rank_Top_Cate3_Pick(self, cate): #세부 카테고리가 주어졌을때 랭킹을 기준으로 정렬하는 코드
        sql = f"select * from b_info_1 where B_CATE3=\"{cate}\" order by B_RAN ASC"
        self.mycursor.execute(sql)
        book_info = self.mycursor.fetchall()
        return book_info
    def Get_Detail_Cate2_Dcit(self, cate_list): #카테고리 리스트를 기준으로 세부 카테고리 딕셔너리를 리턴하는 코드
        return_value = dict()
        for cate_item in cate_list:
            return_value[cate_item] = {}
            for cate2_item in cate_list[cate_item]:
                sql = "select distinct B_Cate3 from b_info_1 where b_cate2 = '{}'".format(cate2_item)
                self.mycursor.execute(sql)
                book_info = []
                for i in self.mycursor.fetchall():
                    if i[0] is not None: book_info.append(i[0])
                return_value[cate_item][cate2_item] = book_info
        return return_value
    def Get_Detail_Cate_Dcit(self, cate_list): #카테고리 리스트를 기준으로 세부 카테고리 딕셔너리를 리턴하는 코드
        return_value = dict()
        for cate in cate_list:
            sql = "select distinct B_Cate2 from b_info_1 where b_cate = '{}'".format(cate)
            self.mycursor.execute(sql)
            book_info = [i[0] for i in self.mycursor.fetchall()]
            return_value[cate] = book_info
        return return_value
    def Get_Category1_list(self):
        sql = "select distinct B_Cate from b_info_1"
        self.mycursor.execute(sql)
        book_info = [i[0] for i in self.mycursor.fetchall()]
        return book_info

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False #JSON data ASCII Encoding Error Fix
bs = Book_Search()
# cate_list = ['대학교재', '청소년', '여행', '만화,라이트노벨', '자기계발', '수험서 자격증', '자연과학', '잡지', 'IT 모바일', '전집', '소설,시,희곡', '국어 외국어 사전', '예술', '건강 취미', '에세이', '초등참고서', '인문', '어린이', '경제 경영', '가정 살림', '사회 정치', '인물', '중고등참고서', '유아', '종교', '역사']
cate_list = bs.Get_Category1_list()
cate_detail_dict = bs.Get_Detail_Cate_Dcit(cate_list) #ex) cate_detail_dict['대학교재'] = 대학교재의 sub 카테고리 모두 출력
cate_detail2_dict = bs.Get_Detail_Cate2_Dcit(cate_detail_dict) #ex) cate_detail_dict['대학교재'] = 대학교재의 sub 카테고리 모두 출력

@app.route('/')
def main():
    book_datas = bs.Get_Rank_Top_Pick(cate_list)
    return render_template('index.html', book_cate_list=cate_list, book_datas=book_datas)

@app.route('/book_search', methods=['GET'])
def book_search():
    parameter = request.args.to_dict()
    if not parameter.get('book_name', None):
        return "input data check"
    book_name = parameter['book_name']
    book_datas = bs.Get_Book_Info_Search(book_name)
    return render_template('book_search.html', book_datas=book_datas, book_cate_list=cate_list)

@app.route('/cate/<int:cate_index>')
def cate_view(cate_index):
    cate_select = cate_list[cate_index-1]
    cate_select_detail = cate_detail_dict[cate_select]
    book_datas = bs.Get_Rank_Top_Cate_Pick(cate_select)
    return render_template('detail.html', cate_index=cate_index, cate_select=cate_select,cate_select_detail=cate_select_detail, book_cate_list=cate_list, book_datas = book_datas)

@app.route('/cate/<int:cate_index>/<int:detail_index>')
def cate_detail_view(cate_index, detail_index):
    cate_select = cate_list[cate_index-1]
    cate_select_detail = cate_detail_dict[cate_select]
    cate_select_detail2 = cate_detail2_dict[cate_select][cate_select_detail[detail_index-1]]
    cate_select = cate_select_detail[detail_index-1]
    book_datas = bs.Get_Rank_Top_Cate2_Pick(cate_select)
    return render_template('detail.html', cate_index=cate_index, cate_detail_index=detail_index, cate_select=cate_select,cate_select_detail=cate_select_detail, cate_select_detail2=cate_select_detail2, book_cate_list=cate_list, book_datas = book_datas)

@app.route('/cate/<int:cate_index>/<int:detail_index>/<int:detail2_index>')
def cate_detail2_view(cate_index, detail_index, detail2_index):
    cate_select = cate_list[cate_index-1]
    cate_select_detail = cate_detail_dict[cate_select]
    cate_select_detail2 = cate_detail2_dict[cate_select][cate_select_detail[detail_index-1]]
    cate_select = cate_select_detail2[detail2_index-1]
    book_datas = bs.Get_Rank_Top_Cate3_Pick(cate_select)
    return render_template('detail.html', cate_index=cate_index, cate_detail_index=detail_index, cate_select=cate_select, cate_select_detail=cate_select_detail, cate_select_detail2=cate_select_detail2, book_cate_list=cate_list, book_datas = book_datas)

@app.route('/book_like')
def book_like():
    book_datas = []
    book_list = request.cookies.get('book_list')
    if book_list:
        book_list = json.loads(book_list)
        book_datas = bs.Get_Num_Pick(book_list)
    return render_template('book_like.html', book_datas=book_datas, book_cate_list=cate_list)

@app.route('/book_recommend')
def book_recommend():
    book_datas = []
    book_list = request.cookies.get('book_list')
    if book_list:
        book_list = json.loads(book_list)
        br = Book_Recommend()
        br.Book_Select(book_list)
        print("BOOK LIST", book_list)
        fd = open("debug.txt", 'w', encoding='utf-8')
        print(br.cate1_score, file=fd, end = "\n\n\n")
        print(br.cate2_score, file=fd, end = "\n\n\n")
        print(br.cate3_score, file=fd, end = "\n\n\n")
        fd.close()
        book_most = br.Score_Calc()
        book_datas = br.Book_Processing(book_most)
        
    return render_template('book_recommend.html', book_datas=book_datas, book_cate_list=cate_list)

if __name__ == "__main__":
    # print(bs.Get_Rank_Top_Pick(cate_list)[])
    # print(cate_detail_dict['청소년'])
    app.debug = True
    app.run()

    # select B_Name, B_CATE, B_CATE2 from b_info where B_Name = "어린 왕자";