import sqlite3

import pandas as pd

con = None
cur = None


stock_code = ""
asset_name = ""
market_type = ""
accounting_classification = ""

con = sqlite3.connect("tax_adjustment.db")
cur = con.cursor()
cur.execute("PRAGMA foreign_keys = ON;")
cur.execute("""
            create table if not exists investment_asset
            (
            stock_code text PRIMARY KEY,
            asset_name text NOT NULL,
            market_type text NOT NULL,
            accounting_classification text NOT NULL CHECK(accounting_classification IN ('FVOCI', 'FVTPL')) NOT NULL
            FOREIGN KEY(stock_code) REFERENCES stock_list(stock_code)
            )
            """)

print("1. 데이터 입력\n2. 입력된 데이터 보기")



while True:
    menu = input("메뉴번호를 입력하세요\n>>>")
    if menu == "1" :
        while True:
            stock_code = input("종목코드 입력: ")
            
            if stock_code == "" :
                break
            
            else :
                cur.execute("""
                SELECT asset_name, market_type
                FROM stock_list
                WHERE stock_code = ?
                """, (stock_code,))

                result = cur.fetchone()

                if result is None :
                    print("존재하지 않는 종목코드 입니다.")
                    continue

                asset_name, market_type = result

                accounting_classification = input("분류(FVTPL, FVOCI) : ")

                cur.execute("insert into investment_asset values(?,?,?,?)", (stock_code, asset_name, market_type, accounting_classification ))
                con.commit()
            
            

            
    
    elif menu == "2" :

        cur.execute("""
                    select * from investment_asset
                    """)
        
        print("종목코드   이름\t\t\t\t시장구분       분류")
        print("-------------------------------------------------------")
        
        while True:
            row = cur.fetchone()
            if row == None:
                break

            data1 = row[0]
            data2 = row[1]
            data3 = row[2]
            data4 = row[3]


            
            print(f"{data1:<10} {data2:<20}\t{data3:<10} {data4:<10}")

    
    
    elif menu == "" :
        break

    else :
        print("메뉴번호를 다시 입력해주세요")
        continue


