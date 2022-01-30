from flask import Flask, render_template, request
from helper import manager
app = Flask(__name__, template_folder="templates")


cargo = {"rower": 5, "traktor": 10, "samolot": 1}

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html', cargo=cargo)


@app.route("/ksiegowosc")
def web_account():
    saldo = manager.balance
    return render_template('account.html', saldo=saldo, title='księgowość')


@app.route("/archiwum")
def archive():
    log = manager.logs
    return render_template('archive.html', title='archiwum', log=log)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


if __name__ == '__main__':
    app.run(debug=True)