#책 추천 알고리즘
from api.book_load import Book_Loader
from collections import Counter, defaultdict

# self.mydb = None #DB
# self.mycursor = None #DB_Cursor
# self.book_info = None #모든 책 정보 Dict
# self.book_cate1_list = set() #모든 세부 카테고리 리스트
# self.book_cate2_list = set() #큰 카테고리 리스트
# self.book_name_list = set() #모든 책 리스트
# self.book_name_info = defaultdict(list)

class Book_Recommend(Book_Loader):
    def __init__(self):
        super().__init__()
        self.cate2_score = Counter(self.book_cate2_list) #모든 카테고리별 점수
        # print(self.cate1_score)
        self.cate1_score = Counter(self.book_cate1_list)#세부 카테고리 점수
        self.book_score = Counter(self.book_name_info.keys())
        self.book_cate = dict() #책 세부카테고리:큰 카테고리
        # self.book_name_cate2_list = defaultdict(list)
        # self.book_name_cate_list = dict()
    def Book_Select(self, book_name_list): #책을 선택해서 해당 책의 카테고리와 서브카테고리를 가지고 사용자가 선호하는 카테고리를 점수로 계산한다.
        for book_name in book_name_list:
            book_info_list = self.Get_Book_Info_Search(book_name) #책 정보
            if not book_info_list:
                continue
            temp_cate1 = list()
            for book_info in book_info_list:
                self.book_cate[book_info[6]] = book_info[5] #18줄
                self.cate2_score[book_info[6]] += 1 #세부카테고리에 점수 추가
                if book_info[5] in temp_cate1: #이미 추가된 카테고리라면(서브 카테3리가 다른 중복된 책이 존재) 카테고리에는 가중치 부여 X
                    continue
                # self.book_name_cate_list[book_info[2]] = book_info[5]
                self.cate1_score[book_info[5]] += 1 #새로운 책의 카테고리라면 가중치 부여
                temp_cate1.append(book_info[5])

        # for book_name, cate_list in self.book_name_cate2_list.items():
        #     max_ = [0, None]
        #     for cate in cate_list:
        #         if self.cate2_score[cate] > max_[0]:
        #             max_ = [self.cate2_score[cate], cate]
        #     print(book_name, max_)
        #     self.book_score[book_name] *= self.[max_[1]] * self.cate2_score[self.book_name_cate_list[book_name]]
        # print(self.book_score)
    def Find_Cate_Selected(self): #점수가 1 이상인 것들 (선택하지 않은 카테고리 제외 함수)
        cate_list = set()
        for cate, score in self.cate1_score.items():
            if score > 1:
                cate_list.add(cate)
        return list(cate_list)
    def Score_Calc(self):
        # 고려 사항
        # 1. cate1
        # 2. cate2
        # 3. rank
        # 4. review
        # 5. review_relationship

        '''
            1. 세부카테고리 * 큰카테고리 * ranking에 대한 가중치
        '''
        for cate2, cate1 in self.book_cate.items():
            self.cate2_score[cate2] *= self.cate1_score[cate1]
        cate1_list = self.Find_Cate_Selected()
        book_list = list()
        for cate1 in cate1_list:
            sql = f"select * from b_info where B_CATE = '{cate1}'"
            self.mycursor.execute(sql)
            book_list.extend(self.mycursor.fetchall())

        rank_temp = {i:11-i for i in range(1,11)}

        for book in book_list:
            self.book_score[book[2]] *= self.cate2_score[book[6]] * rank_temp[book[7]]
        return self.book_score.most_common(50)
    def Book_Processing(self, book_most):
        temp = []
        for book_name, book_count in book_most:
            sql = f"select * from b_info where B_NAME ='{book_name}' limit 1"
            self.mycursor.execute(sql)
            book_info = self.mycursor.fetchall()
            temp.extend(book_info)
        return temp

if __name__ == "__main__":
    br = Book_Recommend()
    print(br.Book_Select(['어린 왕자', '스즈메의 문단속', '오늘 밤', '정보 보안 개론', '네트워크 개론']))
    print(br.cate1_score)
    print(br.Score_Calc())
    print(list(br.cate1_score.keys()))
    print(br.book_cate)
    print(br.cate2_score)