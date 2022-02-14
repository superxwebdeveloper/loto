from flask import Flask, session, render_template, redirect, request, abort
from my_secrets import my_username, my_password
import os
import random
import time

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

def challenge():
    random.seed(int(time.time()))
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
        chall = challenge()
        session["solution"] = chall
        if len(guess) != 5:
            session["state"] = "loser"
            return redirect("/", 302)
        for i in range(5):
            if guess[i] != chall[i]:
                session["state"] = "loser"
                return redirect("/", 302)
        session["state"] = "winner"    
    if session["state"] != "winner":
        abort(403, "You have not won the game!")
    return render_template("win.html")

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == 'POST':
        if login(request.form["username"], request.form["password"]):
            session["state"] = "player"
            return redirect("/", 302)
    return render_template("login.html", failed=(request.method=="POST"))
    
if __name__ == "__main__":
    app.secret_key = "debugKey"
    app.run(host="127.0.0.1", debug=True, port=5000)