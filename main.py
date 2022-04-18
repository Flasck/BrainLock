from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", name="", surname="", len1=15, len2=5)


@app.route("/registration")
def reg():
    return render_template("reg.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/task/<typ>/<number>")
def task(typ, number):
    return render_template("task.html", typ=typ, number=number)


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='127.0.0.1')

