from flask import Flask, session, render_template, redirect, request, abort
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

@app.route("/")
def main():
    if 'state' not in session:
        session["state"] = "player"
    return render_template("index.html")

@app.route("/winner", methods=["POST"])
def verify():
    if 'state' not in session:
        return redirect("/", 302)
    guess = extract_guess(request.form["guess"])
    print(guess)
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
    return redirect("/winner", 302)

@app.route("/winner", methods=["GET"])
def win():
    if 'state' not in session:
        return redirect("/", 302)
    if session["state"] != "winner":
        abort(403, "You have not won the game!")
    return render_template("win.html")
    
if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True, port=5000)