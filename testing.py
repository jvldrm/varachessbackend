from myFunctions import  make_move, get_current_turn_and_fen, get_current_turn, checkEmailPass, get_players_id

current_game_id = '33'



if checkEmailPass("jezakval@hotmail.co", "dovesin7") :
    print ("That player exists")
else:
    print ("That player does NOT exist")






players = get_players_id(current_game_id)
print(players)
print("white is ", players[0])
print("black is ", players[1])

(current_player_id_white, current_player_id_black) = players


print("white is ", current_player_id_white)
print("black is ", current_player_id_black)






#arr = get_current_turn(0)



#make_move(33, current_player_id_white, current_player_id_black,  '1r2r2k/1p1n3R/p1qp2pB/6Pn/P1Pp/3B4/1P2PQ1K/5R b - - 0 1')


make_move(current_game_id, current_player_id_white, current_player_id_black,  '1k6/7R/8/5P1p/7P/r7/1r6/5K2 b - - 10 45')



#(turn, fen) = get_current_turn_and_fen(33)

#print(f"The turn is {turn} and fen is {fen}")

(turn, fen) = get_current_turn_and_fen(99)

print(f"turn: {turn} fen: {fen} ")