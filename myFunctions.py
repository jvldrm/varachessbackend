import sqlite3

import logging
logging.basicConfig(filename='myLog.log', encoding='utf-8', level=logging.DEBUG)



def get_current_turn_and_fen(game_id):
    con = sqlite3.connect("mydata.db")
    cur = con.cursor()
    res = cur.execute(f""" select turn, fen 
                      from plays 
                      where 
                      game_id={game_id}
                      and id=(select max(id) as id from plays where game_id={game_id}) """)
    val = res.fetchone() 

    return val
    

    #if val is None:
    

def get_current_turn(game_id):
    con = sqlite3.connect("mydata.db")
    cur = con.cursor()
    res = cur.execute(f'select * from plays where id = (select max(id) as id from plays where game_id={game_id}) and game_id={game_id}')

    #val, = res.fetchone()
    li = res.fetchall()
    if not li : 
        print(f"There is no game_id {game_id}")
        return []
    
    valuesArr, = li
    print(f"This is the array: {valuesArr}")
    if valuesArr == []:
        print ("There are no games with that ID")
    else:
        print(f"At get_current_turn the value is {valuesArr} id:{valuesArr[0]}")

    con.close()

    #if val is None:
    #    val = 'notstarted'
    #return val
    
    return valuesArr

def get_players_id(game_id):
    con = sqlite3.connect("mydata.db")
    cur = con.cursor()
    #res = cur.execute(f'select * from plays where id = (select max(id) from plays where game_id={game_id}) and game_id={game_id}')
    res = cur.execute(f'select * from plays where id = (select max(id) as id from plays where game_id={game_id}) and game_id={game_id}')

    
    #val, = res.fetchone()
    print("Trying to get players id from game_id")
    li = res.fetchall()
    if not li : 
        print(f"    There is no game_id {game_id}")
        return []
    
    valuesArr, = li
    
    if valuesArr == []:
        print ("There are no games with that ID")
        players=()
    else:
        print(f"At get_current_turn the value is {valuesArr} id:{valuesArr[0]}")
        players = (valuesArr[4], valuesArr[5])
    
    print(f"    This is the players tuple: {players}")

    con.close()

    #if val is None:
    #    val = 'notstarted'
    #return val
    
    return players







def make_move(game_id, player_id_white, player_id_black, fen ):
    print('-- at make_move')
    #print("game id is ", game_id)

    con = sqlite3.connect("mydata.db")
    cur = con.cursor()
    res = cur.execute(f'select id, turn from plays where id = (select max(id) as id from plays where game_id={game_id}) and game_id={game_id}')
    #print(res)
    

    vals = res.fetchone()
    #print (type(vals))

    if vals == None:
        #print ("there is an error, game does not exist perhaps")
        # put the new game_id and make the first move
        res = cur.execute(f'''insert into plays  
                      (game_id, move_id, turn, fen, player_id_white, player_id_black)
                      values 
                      ("{game_id}", "0", "w", "{fen}", "{player_id_white}", "{player_id_black}")
                      ''')
    else: #if the game_id already exists, proceed to insert a move
        print("---If the game_id already exists, proceed to insert a move")
        move_id = int( vals[0] )
        turn_db = vals[1]

        move_id += 1
        
        if turn_db == 'w' :
            turn_db = 'b' 
        else:
            turn_db = 'w'
    
        res = cur.execute(f'''insert into plays  
                        (game_id, move_id, turn, fen, player_id_white, player_id_black)
                        values 
                        ("{game_id}", "{move_id}", "{turn_db}", "{fen}", "{player_id_white}", "{player_id_black}")
                        ''')
    con.commit()
    con.close()


def checkEmailPass(email, password):
    con = sqlite3.connect("mydata.db")
    cur = con.cursor()
    res = cur.execute(f""" select password from players where email='{email}' """)
    vals = res.fetchone()
    if not vals : 
        return False
    else:
        val, = vals 
        if( val == password):
            return True
        else:
            return False
     
