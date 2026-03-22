import sqlite3
from datetime import datetime

import random


con, cur = None, None

data1, data2, data3 = "", "", ""

row = None

class RandomGame:
    def player_input(self):
        self.player =input("player의 이름을 입력하세요\n>>>")
        
        
    def game(self):
        
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

player1 = RandomGame()
player2 = RandomGame()

game_round = 1

player1.player_input()
player2.player_input()
while True:
    
    print(f'<<<<{game_round}라운드>>>>')
    player1.game()
    player2.game()

    if player1.game_count < player2.game_count:
            print("%s 승" %player1.player)
            break
    elif player1.game_count > player2.game_count:
            print("%s 승" %player2.player)   
            break
    elif player1.game_count == player2.game_count:
            print("비겼습니다") 

            game_round +=1     


con = sqlite3.connect("random_game_score.db")
cur = con.cursor()

cur.execute("create table if not exists recordTable (play_date char(10), player_name char(15), try_count number, round char)")

today = datetime.today().strftime("%Y-%m-%d")

cur.execute("insert into recordTable values(?, ?, ?, ?)", (today, player1.player, player1.game_count, game_round))
cur.execute("insert into recordTable values(?, ?, ?, ?)", (today, player2.player, player2.game_count, game_round))
con.commit()

cur.execute("select * from recordTable")


print("    날짜    플레이어 이름    시도횟수")
print("===================================")

while True:
    row = cur.fetchone()
    if row == None:
        break
    data1 = row[0]
    data2 = row[1]
    data3 = row[2]

    print(f'{data1}\t{data2}\t\t{data3}')

con.close()