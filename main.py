from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/registration")
def reg():
    return render_template("reg.html")


@app.route("/home_registered")
def home_reg():
    return render_template("home_reg.html")


@app.route("/task")
def task():
    return render_template("task.html")


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='127.0.0.1')

