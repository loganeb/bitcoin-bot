from flask import Flask
import state

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/openpositions")
def get_open_positions():
    return state.get_position_open()