from flask import Flask, session, render_template, redirect, request, abort
from my_secrets import my_username, my_password
import os
import random
import time

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

scoreboard_folder = "/home/web/scoreboard/"

def challenge(id):
    random.seed(int(time.time()) + id)
    solution = random.sample(list(range(1,50)), 5)
    solution.sort()
    return solution

def extract_guess(guess):
    guess = ''.join([c for c in guess if c.isdigit() or c == ','])
    while len(guess) > 0 and guess[0] == ",":
        guess = guess[1:]
    while len(guess) > 0 and guess[-1] == ",":
        guess = guess[:-1]
    if len(guess) == 0:
        return []
    guess = [int(x) for x in guess.split(",")]
    guess.sort()
    return guess

def login(username, password):
    return username == my_username and password == my_password

@app.route("/")
def main():
    if 'state' not in session:
        return redirect("/login", 302)
    return render_template("index.html")

@app.route("/winner", methods=["POST", "GET"])
def verify():
    if 'state' not in session:
        return redirect("/login", 302)
    if request.method == "POST":
        guess = extract_guess(request.form["guess"])
        chall = challenge(session["id"])
        if "solution" in session and chall == session["solution"]:
            abort(403, "Rate limited!")
        session["solution"] = chall
        if guess != chall:
            session["state"] = "loser"
            return redirect("/", 302)
        session["state"] = "winner"
    if session["state"] != "winner":
        abort(403, "You have not won the game!")
    return render_template("win.html", time=int(time.time()))

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == 'POST':
        if login(request.form["username"], request.form["password"]):
            session["state"] = "player"
            session["id"] = random.randint(1,1000000)
            return redirect("/", 302)
    return render_template("login.html", failed=(request.method=="POST"))

@app.route("/scoreboard", methods=["GET", "POST"])
def scoreboard():
    if request.method == "POST":
        if 'state' not in session or session["state"] != "winner":
            return redirect("/login", 302)
        with open(scoreboard_folder + request.form["date"], "a+") as f:
            f.write(request.form["name"])
    winners = []
    timestamps = []
    for t in os.listdir(scoreboard_folder):
        try:
            x = int(t)
            if x >= 0:
                timestamps.append(x)
        except ValueError:
            pass
    timestamps.sort()
    for t in timestamps:
        with open(scoreboard_folder + str(t)) as f:
            winners.append(f.read())
    return render_template("scoreboard.html", winners=winners)
    
if __name__ == "__main__":
    app.secret_key = "debugKey"
    scoreboard_folder = "/home/apoirrier/scoreboard/"
    app.run(host="127.0.0.1", debug=True, port=5000)