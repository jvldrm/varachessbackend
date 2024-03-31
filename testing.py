from myFunctions import  make_move, get_current_turn_and_fen, get_current_turn, checkEmailPass, \
    get_players_id, logout, getAvailablePlayers, makeInvitation, checkIfInvited, acceptDeclineInvitation, loginWallet,\
    getStatusOfGame, get_all_players_in_db, getInvitationStatus, checkIfPendingGame
import json

import time

#this is a testing function
def playGame(game_id, current_player, player_id_white, player_id_black):
    (turn, fen) = get_current_turn_and_fen(game_id)
    if current_player == player_id_white:
        player_color = "w"
        player_color_long = 'WHITE'
    elif current_player == player_id_black:
        player_color = "b"
        player_color_long = 'BLACK'

    print(f"Your color is: {player_color_long}")
    print(f"turn: {turn} fen: {fen} ")
    if( turn == player_color):
        print("It's your turn")
        
    else:
        print("It's your opponent's turn")

all_players = get_all_players_in_db()

print("WELCOME TO VARACHESS TEXT VERSION")

print("These are all the players: ")

playersList = {}

print("\tID \tNAME \tACCOUNT \tLASTLOGIN")
for r in all_players:
   print(f'\t{r[0]} \t{r[1]} \t{r[2]} \t{r[3]}\n')
   playersList[r[0]] = [r[1], r[2], r[3]]
   
player_id = int(input("What player ID are you?"))

myPlayer = "megastar"
myAccount = 'Xyqqt47ddn95CZbnDn7HynygXfb1uoaNEvkGC38V9zQ6xuWw'



myPlayer = "unahistoria"
myAccount = '5CZbnDn7HynygXfb1uoaNEvkGC38V9zQ6xuWwXyqqt47ddn9'

myPlayer = playersList[player_id][0]
myAccount = playersList[player_id][1]

print(f"You are {myPlayer} with {myAccount}")

player_id = loginWallet(myPlayer, myAccount )


if player_id > -1:
    print("OKK -- login check, player id: ", player_id)
else:
    print("Problem to login")
    exit



# first check if you have a pending game
listGames = checkIfPendingGame(player_id)

if len(listGames) > 0:
    labels=["ID", "date_start", "player1", "player2", "status", "date_finish",  \
            "player_id_won", "player_id_lost", "player_id_white", "player_id_black" ]
    for r in listGames:
        print("-------------------------")
        for i in range(0, 10):
            print(f"{labels[i]}: {r[i]} ")

    game_id = int( input("Select game ID: "))

    print("You selected this game_id ", game_id)
    playGame(game_id, player_id, listGames[0][8], listGames[0][9])
else:
    print("You don't have any pending games.")





char = input("Do you want to [I]nvite or [W]ait for invitation?? ")

if char == 'I' :
    vals = getAvailablePlayers()
    print( vals )
    jvals =  json.dumps(vals)
    print(jvals)
    playersList = getAvailablePlayers()
    for r in playersList:
        print( f'ID: {r[2]} \t NAME: {r[0]} \n')



    player_id_invite = int(input("What player ID do you want to invite?"))

    print( "INVITATION SUCESS? ", makeInvitation(player_id, player_id_invite) )
    res = input("Do you want to [W]ait for response or [E]xit?? ")
    
    if res == 'W':
        keepWaiting = True
        while keepWaiting == True:
            mySentInvitations = getInvitationStatus(player_id)
            print(mySentInvitations)
            if len(mySentInvitations) > 0 :
                for r in mySentInvitations :
                    print(f"ID:{r[0]} player_id_to:{r[2]} date_invitation:{r[3]} date_response:{r[4]} status:{r[5]} game_id:{r[6]}")
                    if r[5] == "ACCEPTED" :
                        print("THIS INVITATION HAS BEEN ACCEPTED")
                        game_id = r[6]
                        keepWaiting = False
            else:
                print("NO invitations yet, going to wait")

            time.sleep(2)
    else:
        exit

    print("The game can start with game_id: ", game_id)

elif char == 'W' :

    myInvitations = checkIfInvited(player_id)

    if len(myInvitations) > 0:
        print("YOUR INVITATIONS: ")
        for r in myInvitations:
            print(
                f'player_id_from: {r[0]} \t date_invitation: {r[1]} \t status: {r[2]}\n'
            )

        player_id_inviter = int(input("Select a player's invitation: "))
        response = int(input("Take action: \n1 ACCEPT \n0 DECLINE \n"))
        game_id = acceptDeclineInvitation(player_id, player_id_inviter, response)
        print("ACTION STATUS (game_id): ", game_id)
        if game_id > 0:
            print("This is the status of the game: ", getStatusOfGame(game_id))
            playGame(game_id, player_id, player_id_inviter)
        else:
            print("The game was not created")

    else:
        print("YOU HAVE NO INVITATIONS")
else:
    print("Don't know command")


exit()



#res =  checkEmailPass("jezakval@hotmail.com", "dovesin777")
#print (res) 
#print("The first value in tuple is ", res[0])

res = logout( "jezakval@hotmail.com", 'dovesin777')

print("Answer is ", res)


players = get_players_id(current_game_id)
print(players)
print("white is ", players[0])
print("black is ", players[1])

(current_player_id_white, current_player_id_black) = players


print("white is ", current_player_id_white)
print("black is ", current_player_id_black)



#arr = get_current_turn(0)



#make_move(33, current_player_id_white, current_player_id_black,  '1r2r2k/1p1n3R/p1qp2pB/6Pn/P1Pp/3B4/1P2PQ1K/5R b - - 0 1')


#make_move(current_game_id, current_player_id_white, current_player_id_black,  '1k6/7R/8/5P1p/7P/r7/1r6/5K2 b - - 10 45')



#(turn, fen) = get_current_turn_and_fen(33)

#print(f"The turn is {turn} and fen is {fen}")

(turn, fen) = get_current_turn_and_fen(99)

print(f"turn: {turn} fen: {fen} ")




player_id = int(input("What player ID are you?"))

print("These are the available players: ")

playersList = getAvailablePlayers()

print(playersList)
for r in playersList:
    print( f'ID: {r[0]} \t NICK: {r[1]} \t EXP: {r[2]}\n')

player_id_invite = int(input("What player ID do you want to invite?"))

print( "INVITATION SUCESS? ", makeInvitation(player_id, player_id_invite) )

myInvitations = checkIfInvited(player_id)

if len(myInvitations) > 0:
    print("YOUR INVITATIONS: ")
    for r in myInvitations:
        print( f'player_id_from: {r[0]} \t date_invitation: {r[1]} \t status: {r[2]}\n')
    
    player_id_inviter = int(input("Select a player's invitation: "))
    response = int(input("Take action: \n1 ACCEPT \n0 DECLINE \n"))
    print("ACTION STATUS: ", acceptDeclineInvitation(player_id, player_id_inviter, response))
else:
    print("YOU HAVE NO INVITATIONS")
