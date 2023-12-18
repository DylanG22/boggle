from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

board = [['M', 'I', 'U', 'R', 'G'], ['O', 'P', 'H', 'O', 'T'], ['H', 'S', 'R', 'F', 'N'], ['Z', 'F', 'B', 'G', 'F'], ['T', 'T', 'G', 'O', 'J']]

class FlaskTests(TestCase):


    app.config["TESTING"] = True

    def test_show_board(self):
        with app.test_client() as client:
            res = client.get('/game')
            html = res.get_data(as_text=True)
            self.assertIn('<form id="boggle_form">', html)

    def test_check_guess(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['board'] = board
            res = client.get('/check_word?guess=frog')
            self.assertEqual('ok',res.json['result'])
            res2 = client.get('/check_word?guess=mkre')
            self.assertEqual("not-word",res2.json['result'])
            res3 = client.get('/check_word?guess=fire')
            self.assertEqual("not-on-board",res3.json['result'])
