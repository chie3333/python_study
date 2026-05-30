###투자 자산 세무조정
import sqlite3

import pandas as pd

con = None
cur = None


stock_code = ""
asset_name = ""
market_type = ""
accounting_classification = ""

quantity = None
price_per_share = None
trade_date = ""
event_type = ""

note = None




con = sqlite3.connect("tax_adjustment.db")
cur = con.cursor()
cur.execute("PRAGMA foreign_keys = ON;")

# cur.execute("DROP TABLE IF EXISTS investment_asset")
# cur.execute("DROP TABLE IF EXISTS trade_event")

cur.execute("""
            create table if not exists investment_asset
            (asset_id integer PRIMARY KEY AUTOINCREMENT,
            stock_code text NOT NULL,
            asset_name text NOT NULL,
            market_type text NOT NULL,
            accounting_classification text CHECK(accounting_classification IN ('FVOCI', 'FVTPL')),
            FOREIGN KEY(stock_code) REFERENCES stock_list(stock_code),
            UNIQUE(stock_code, accounting_classification)
            )
            """)

cur.execute("""
            create table if not exists trade_event
            (
            trade_id integer PRIMARY KEY AUTOINCREMENT,
            asset_id integer NOT NULL, 
            trade_date text NOT NULL CHECK(trade_date LIKE '____-__-__'),
            event_type text NOT NULL CHECK(event_type IN('BUY','SELL','DIVIDEND')),
            quantity integer CHECK(quantity >= 0),
            price_per_share integer CHECK(price_per_share >= 0),
            trade_amount integer CHECK(trade_amount >= 0),
            note text,
            FOREIGN KEY(asset_id) REFERENCES investment_asset(asset_id)
            )
            """)






while True:
    print("1. 데이터 입력\n2. 입력된 데이터 보기")

    menu = input("메뉴번호를 입력하세요\n>>>")
    if menu == "1" :

        while True:
            
            stock_code = ""
            asset_name = ""
            market_type = ""
            accounting_classification = ""

            quantity = None
            price_per_share = None
            trade_date = ""
            event_type = ""

            note = ""

            trade_date = input("거래 날짜를 입력하세요(YYYY-MM-DD) : ")

            if trade_date == "" :
                break

            event_type = input("거래 종류(BUY, SELL, DIVIDEND) : ")
            
            while True :
            
                stock_code = input("종목코드 입력: ")
                
                if stock_code == "" :
                    break

                cur.execute("""
                SELECT asset_name, market_type
                FROM stock_list
                WHERE stock_code = ?
                """, (stock_code,))

                result = cur.fetchone()
                

                if result is None :
                    print("존재하지 않는 종목코드 입니다.")
                    continue
            
                else :
                    


                    if event_type == "BUY" :
                        
                        
                        asset_name, market_type = result
                        accounting_classification = input("분류(FVTPL, FVOCI) : ")

                        cur.execute("""
                                    insert OR IGNORE INTO investment_asset 
                                    (stock_code, asset_name, market_type, accounting_classification)
                                    values(?,?,?,?)""", 
                                    (stock_code, asset_name, market_type, accounting_classification)
                                    )
                        
                        cur.execute("""
                        SELECT asset_id 
                        FROM investment_asset
                        WHERE stock_code = ?
                        AND accounting_classification = ?
                        """, (stock_code, accounting_classification))
                        
                        result = cur.fetchone()   

                        if result is None:
                            print("자산 생성 실패")
                            continue    

                        else :    
                            asset_id = result[0] 

                            quantity = int(input("주식 수 입력 : "))
                            price_per_share = int(input("1주당 주가 입력 : "))
                            trade_amount = quantity*price_per_share
                            note = input("적요 : ")

                            if note == "" :
                                note = None

                            cur.execute("""
                                    insert into trade_event
                                    (asset_id, trade_date, event_type, quantity, price_per_share, trade_amount, note) 
                                    values(?,?,?,?,?,?,?)""", 
                                    (asset_id, trade_date, event_type, quantity, price_per_share, trade_amount, note)
                                    )
                            

                            
                    elif event_type == 'SELL' :

                        stock_code = input("종목코드 입력: ")
                    
                
                        cur.execute("""
                        SELECT * 
                        FROM investment_asset
                        WHERE stock_code = ?
                        """, (stock_code,))

                        result = cur.fetchone()

                        if result is None :
                            print("보유하고 있지 않은 종목코드 입니다.")
                            continue
            

                        quantity = int(input("주식 수 입력 : "))
                        price_per_share = int(input("1주당 주가 입력 : "))
                        trade_amount = quantity*price_per_share
                        note = input("적요 : ")

                        if note == "" :
                            note = None
                        cur.execute("""
                                insert into trade_event
                                (stock_code, trade_date, event_type, quantity, price_per_share, trade_amount, note) 
                                values(?,?,?,?,?,?,?)""", 
                                (stock_code, trade_date, event_type, quantity, price_per_share, trade_amount, note)
                                )
                            
                    
                    elif event_type == "DIVIDEND" :

                        stock_code = input("종목코드 입력: ")
                    
                
                        cur.execute("""
                        SELECT * 
                        FROM investment_asset
                        WHERE stock_code = ?
                        """, (stock_code,))

                        result = cur.fetchone()

                        if result is None :
                            print("보유하고 있지 않은 종목코드 입니다.")
                            continue

                        trade_amount = int(input("배당금 입력 :"))
                        note = input("적요 : ")

                        if note == "" :
                            note = None
                        cur.execute("""
                                insert into trade_event
                                (stock_code, trade_date, event_type, trade_amount, note) 
                                values(?,?,?,?,?)""", 
                                (stock_code, trade_date, event_type, trade_amount, note)
                                )


                    
                    
                    else :
                        print("잘못 입력하셨습니다. 다시 입력해주세요.")
                        continue
                        

                
                
                
            con.commit()
            
            
    elif menu == "2" :
        print("1.보유 주식 확인\n2.거래 내역 확인")
                            
        menu2 = input("메뉴 번호를 입력하세요 : ")

        if menu2 == "1" :  
            cur.execute("select * from investment_asset")
            
            print("종목코드   이름\t\t\t\t시장구분       분류")
            print("-------------------------------------------------------")
            
            while True:
                row = cur.fetchone()
                if row == None:
                    break

                data1 = row[0]
                data2 = row[1]
                data3 = row[2]


                
                print(f"{data1:<10} {data2:<20}\t{data3:<10}")
        
        elif menu2 == "2" :
                            
            cur.execute("select * from trade_event")
            
            
            rows = cur.fetchall()

            for row in rows :

                print(row)

    elif menu == "" :
        break

    else :
        print("메뉴번호를 다시 입력해주세요")
        continue


