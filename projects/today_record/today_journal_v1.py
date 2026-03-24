# 일기 기록 프로그램 (26-03-24)

import sqlite3

con = None
cur = None
row = None

date = ""
title = ""
content = ""

def write_diary():
    
    date = input("날짜(형식 : 2026-03-24) : ")
    title = input("제목 : ")
    content = input("내용을 입력하세요 : ")

    return date, title, content 

class DBmanager :
    
    def __init__(self) :

        self.con = sqlite3.connect("today_record.db")
        self.cur = self.con.cursor()
        self.cur.execute("""
                         create table if not exists today_diary
                         (
                         date text,
                         title text,
                         content text
                         )
                         """)

    def save_diary(self, date, title, content):
        self.cur.execute("insert into today_diary values(?,?,?)", (date, title, content))
        self.con.commit()

    def read_diary(self):
        self.cur.execute("select * from today_diary")
        self.row = self.cur.fetchone()
        
        if self.row == None :
            print("저장된 기록이 없습니다")
        else :
            while True :
            
                if self.row == None :
                    break
                
                self.data1 = self.row[0]
                self.data2 = self.row[1]
                self.data3 = self.row[2]
                print("%s" % self.data1)
                print("%s" % self.data2)
                print("%s" % self.data3)
                self.row = self.cur.fetchone()

    def search_diary(self) :
        
        while True :
            print("검색하기")
            print("1. 날짜")
            print("2. 제목")
            print("3. 내용")
            print("4. 메인 메뉴로 돌아가기")
            self.choice2 = input("메뉴 번호를 입력하세요 \n>>>")

            if self.choice2 == "1" :

                self.date_key = input("날짜를 입력하세요(형식 2026-03-24) : ") 
                self.cur.execute("select * from today_diary where date like ?", ('%'+ self.date_key + '%',))  ### 지피티 도움 execute는 (쿼리문, 값들(튜플)) => 값: (v1 , ) < 콤마로 표시해야 그냥 변수가 아닌 튜플로 인식
                self.row = self.cur.fetchone()
        
                if self.row == None :
                    print("저장된 기록이 없습니다")
                else :
                    while True :
                    
                        if self.row == None :
                            break
                        
                        self.data1 = self.row[0]
                        self.data2 = self.row[1]
                        self.data3 = self.row[2]
                        print("%s" % self.data1)
                        print("%s" % self.data2)
                        print("%s" % self.data3)
                        self.row = self.cur.fetchone()
            elif self.choice2 == "2" :

                self.title_key = input("제목에서 검색할 내용을 입력하세요 : ")
                self.cur.execute("select * from today_diary where title like ?", ('%'+ self.title_key + '%',))
                self.row = self.cur.fetchone()
        
                if self.row == None :
                    print("저장된 기록이 없습니다")
                else :
                    while True :
                    
                        if self.row == None :
                            break
                        
                        self.data1 = self.row[0]
                        self.data2 = self.row[1]
                        self.data3 = self.row[2]
                        print("%s" % self.data1)
                        print("%s" % self.data2)
                        print("%s" % self.data3)
                        self.row = self.cur.fetchone()
            elif self.choice2 == "3" :

                self.content_key = input("일기 내용에서 검색할 내용을 입력하세요 :")
                self.cur.execute("select * from today_diary where content like ?", ('%'+ self.content_key + '%',))    
                self.row = self.cur.fetchone()
        
                if self.row == None :
                    print("저장된 기록이 없습니다")
                else :
                    while True :
                    
                        if self.row == None :
                            break
                        
                        self.data1 = self.row[0]
                        self.data2 = self.row[1]
                        self.data3 = self.row[2]
                        print("%s" % self.data1)
                        print("%s" % self.data2)
                        print("%s" % self.data3)
                        self.row = self.cur.fetchone()

            elif self.choice2 == "4" :
                return                     # 호출했던 위치로 돌아감
class Menu :
    def __init__(self):
        print("DIARY")

    def select_menu(self, db) :
        
        while True :
            
            print("1. 일기 쓰기")
            print("2. 일기 읽기")
            print("3. 종료")
            
            self.choice = input("메뉴 번호를 입력하세요 \n >>>")
            
            if self.choice == "1" :

                date, title, content = write_diary()
                
                db.save_diary(date, title, content)

            elif self.choice == "2" :
                
                print("1. 검색하기")
                print("2. 전체 기록 보기")
                print("3. 메인 메뉴로 돌아가기")

                self.choice_1 = input("메뉴 번호를 입력하세요 \n >>>")

                if self.choice_1 == "1":
                    db.search_diary()

                elif self.choice_1 == "2" :
                    db.read_diary()
                
                elif self.choice_1 == "3" :
                    continue

                else :
                    print("메뉴 번호를 입력해주세요")
                    continue

            elif self.choice == "3" :
                print("일기장을 종료합니다")
                exit()
            
            else :
                print("메뉴 번호를 숫자로 입력해주세요")
                continue

db = DBmanager()
diary = Menu()
diary.select_menu(db)