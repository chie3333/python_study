import sqlite3

import pandas as pd

con = None
cur = None


con = sqlite3.connect("tax_adjustment.db")
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS stock_list")
cur.execute("""
            create table if not exists stock_list
            (
            stock_code text PRIMARY KEY,
            asset_name text,
            market_type text
            )
            """)
df = pd.read_csv("stock_list.csv")
df.to_sql("stock_list", con, if_exists="append", index=False)

"""
테이블 정보 보는 방법
cur.execute("PRAGMA table_info(stock_list)")
print(cur.fetchall())
con.commit()
"""
# cur.execute("""
#             select * from stock_list
#             where stock_code = "00660"
#             """)

# row = cur.fetchone()

# print(row)


con.close()


