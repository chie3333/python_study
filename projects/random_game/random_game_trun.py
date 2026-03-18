#턴제 랜덤 숫자 맞히기 게임 260318

import random

def game(v1, v2):
    random_int = random.randint(1,100)
    game_count = 0
    

    while True :
        if game_count % 2 == 0 :
            turn = v1
            print(f"{v1}님의 차례입니다. 1부터 100 사이의 정수를 입력해주세요")
        else :
            turn = v2
            print(f"{v2}님의 차례입니다. 1부터 100 사이의 정수를 입력해주세요")
        
        try:
            player_int = int(input(">>>"))
            if player_int < 1 or player_int > 100 :
                print("1부터 100 사이의 정수를 입력해주세요")
                continue
        except ValueError:
            print("정수만 입력해주세요")
            continue

        game_count += 1
        
        if player_int > random_int:
            if game_count >= 5:
                if player_int - random_int >= 5 :
                    print("다운(5 이상 차이납니다)")
                elif player_int - random_int < 5 :
                    print("다운(5 미만 차이납니다)")
            else :
                print("다운")
            
        elif player_int < random_int:
            if game_count >= 5:
                if random_int - player_int >= 5 :
                    print("업(5 이상 차이납니다)")
                elif random_int - player_int < 5 :
                    print("업(5 미만 차이납니다)")
            else :
                print("업")
            

        else :
            print(f"{turn} 승!, {game_count}번 만에 맞혔습니다")
            break

player1 = input("player1의 이름을 입력하세요 \n >>>")
player2 = input("player2의 이름을 입력하세요 \n >>>")

game(player1, player2)