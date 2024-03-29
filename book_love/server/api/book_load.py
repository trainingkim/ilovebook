#DB Controller
import mysql.connector #MySQL DB연동
from collections import defaultdict #dict

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
# | B_RAN   | int(11)   | YES  |     | NULL    |       |
# | B_AVE   | float     | YES  |     | NULL    |       |
# | B_NUM_1 | float     | YES  |     | NULL    |       |
# | B_NUM_2 | float     | YES  |     | NULL    |       |
# +---------+-----------+------+-----+---------+-------+

class Book_Loader(object):
    def __init__(self):
        self.mydb = None #DB
        self.mycursor = None #DB_Cursor
        self.book_info = None #모든 책 정보 Dict
        self.book_cate1_list = set() #모든 세부 카테고리 리스트
        self.book_cate2_list = set() #모든 카테고리 리스트
        self.book_cate3_list = set() #모든 카테고리 세부-세부 리스트
        self.book_name_list = set() #모든 책 리스트
        self.book_name_info = defaultdict(list)

        self.mydb = mysql.connector.connect(#Database 연결
        host="localhost",
        user="root",
        password="1234",
        database="book"
        )
        self.mycursor = self.mydb.cursor() #mysql
        self.book_info = self.Get_Book_All_Load()
        
        self.Book_Info_Processing() #책 정보와 카테고리 리스트를 set에 추가

    def Book_Info_Processing(self):
        self.book_cate1_list = set()
        self.book_cate2_list = set()
        self.book_name_list = set()
        for b_info in self.book_info['book_info']:
            self.book_name_list.add(b_info[2])
            self.book_cate1_list.add(b_info[5])
            self.book_cate2_list.add(b_info[6])
            self.book_cate3_list.add(b_info[7])
            self.book_name_info[b_info[2]].append(b_info)
        self.book_name_list = list(self.book_name_list)
        self.book_cate1_list = list(self.book_cate1_list)
        self.book_cate2_list = list(self.book_cate2_list)
        self.book_cate3_list = list(self.book_cate3_list)
        
    def Make_Where(self, sql, condition):
        # sql += " where "
        # for i in condition:
        pass
    def Get_Book_All_Load(self): #DB로부터 모든 책 정보 불러오기
        sql = "select * from b_info_1"
        self.mycursor.execute(sql)
        return_value = {}
        book_info = self.mycursor.fetchall()
        return_value['book_info'] = book_info
        return_value['count'] = len(book_info)
        return return_value
    def Get_Cate_List(self, version = None): #카테고리 리스트를 반환
        if version == 1:
            return self.book_cate1_list
        if version == 2:
            return self.book_cate2_list
        return self.book_cate1_list, self.book_cate2_list
    def Get_Name_List(self): #책 리스트 반환
        return self.book_name_list
    def Get_Book_Info_Search(self, book_name): #책 이름으로 책정보 검색 후 반환
        sql = f"select B_Name from b_info_1 where B_Num LIKE \"%{book_name}%\""
        self.mycursor.execute(sql)
        book_name = self.mycursor.fetchall()
        # print(sql, book_name)
        if not book_name:
            return None
        return self.book_name_info[book_name[0][0]]
    # def Get_Book_Load(self, filter):
    #     sql = "select * from b_info where" + filter
    #     self.mycursor.execute(sql)
    #     return_value = {}
    #     book_info = self.mycursor.fetchall()
    #     return_value['book_info'] = book_info
    #     return_value['count'] = len(book_info)
    #     return return_value
if __name__ == "__main__": #검색 Test
    bl = Book_Loader()
    print(bl.Get_Book_Info_Search('공주'))
    # print(bl.Get__List())
    