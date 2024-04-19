import sqlite3

game_id  = 33

con = sqlite3.connect("mydata.db")
cur = con.cursor()
res = cur.execute(f"""
                  update plays set fen = '1k6/4R3/8/r4P1p/1r5P/8/7K/8 b - - 0 40' 
                  where id=(select max(id) as id from plays where game_id={game_id}) 
                  and game_id={game_id};
                  """)

