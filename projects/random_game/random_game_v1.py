#랜덤 숫자 맞추기 게임 260317
import random


#print(random_int)

game_count1 = 0

game_count2 = 0

game_round = 1

player1 =input("player1의 이름을 입력하세요")

player2 =input("player2의 이름을 입력하세요")

    

print("%s님부터 시작합니다" %player1)

def game():
    
    random_int1 = random.randint(1,100)
    random_int2 = random.randint(1,100)
    
    global game_count1 

    global game_count2

    game_count1 = 0 #게임할때마다 갱신해줘야함

    game_count2 = 0
    
    print("%s님 1부터 100 사이의 정수를 입력해주세요" %player1)
    while True:
            try:
                player1_int = int(input(">>>"))
                if player1_int < 1 or player1_int > 100 :
                    print("1부터 100 사이의 정수를 입력해주세요")
                    continue
            except ValueError:
                print("정수만 입력해주세요")
                continue     
                
            game_count1 += 1    
            if player1_int > random_int1:
                print("다운")
                
            elif player1_int < random_int1:
                print("업")
                
            elif player1_int == random_int1:
                
                print("%s님 %d 번만에 맞습니다" %(player1,game_count1))
                break
    
        
    print("%s님 1부터 100 사이의 정수를 입력해주세요" %player2)    
    while True:
        try:
                
                player2_int = int(input(">>>" ))
                if player2_int < 1 or player2_int > 100 :
                    print("1부터 100 사이의 정수를 입력해주세요")
                    continue
        except ValueError :
                print("정수만 입력해주세요")
                continue
                
        game_count2 += 1        
        if player2_int > random_int2:
                    print("다운")
                    
        elif player2_int < random_int2:
                    print("업")
                    
        elif player2_int == random_int2:
                    print("%s님 %d 번만에 맞혔습니다" %(player2, game_count2))
                    break
                      

while True:
    game()
    if game_count1 < game_count2:
            print("%s 승" %player1)
            break
    elif game_count1 > game_count2:
            print("%s 승" %player2)   
            break
    elif game_count1 == game_count2:
            print("비겼습니다") 
            game_round +=1                  
            print("round %d" %game_round)  