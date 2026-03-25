import sqlite3
from datetime import datetime

import random

class RandomGame():
    
    def player_input(self,number):
        self.player =input("player%d의 이름을 입력하세요\n>>>"%number)
        
        
    def game1(self):
        
        self.random_int = random.randint(1,100)
        
        self.game_count = 0 
        
        print("%s님 1부터 100 사이의 정수를 입력해주세요" %self.player)
        
        while True:
            try:
                self.player_int = int(input(">>>"))
                if self.player_int < 1 or self.player_int > 100 :
                    print("1부터 100 사이의 정수를 입력해주세요")
                    continue
            except ValueError:
                print("정수만 입력해주세요")
                continue  
                
            self.game_count += 1 

            
            if self.player_int > self.random_int:
                if self.game_count > 5:
                    if self.player_int - self.random_int >= 5:
                        print("다운(5이상)")
                    else :
                        print("다운(5미만)")
                else:
                    print("다운")
            
            elif self.player_int < self.random_int:
                
                if self.game_count > 5:
                    if self.random_int - self.player_int >= 5:
                        print("업(5이상)")
                    else :
                        print("업(5미만)")
                else :
                    print("업")
                
            else :
                
                print("%s님 %d 번만에 맞혔습니다" %(self.player,self.game_count))
                break


    def game1outcome(self, player1, player2):

        self.game_round = 1
        
        while True:

            print(f'<<<<{self.game_round}라운드>>>>')
            player1.game1()
            player2.game1()

            if player1.game_count < player2.game_count:
                    print("%s 승" %player1.player)
                    break
            elif player1.game_count > player2.game_count:
                    print("%s 승" %player2.player)   
                    break
            elif player1.game_count == player2.game_count:
                    print("비겼습니다") 

                    self.game_round +=1   


    def game2(self, player1, player2):
        
        self.random_int = random.randint(1,100)
        
        self.turn = ""
        self.game_count = 0
        
        while True :
            if self.game_count % 2 == 0 :
                self.turn = player1
                print(f"{self.turn}님의 차례입니다. 1부터 100 사이의 정수를 입력해주세요")
            else :
                self.turn = player2
                print(f"{self.turn}님의 차례입니다. 1부터 100 사이의 정수를 입력해주세요")
            
            try:
                self.player_int = int(input(">>>"))
                if self.player_int < 1 or self.player_int > 100 :
                    print("1부터 100 사이의 정수를 입력해주세요")
                    continue
            except ValueError:
                print("정수만 입력해주세요")
                continue

            self.game_count += 1
            
            if self.player_int > self.random_int:
                if self.game_count > 5:
                    if self.player_int - self.random_int >= 5 :
                        print("다운(5 이상 차이납니다)")
                    elif self.player_int - self.random_int < 5 :
                        print("다운(5 미만 차이납니다)")
                else :
                    print("다운")
                
            elif self.player_int < self.random_int:
                if self.game_count > 5:
                    if self.random_int - self.player_int >= 5 :
                        print("업(5 이상 차이납니다)")
                    elif self.random_int - self.player_int < 5 :
                        print("업(5 미만 차이납니다)")
                else :
                    print("업")
                

            else :
                print(f"{self.turn} 승!, {self.game_count}번 만에 맞혔습니다")
                return self.turn, self.game_count
                

                
class GamePlay() :
    

    def __init__(self) :
        self.player1 = RandomGame()
        self.player2 = RandomGame()

    def player_nameing(self):
        self.player1.player_input(1)
        self.player2.player_input(2)

    def game1play(self) :
        
        game1play = RandomGame()
        game1play.game1outcome(self.player1, self.player2)

        database.game1record(self.player1.player, self.player1.game_count)
        database.game1record(self.player2.player, self.player2.game_count)

    def game2play(self) :
        
        game2play = RandomGame()
        turn, game_count = game2play.game2(self.player1.player, self.player2.player)

        database.game2record(turn, game_count)


class DatabaseManager() :
        
    con, cur = None, None

    data1, data2, data3 = "", "", ""

    row = None
    
    def __init__(self):   
        self.con = sqlite3.connect("random_game_score.db")
        self.cur = self.con.cursor()
        self.cur.execute("create table if not exists gameRecordTable (play_date char(10), player_name char(15), try_count number)")

    def game1record(self, player, game_count):  
        
        today = datetime.today().strftime("%Y-%m-%d")

        self.cur.execute("insert into gameRecordTable values(?, ?, ?)", (today, player, game_count))

        self.con.commit()

    def game2record(self, player, game_count):
        
        today = datetime.today().strftime("%Y-%m-%d")
        self.cur.execute("insert into gameRecordTable values(?, ?, ?)", (today, player, game_count))

        self.con.commit()

    def record_print(self):

        self.cur.execute("select * from gameRecordTable")


        print("   날짜       플레이어 이름    시도횟수")
        print("=======================================")

        row = self.cur.fetchone()
        if row == None :    
            print("기록이 없습니다")

        else :
            while True:
            
                if row == None:
                    break
                data1 = row[0]
                data2 = row[1]
                data3 = row[2]

                print("%10s\t%10s\t%3d" % (data1, data2, data3))
                row = self.cur.fetchone()

        

    def max_record(self):
    
        self.cur.execute("select * from gameRecordTable where try_count = (select min(try_count) from gameRecordTable)")
        print("<<<최고기록>>>")
        print(f'플레이어 이름\t 시도횟수')

        max_data = self.cur.fetchone()

        if max_data == None :    
            print("기록이 없습니다")  

        else :
            while True :
                
                # max_data = cur.fetchone() => 여기에 넣으면 첫 번째 줄 데이터는 날려버리고 두 번째 줄 불러와짐
                if max_data != None :

                    max_name = max_data[1]
                    max_score = max_data[2]
                        
                    print("%8s\t%5d"%(max_name,max_score) )
                else :
                    break    
            
                max_data = self.cur.fetchone() # 앞에 첫 줄 불러왔기 때문에 다음 줄 불러오기
    def delete_record(self):
        
        self.cur.execute("delete from gameRecordTable")
        self.con.commit()
        
        print("기록이 삭제되었습니다")    

class GameMenu(GamePlay) :
    choice = ""

    def __init__ (self):
        
        super().__init__()

        while True :

            print("<<<랜덤 숫자 맞히기 게임>>>")
            print("1. 게임 선택")
            print("2. 기록 확인")
            print("3. 종     료")
            print("원하는 메뉴의 번호를 입력해주세요")

            self.choice = input(">>>")
            
            if self.choice == "1" :
                while True :
                
                    print("게임 선택")
                    print("1. 기록 경쟁 게임")
                    print("2. 누가 먼저 맞혀볼까용")
                    print("3. 메인 메뉴로 돌아가기")
                    
                    choice_1 = input(">>>")
                    if choice_1 == "1" :
                        
                        self.player_nameing()
                        self.game1play()

                    elif choice_1 == "2" :

                        self.player_nameing()
                        self.game2play()


                    elif choice_1 == "3" :
                        break

                    else :
                        print("잘못 입력하셨습니다. 메뉴 번호를 입력해주세요")
            
            elif self.choice == "2" :
                
                while True :
                    print("1. 최고 기록 확인")
                    print("2. 전체 기록 확인")
                    print("3. 기록 삭제")
                    print("4. 메인 메뉴로 돌아가기")
                    
                    choice_2 = input(">>>")
                    if choice_2 == "1" :
                        
                        database.max_record()

                    elif choice_2 == "2" :

                        database.record_print()

                    elif choice_2 == "3" :
                        database.delete_record()

                    elif choice_2 == "4" :
                        break

                    else :
                        print("잘못 입력하셨습니다. 메뉴 번호를 입력해주세요")    

            elif self.choice == "3" :
                print("게임을 종료합니다")
                exit()

            else :
                print("잘못 입력하셨습니다. 메뉴 번호를 입력해주세요")


database = DatabaseManager()

game = GameMenu()