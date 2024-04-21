from flask import Flask, request, jsonify, render_template, make_response
import json
import sqlite3
from myFunctions import get_current_turn, make_move, get_current_turn_and_fen, \
                    checkEmailPass, get_players_id, logout, getAvailablePlayers, loginWallet, \
                    makeInvitation, getInvitationStatus, checkIfInvited, acceptDeclineInvitation, \
                    finishGame, getStatusOfGame, removeGame, removeInvitation

from flask_cors import CORS
import logging
logging.basicConfig(filename='myLog.log', encoding='utf-8', level=logging.DEBUG)

from datetime import datetime


app = Flask(__name__)
#CORS(app)
CORS(app, supports_credentials=True) 
#cors = CORS(app, resources={r"*": {"origins": "*"}})
#CORS(app, origins='http://localhost:3000')
#app.config['CORS_HEADERS'] = 'Content-Type'

current_game_id = '33'
current_player_id_white = '222'
current_player_id_black = '777'

@app.route("/")
def hello_world():
    con = sqlite3.connect("mydata.db")
    cur = con.cursor()
    cur.execute(
      "CREATE TABLE if not exists plays(id INTEGER NOT NULL PRIMARY KEY, move_id, turn, fen, player_id_white, player_id_black)"
    )
    
    return "<p>Hello, World! <a href='/play'> GO PLAY </a>  </p>"

@app.route("/form")
def form():
    return render_template('aform.html')

@app.route("/loginplayer")
def loginplayer():
    name = request.args.get('name')
    account = request.args.get('account')
    status = loginWallet(name, account)
    myObj = {   
                    'status' : status, 
                    } 
    response = make_response(jsonify(myObj))
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


@app.route("/login") 
def login():
    email = request.args.get('email')
    password = request.args.get('password')

    datadb = checkEmailPass(email, password)
    canlog = datadb[0]
    if canlog :
        myObj = {   
                    'email' : email, 
                    'password' : password,
                    'nickname': datadb[1],
                    'name': datadb[2],
                    'logged' : 'true'
                    } 
    else:
        myObj = {   
                    'email' : email, 
                    'password' : password,
                    'logged' : 'false'
                    } 

    response = make_response(jsonify(myObj))
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response
    #return "<p>HELLO and wlecome</p>";

@app.route("/logoutplayer") 
def logoutplayer():
    email = request.args.get('email')
    password = request.args.get('password')
    if logout(email, password) :
        myObj = {   
                    'status' : 'ok'
                    } 
    else:
        myObj = {   
                    'status' : 'error'
                } 
    response = make_response(jsonify(myObj))
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


@app.route("/invite")
def invite():
    player_id_from = request.args.get('player_id_from')
    player_id_to = request.args.get('player_id_to')

    status = makeInvitation(player_id_from, player_id_to)
    myObj = {   'status' : status, 
                } 
    response = make_response(jsonify(myObj))
    return response


@app.route("/test", methods=["POST", "OPTIONS"])
def test():
    logging.debug('I am at the TEST post, got this stuff %s', request.form['player_id'])

    x = request.form['player_id']
    y = request.form['player_color']
    z = request.form['game_id']
    myObj = {   'player_id' : x, 
                'player_color' : y, 
                'game_id' : z,
                
                'fen': 'ppppx',
                'status': 'WAIT',
                'turn': 'w'
                } 
    response = make_response(jsonify(myObj))
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

    #return jsonify(myObj)

@app.route('/test_get')
def test_get():
    x = request.args.get('player_id')
    y = request.args.get('player_color')
    myObj = {   'player_id' : x, 
                'player_color' : y, 
                'game_id' : '22',
                
                'fen': 'ppppx',
                'status': 'WAIT from get',
                'turn': 'w'
                } 
    response = make_response(jsonify(myObj))
    return response

@app.route('/reset')
def resetgame():
    fenReset = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    make_move(game_id, current_player_id_white, current_player_id_black, fenReset)
    myObj = {   'player_id' : player_id, 
                'player_color' : player_color, 
                'game_id' : game_id,
                
                'fen': fenReset,
                'status': 'RESTART',
                'turn': 'w'
                } 
    
    print(f"CURRENT FEN: {fen}\nCURRENT TURN: {turn}")
    
    response = jsonify(myObj)
    #response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route("/status")
def status():
    
    game_id=request.args.get('game_id') or 'None'
    print(f"@status game_id: {game_id}")

    valuesArr = get_current_turn(game_id)
    
    if valuesArr == [] :
        myObj = {   
                    'turn': "EMPTY",
                    'fen': "EMPTY",
                    'player_id_white': "EMPTY",
                    'player_id_black': "EMPTY",

                } 
        
    else :
        myObj = {   
                    'turn': valuesArr[7],
                    'fen': valuesArr[6],
                    'player_id_white': valuesArr[4],
                    'player_id_black': valuesArr[5],

                } 
    response = jsonify(myObj)
    return response

@app.route("/play")
def play():
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
   
    print("\n\n@ /play route from get ", current_time)
    #<player_id>/<player_color>/<game_id>/<fen>
    player_id= request.args.get('player_id') or 'None'
    player_color=request.args.get('player_color') or 'None'
    game_id=request.args.get('game_id') or 'None'
    fen=request.args.get('fen') or 'None'

    (player_id_white, player_id_black)=get_players_id(game_id)

    print(f"--And i got this: \nplayer_id: {player_id} \nplayer_color: {player_color} \ngame_id: {game_id} \nfen: {fen} ")

    logging.debug('I am at /play got player_id=%s ,player_color=%s, game_id=%s fen=%s', player_id, player_color, game_id, fen )
    logging.debug('game_id has this type: %s', type(game_id))

    if(fen != 'None' ) :
        make_move(game_id, player_id_white, player_id_black,  fen)

    (turn, fen) = get_current_turn_and_fen(game_id)

    myObj = {   'player_id' : player_id, 
                'player_color' : player_color, 
                'game_id' : game_id,
                
                'fen': fen,
                'status': 'WAIT',
                'turn': turn
                } 
    
    print(f"CURRENT FEN: {fen}\nCURRENT TURN: {turn}")
    
    response = jsonify(myObj)
    #response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/whoseturn")
def whoseturn():
    (turn, fen) = get_current_turn_and_fen(current_game_id)
    return f"<p> The turn is for {turn} with fen: {fen} </p>"

if __name__ == '__main__':
    app.run(debug=True)




@app.route('/listplayers')
def listplayers():
    list_players = getAvailablePlayers()
    response = make_response(jsonify(list_players))
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


@app.route('/mysentinvitations/<player_id>')
def mysentinvitations(player_id):
    #game_id=request.args.get('game_id') 
    list_invitations = getInvitationStatus(player_id)
    response = make_response(jsonify(list_invitations))
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

@app.route('/gamestatus/<game_id>')
def gamestatus(game_id):
    #game_id=request.args.get('game_id') 
    list_invitations = getStatusOfGame(game_id)
    response = make_response(jsonify(list_invitations))
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

@app.route('/endgame/<game_id>/<player_id_won>/<player_id_lost>/<status>')
def endgame(game_id, player_id_won, player_id_lost, status):
    #game_id=request.args.get('game_id') 
    response = finishGame(game_id, player_id_won, player_id_lost, status)
    response = make_response(jsonify(response))
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


@app.route('/closegame/<game_id>')
def closegame(game_id):
    #game_id=request.args.get('game_id') 
    response = removeGame(game_id)
    response = make_response(jsonify(response))
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

@app.route('/myinvitations/<player_id>')
def myinvitations(player_id):
    #game_id=request.args.get('game_id') 
    list_invitations = checkIfInvited(player_id)
    response = make_response(jsonify(list_invitations))
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response




@app.route('/acceptdeclineinvitation/<player_id>/<player_id_from>/<response>')
def acceptdeclineinvitation(player_id, player_id_from, response):
    #game_id=request.args.get('game_id') 
    print(f"@acceptdeclineinvitation {player_id} {player_id_from} {response}")
    list_invitations = acceptDeclineInvitation(player_id, player_id_from, response)
    response = make_response(jsonify(list_invitations))
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


@app.route('/cancelinvitation/<player_id_from>/<player_id_to>')
def cancelinvitation(player_id_from, player_id_to):
    #game_id=request.args.get('game_id') 
    response = removeInvitation(player_id_from, player_id_to)
    response = make_response(jsonify(response))
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response