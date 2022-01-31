from flask import Flask, render_template, request
from helper import manager
app = Flask(__name__, template_folder="templates")


@app.route("/")
@app.route("/home")
def home():
    cargo = manager.warehouse
    balance = manager.balance
    return render_template('index.html', cargo=cargo, balance=balance)


@app.route("/saldo")
def balance():
    return render_template("balance.html", title="Saldo")


@app.route("/balance_response", methods=['POST', 'GET'])
def balance_response():
    manager.error = ""
    income = int(request.form.get('income'))
    comment = request.form.get('comment')
    manager.execute("saldo", income, comment)
    error = manager.error
    cargo = manager.warehouse
    balance = manager.balance
    manager.write_data_to_file()
    return render_template("balance_response.html", income=income, comment=comment, error=error,
                           cargo=cargo, balance=balance)


@app.route("/zakup")
def buy():
    return render_template("buy.html", title="Zakup towaru")


@app.route("/buy_response", methods=['POST', 'GET'])
def buy_response():
    manager.error = ""
    item = request.form.get('item')
    price = int(request.form.get('price'))
    quantity = int(request.form.get('quantity'))
    manager.execute("zakup", item, price, quantity)
    error = manager.error
    cargo = manager.warehouse
    balance = manager.balance
    manager.write_data_to_file()
    return render_template("buy_response.html", item=item, price=price, quantity=quantity, error=error,
                           cargo=cargo, balance=balance)


@app.route("/sprzedaz")
def sale():
    cargo = manager.warehouse
    return render_template("sale.html", title="Sprzedaż towaru", cargo=cargo)


@app.route("/sale_response", methods=['POST', 'GET'])
def sale_response():
    manager.error = ""
    item = request.form.get('item')
    price = int(request.form.get('price'))
    quantity = int(request.form.get('quantity'))
    manager.execute("sprzedaz", item, price, quantity)
    error = manager.error
    cargo = manager.warehouse
    balance = manager.balance
    manager.write_data_to_file()
    return render_template("sale_response.html", item=item, price=price, quantity=quantity, error=error,
                           cargo=cargo, balance=balance)


@app.route("/historia")
@app.route("/historia/<line_from>/<line_to>")
def archive(line_from=None, line_to=None):
    log = manager.logs
    if line_from and line_to:
        return render_template('archive.html', title=f"historia od {line_from} do {line_to}",
                               log=log, line_from=int(line_from), line_to=int(line_to))
    else:
        return render_template('archive.html', title='historia', log=log, line_from=0, line_to=len(log))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


if __name__ == '__main__':
    app.run(debug=True)