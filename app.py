from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "play X here"

    return render_template("game.html", game=session["board"], turn=session["turn"])

def win( r, c):
    val = session["board"][r][c]
    if (r+1 < 3 and r-1 >= 0):
        if (session["board"][r+1][c] == val and session["board"][r-1][c] == val):
            return True
    else:
        return False

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    if session["turn"] == "play X here":
        session["board"][row][col] = "X"
        if (win(row, col)):
            name = "X"
            return render_template("win.html", name = name)
        else:
            session["turn"] = "play O here"
    elif session["turn"] == "play O here":
        session["board"][row][col] = "O"
        if (win( row, col)):
            name = "O"
            return render_template("win.html", name = name)
        else:
            session["turn"] = "play X here"
    return redirect(url_for("index"))

