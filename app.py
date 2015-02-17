import os, sys

path = os.path.join('.', os.path.dirname(__file__), '../')
sys.path.append(path)

from flask import Flask, g, render_template, redirect, url_for, request, jsonify
import flask_sijax
from werkzeug.contrib.cache import SimpleCache
import shortuuid
import json
from game import Game

cache = SimpleCache() # not good for multiprocess
app = Flask(__name__)

app.config["SIJAX_STATIC_PATH"] = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
app.config["SIJAX_JSON_URI"] = '/static/js/sijax/json2.js'

flask_sijax.Sijax(app)


# helper to id if the request is json 
def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']


@app.route("/")
@app.route("/game/", methods=["GET", "POST"])
def create_new_game():
    if request.method == 'POST':
        room_id = shortuuid.ShortUUID().random(length=4)
        game_object = Game()
        cache.set(room_id, game_object, timeout=60 * 60*24) # game is good for 24h
        # redirect to game room
        url = url_for('game', room_id=room_id)
        return redirect(url)
    return render_template('index.html')
    

@flask_sijax.route(app, "/game/<room_id>")
def game(room_id): #, methods=["GET", "POST"]):
    def update_game_object(position):
        position = int(position)
        current_player = game_object.get_current_player()

        if current_player.type == "human":
            current_player.set_move(position)
            game_object.execute_move(current_player)
        else: # it's an ai have it move
            game_object.execute_move(current_player)
        ### store state
        cache.set(room_id, game_object, timeout=60 * 60*24) # game is good for 24h
        ##########################
        # get the next player so if it's an AI we can have it play it's turn
        next_player = game_object.get_current_player()

        if next_player.type is not "human":
            game_object.execute_move(next_player)

        ### store state
        cache.set(room_id, game_object, timeout=60 * 60*24) # game is good for 24h


    def make_move_handler(obj_response, position):
        update_game_object(position)
        
        ### update board
        for i, cell in enumerate(game_object.board):
            obj_response.html("#%s" % i, cell)
        if game_object.is_game_ended: # game has ended
            if game_object.is_winning_board: # game has been  won
                for cell_id in game_object.winning_row:
                    obj_response.css('#%s' % cell_id, 'background-color', 'green')
                obj_response.html("#winner", "'%s' has Won the game!" % game_object.winner_symbol)
            else : # it's a draw
                obj_response.html("#winner", "Uh! Oh! it's a draw!")

    game_object = cache.get(room_id)
    # register the sijax callbacks
    if g.sijax.is_sijax_request:
        g.sijax.register_callback('make_move', make_move_handler)
        return g.sijax.process_request()
    return render_template('game.html', game_object=game_object)


if __name__ == '__main__':
    app.run(debug=True, port=8080)

