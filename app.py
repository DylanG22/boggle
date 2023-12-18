from boggle import Boggle
from flask import Flask, request, render_template, flash, redirect, session, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fsaerdf zfbzbdzfrujjbn'
boggle_game = Boggle()

@app.route('/')
def show_home():
    ''' returns the template for the home page'''
    return render_template('home.html')


@app.route('/game')
def show_board():
    ''' makes a new game board then creates template with new board'''
    game_board = boggle_game.make_board()
    session['board'] = game_board
    return render_template('game.html', board=game_board)

@app.route('/check_word')
def check_guess():
    ''' handles app.js request. uses boggle class to check the given word with the game board'''
    guess = request.args['guess']
    board = session['board']
    res = boggle_game.check_valid_word(board,guess)
    return jsonify({'result':res})


@app.route('/gameover', methods=['POST'])
def end_game():
    ''' updates the highscore and times played in session and returns new highscore'''
    score = int(request.json['score'])

    highscore = session.get('highscore',0)
    num_plays = session.get('nplays',0)

    if score > highscore:
        session['highscore'] = score

    session['nplays'] = num_plays + 1
    return jsonify({'highscore' : session.get('highscore',0)})