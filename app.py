import os, sys

path = os.path.join('.', os.path.dirname(__file__), '../')
sys.path.append(path)

from flask import Flask, g, render_template, redirect, url_for, request
import flask_sijax
from werkzeug.contrib.cache import SimpleCache
import shortuuid
from game import Game

cache = SimpleCache() # not good for multiprocess
app = Flask(__name__)

app.config["SIJAX_STATIC_PATH"] = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
app.config["SIJAX_JSON_URI"] = '/static/js/sijax/json2.js'

flask_sijax.Sijax(app)

@app.route("/")
@app.route("/game/", methods=["GET", "POST"])
def create_new_game():
    if request.method == 'POST':
        room_id = shortuuid.ShortUUID().random(length=4)
        game_object = Game()
        cache.set(room_id, game_object, timeout=60 * 60*24) # game is good for 24h
        # redirect to game room
        return redirect(url_for('game', room_id=room_id))
    # otherwise list rooms
    return render_template('index.html')
    # return

@flask_sijax.route(app, "/game/<room_id>")
def game(room_id): #, methods=["GET", "POST"]):
    def make_move_handler(obj_response, position):
        print "this is the position to be played", position
        position = int(position)
        current_player = game_object.get_current_player()
        # current_player.set_move(position)
        print "current_player player ::", current_player.symbol, current_player.type
        if current_player.type == "human":
            current_player.set_move(position)
            game_object.execute_move(current_player)
        else:
        #     ai_position_play = current_player.make_move(game_object.board)
            game_object.execute_move(current_player)


        ### store state
        cache.set(room_id, game_object, timeout=60 * 60*24) # game is good for 24h
        ##########################
        next_player = game_object.get_current_player()

        print "next player ::", next_player.symbol, next_player.type
        if next_player.type is not "human":
            game_object.execute_move(next_player)

        ### store state
        cache.set(room_id, game_object, timeout=60 * 60*24) # game is good for 24h
        ### update board
        for i, cell in enumerate(game_object.board):
            obj_response.html("#%s" % i, cell)
        if game_object.is_winning_board:
            for cell_id in game_object.winning_row:
                obj_response.css('#%s' % cell_id, 'background-color', 'green')
            print "Winner", game_object.winner_symbol
            obj_response.html("#winner", "'%s' has Won the game!" % game_object.winner_symbol)
        elif game_object.is_game_ended:
            obj_response.html("#winner", "Uh! Oh! it's a draw!")
        # if 
    game_object = cache.get(room_id)

    vars = {
        "game": game_object
    }

    if g.sijax.is_sijax_request:
        g.sijax.register_callback('make_move', make_move_handler)
        return g.sijax.process_request()
    return render_template('game.html', vars=vars, game_object=game_object)


if __name__ == '__main__':
    app.run(debug=True, port=8080)