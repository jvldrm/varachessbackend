import sqlite3
import random
import logging
logging.basicConfig(filename='myLog.log', encoding='utf-8', level=logging.DEBUG)


def get_all_players_in_db():
    con = sqlite3.connect("mydata.db")
    cur = con.cursor()
    res = cur.execute(f""" select id, name, account, lastlogin from players """)
    li = res.fetchall()
    return li


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







def make_move(game_id, player_id_white, player_id_black, fen):
  print('-- at make_move')
  #print("game id is ", game_id)

  con = sqlite3.connect("mydata.db")
  cur = con.cursor()
  res = cur.execute(
      f'select id, turn from plays where id = (select max(id) as id from plays where game_id={game_id}) and game_id={game_id}'
  )
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
  else:  #if the game_id already exists, proceed to insert a move
    print("---If the game_id already exists, proceed to insert a move")
    move_id = int(vals[0])
    turn_db = vals[1]

    move_id += 1

    if turn_db == 'w':
      turn_db = 'b'
    else:
      turn_db = 'w'

    res = cur.execute(f'''insert into plays  
                        (game_id, move_id, turn, fen, player_id_white, player_id_black)
                        values 
                        ("{game_id}", "{move_id}", "{turn_db}", "{fen}", "{player_id_white}", "{player_id_black}")
                        ''')
    ## actualizar el estado del juego
  res=cur.execute(f'''update games set status="INPROGRESS" where id={game_id}''')
  con.commit()
  con.close()


def loginWallet(name, account):
    con = sqlite3.connect("mydata.db")
    cur = con.cursor()
    #res = cur.execute(f'select * from plays where id = (select max(id) from plays where game_id={game_id}) and game_id={game_id}')
    res = cur.execute(f'select * from players where name = "{name}" and account="{account}"')

    
    #val, = res.fetchone()
    print(f"Trying to check if player {name} with account {account}")
    li = res.fetchall()
    if not li : 
        print(f"  There are no players ")
        #crear un renglon para esta cartera
        try:
            res = cur.execute(f"""insert into players (name, account, lastlogin)
                                            values
                                            ( '{name}', '{account}', datetime('now') )""")
            player_id = cur.lastrowid
            con.commit()
            return player_id
        except sqlite3.OperationalError:
            return -1
    else:
        cur.execute(f"""update players set lastlogin=datetime('now')
                    where name='{name}' and account='{account}' """)
        con.commit()
        if cur.rowcount < 1 :
            return -1
        else:
            res = cur.execute(f"""select id from players where name='{name}' and account='{account}' """)
            player_id, = res.fetchone()
            return player_id
        

    



def checkEmailPass(email, password):
    con = sqlite3.connect("mydata.db")
    cur = con.cursor()
    res = cur.execute(f""" select password, nickname, name from players where email='{email}' """)
    vals = res.fetchone()
    
    if not vals : 
        return False
    else:
        (password_db, nickname, name) = vals
        if( password_db == password):
            cur.execute(f""" update players set logged = 1 where email='{email}' """)
            con.commit()
            return (True, nickname, name)
        else:
            return (False,)

def logout(email, password):
    con = sqlite3.connect("mydata.db")
    cur = con.cursor()
    cur.execute(f""" update players set logged = 0 where email='{email}' and password='{password}' """)
    con.commit()
    if cur.rowcount < 1 :
        return False
    else:
        return True
        
def getAvailablePlayers():
    con = sqlite3.connect("mydata.db")
    cur = con.cursor()
    #res = cur.execute("""  select id, nickname, exp from players where logged = 1 """)
    res = cur.execute("""  
                      select name, 1440*(julianday(datetime('now')) - julianday(lastlogin)) as diff, id 
                            from players where diff < 1;
                      """)
    li = res.fetchall()
    
    if not li : 
        return []
    else:
        return li
    
def makeInvitation(player_id_from, player_id_to):
    con = sqlite3.connect("mydata.db")
    cur = con.cursor()
    # revisar si hay invitaciones de este origen
    res = cur.execute(f""" 
                      select status from invitations 
                      where 
                        player_id_to    = {player_id_to} 
                        and 
                        player_id_from  = {player_id_from} 
                      """)
    # solo si no hay invitaciones de este jugador, insert
    li = res.fetchall()
    print( "@make Invitation -- row count from select... ", len(li))
    if len(li) == 0:
        res = cur.execute(f"""insert into invitations (
                                    player_id_from, player_id_to, 
                                    date_invitation, date_response, status, game_id)
                                    values
                                    ({player_id_from}, {player_id_to}, 
                                    datetime('now','localtime'), 
                                    '0', 'WAITING', 0 )""")
        con.commit()
        if cur.rowcount < 1 :
            return False
        else:
            return True
    # si hay invitaciones... decir.. todo bien
    else :
        return True

# para saber si estoy siendo invitado...
def checkIfInvited(player_id):
    con = sqlite3.connect("mydata.db")
    cur = con.cursor()
    res = cur.execute(f""" 
                    select p.name, i.player_id_from, i.date_invitation, i.status, i.game_id 
                      from invitations i 
                      inner join players p on 
                      p.id = i.player_id_to
                      where i.player_id_to = {player_id}
                      """)
    li = res.fetchall()
    for i in range(0, len(li)):
      # check status 
      if ( li[i][3] == 'ACCEPTED') :
        
        r = list(li[i])
        game_id = r[4]
        print("Game id is: ",  game_id)
        res = cur.execute(f"""select  player_id_white, player_id_black from games where id = {game_id} """)
        (player_id_white, player_id_black ) = res.fetchone()
        r.append(  player_id_white )
        r.append( player_id_black )
        li[i] = r


    return li


# para saber si mis invitaciones estan siendo aceptadas (status)...
def getInvitationStatus(player_id):
    con = sqlite3.connect("mydata.db")
    cur = con.cursor()
    res = cur.execute(f"""select i.id, i.player_id_from, i.player_id_to, i.date_invitation, i.date_response, i.status, i.game_id, p.name
                          from invitations i 
                          inner join players p on 
                          p.id = i.player_id_from
                          where i.player_id_from = {player_id}""")
    li = res.fetchall()
    print(li)
    
     
    # check status 
    if ( len(li) > 0 and li[0][5] == 'ACCEPTED') :
       
       li = list(li[0])
       game_id = li[6]
       print("Game id is: ",  game_id)
       res = cur.execute(f"""select  player_id_white, player_id_black from games where id = {game_id} """)
       (player_id_white, player_id_black ) = res.fetchone()
       li.append(  player_id_white )
       li.append( player_id_black )
    return li

def acceptDeclineInvitation(player_id, player_id_from, answer=1):
  con = sqlite3.connect("mydata.db")
  cur = con.cursor()
  print(f"@acceptDeclineInvitation function: {player_id} {player_id_from} {answer} {type(answer)}")
  if int(answer) == 1:
    status = 'ACCEPTED'
    # revisar si ya se habia aceptado...
    # solo puede haber una invitacion del mismo jugador
    #tiene que revisar si esta en WAITING la invitacion para avanzar
    res = cur.execute(f""" 
                      select status from invitations 
                      where 
                        player_id_from    = {player_id_from} 
                        and 
                        player_id_to  = {player_id}
                        and
                        id = (select max(id) as id from invitations 
                                    where player_id_from = {player_id_from} 
                                     and  player_id_to  = {player_id})
                      """)
    (invitation_status, ) = res.fetchone()

    print(
        "@acceptDeclineInvitation (want to accept) current status of invitation: ",
        invitation_status)

    if invitation_status == 'WAITING':
      # escoger quien va a ser el jugador blanco/negro de manera aleatoria
      players = [player_id_from, player_id]
      player_id_white = random.choice(players)
      players.remove(player_id_white)
      player_id_black = players[0]

      # crear el juego si estaba esperando el invitado
      res = cur.execute(f"""insert into games (
                                            player_1, player_2, date_start, status, 
                                            player_id_white, player_id_black
                                        )
                                        values
                                        (  
                                            {player_id_from}, {player_id}, datetime('now','localtime'), 'STARTED', 
                                            {player_id_white}, {player_id_black}
                                        )""")
      game_id = cur.lastrowid
      con.commit()
      # meter el primer movimiento
      res = cur.execute(f"""insert into plays 
                                  (turn, fen, player_id_white, player_id_black, game_id, date_move) 
                                values
                                    ('w', 
                                    'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 
                                    {player_id_from}, {player_id}, {game_id}, datetime('now','localtime')
                                        )""")
      con.commit()
      # revisar si esto esta bien... (PENDIENTE)
    elif invitation_status == 'ACCEPTED':
      #obtener el id del juego si tiene el juego iniciado
      res = cur.execute(f""" 
                      select id from games 
                      where 
                        player_1    = {player_id_from} 
                        and 
                        player_2  = {player_id}
                        and
                        status = 'STARTED'
                      """)
      (game_id, ) = res.fetchone()

    elif invitation_status == 'DECLINED':
      # si ya estaba declinado, no se puede empezar el juego
      game_id = 0
      status = 'DECLINED'
    else:
      # el caso de que no esta aceptado, ni esta esperando, en caso de que no es ninunga de estas opciones
      game_id = 0

  else:
    status = 'DECLINED'
    game_id = 0

  print("The game ID is: ", game_id)

  res = cur.execute(f""" 
                      update invitations
                        set  status = '{status}',
                        date_response = datetime('now','localtime'),
                        game_id = {game_id}
                      where 
                        player_id_to    = {player_id} 
                        and 
                        player_id_from  = {player_id_from} 
                      """)
  con.commit()
  if cur.rowcount < 1:
    return -1
  else:
    return game_id





def checkIfPendingGame(player_id):
    con = sqlite3.connect("mydata.db")
    cur = con.cursor()
    res = cur.execute(f"""select * from games where (player_1 = {player_id} or player_2 = {player_id} ) and status != 'FINISHED' """)
    li = res.fetchall()
    return li


def getStatusOfGame(game_id):
  con = sqlite3.connect("mydata.db")
  cur = con.cursor()
  res = cur.execute(f"""select status from games where id = {game_id} """)
  (status, ) = res.fetchone()
  return status

    
def finishGame(game_id, player_id_won, player_id_lost, draw):
  con = sqlite3.connect("mydata.db")
  cur = con.cursor()
  res = cur.execute(f""" 
                      update game
                        set status = 'FINISHED',
                            date_finish = datetime('now','localtime'),
                            player_id_won = {player_id_won},
                            player_id_lost = {player_id_lost},
                            draw = {draw}
                      where 
                        game_id = {game_id}
                      """)
  ## borrar la invitacion cuando se termina el juego
  res = cur.execute(f"""
                      delete from invitations where game_id={game_id}
                      """)
  con.commit()
  if cur.rowcount < 1:
    return False
  else:
    return True
    








#### prev
    
def acceptDeclineInvitation0(player_id, player_id_from, answer=1):
    con = sqlite3.connect("mydata.db")
    cur = con.cursor()
    if answer == 1 :
        status = 'ACCEPTED'
        # revisar si ya se habia aceptado...

        res = cur.execute(f""" 
                      select status from invitations 
                      where 
                        player_id_from    = {player_id_from} 
                        and 
                        player_id_to  = {player_id}
                        and
                        id = (select max(id) as id from invitations 
                                    where player_id_from = {player_id_from} 
                                     and  player_id_to  = {player_id})
                      """)
        (invitation_status, ) = res.fetchone() 

        print("@acceptDeclineInvitation (want to accept) current status of invitation: ", invitation_status)

        if invitation_status == 'WAITING':
            # crear el juego si estaba esperando el invitado
            res = cur.execute(f"""insert into games (
                                            player_1, player_2, date_start, status
                                        )
                                        values
                                        (  
                                            {player_id_from}, {player_id}, datetime('now','localtime'), 'STARTED'
                                        )""")
            game_id = cur.lastrowid
            con.commit()
            # meter el primer movimiento
            res = cur.execute(f"""insert into plays 
                                        (turn, fen, player_id_white, player_id_black, game_id, date_move) 
		                            values
		                                ('w', 
                                        'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 
                                        {player_id_from}, {player_id}, {game_id}, datetime('now','localtime')
                                         
                                        )""")
            con.commit()
            # revisar si esto esta bien... (PENDIENTE)
        elif invitation_status == 'ACCEPTED':
            #obtener el id del juego si tiene el juego iniciado
            res = cur.execute(f""" 
                      select id from games 
                      where 
                        player_1    = {player_id_from} 
                        and 
                        player_2  = {player_id}
                        and
                        status = 'STARTED'
                      """)
            (game_id, ) = res.fetchone() 
            
        elif invitation_status == 'DECLINED':
            # si ya estaba declinado, no se puede empezar el juego
            game_id = 0
            status = 'DECLINED'
        else:
            # el caso de que no esta aceptado, ni esta esperando, en caso de que no es ninunga de estas opciones
            game_id = 0
            
    else : 
        status = 'DECLINED'
        game_id = 0

    print("The game ID is: ", game_id)

    res = cur.execute(f""" 
                      update invitations
                        set  status = '{status}',
                        date_response = datetime('now','localtime'),
                        game_id = {game_id}
                      where 
                        player_id_to    = {player_id} 
                        and 
                        player_id_from  = {player_id_from} 
                      """)
    con.commit()
    if cur.rowcount < 1 :
        return False
    else:
        return True
    