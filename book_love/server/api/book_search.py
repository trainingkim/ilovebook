#책 검색 수행
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

class Book_Search(object):
    def __init__(self):
        self.mydb = None #DB
        self.mycursor = None #DB_Cursor

        self.mydb = mysql.connector.connect(#Database 연결
        host="localhost",
        user="root",
        password="1234",
        database="book"
        )
    def Get_Book_Info_Search(self, book_name): # 검색어를통해 책 정보를 가져옴
        sql = f"select * from b_info where B_Name LIKE \"%{book_name}%\""
        self.mycursor.execute(sql)
        book_info = self.mycursor.fetchall()
        if not book_name:
            return None
        return book_info


if __name__ == "__main__": #검색 Test
    bl = Book_Loader()
    print(bl.Get_Book_Info_Search('공주'))
    # print(bl.Get__List())
    