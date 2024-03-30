from myFunctions import  make_move, get_current_turn_and_fen, get_current_turn, checkEmailPass, get_players_id, logout, getAvailablePlayers, makeInvitation, checkIfInvited, acceptDeclineInvitation, loginWallet
import json
current_game_id = '33'

myPlayer = "sharona"
myAccount = '5CZbnDn7HynygXfb1uoaNEvkGC38V9zQ6xuWwXyqqt47ddn9'
player_id_from = 11
status = loginWallet(myPlayer, myAccount )
if status:
    print("OKK -- login check")
else:
    print("Problem to login")

vals = getAvailablePlayers()
print( vals )
jvals =  json.dumps(vals)
print(jvals)
playersList = getAvailablePlayers()
for r in playersList:
    print( f'ID: {r[2]} \t NAME: {r[0]} \n')



player_id_invite = int(input("What player ID do you want to invite?"))

print( "INVITATION SUCESS? ", makeInvitation(player_id_from, player_id_invite) )

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
