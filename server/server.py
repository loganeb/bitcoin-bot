from flask import Flask
import json
import state

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/openpositions")
def get_open_positions():
    op = state.get_open_positions()
    res = {}
    for key in op.keys():
        res[key] = json.loads(op[key])
    return res

if __name__ == "__main__":
    main()