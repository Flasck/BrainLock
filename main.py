from flask import Flask, render_template
from werkzeug.utils import redirect
from forms.user_forms import RegisterForm, LoginForm
from data.users import User
from data import db_session
import sqlalchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandex_lyceum_secret_key'
name = ""
surname = ""


@app.route("/")
@app.route("/home")
def home():
    global name, surname
    return render_template("home.html", name=name, surname=surname)


@app.route("/registration", methods=['GET', 'POST'])
def register():
    global name, surname
    if name:
        name = ""
        surname = ""
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template('reg.html', message="Пароли не совпадают!", form=form)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('reg.html', message="Эта почта уже занята!", form=form)
        user = User(email=form.email.data, surname=form.surname.data, name=form.name.data,)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        name = user.name
        surname = user.surname
        return redirect("/home")
    return render_template('reg.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global name, surname
    if name:
        name = ""
        surname = ""
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            name = user.name
            surname = user.surname
            return redirect("/home")
        return render_template('login.html',  form=form, message="Ошибка! Логин или пароль введены неверно!")
    return render_template('login.html', form=form)


@app.route("/task/<typ>/<number>")
def task(typ, number):
    global name, surname
    db_sess = db_session.create_session()
    task = db_sess.execute(f"""SELECT tasks FROM task WHERE num = {number} AND typ = {typ}""").fetchone()[0]
    answer = db_sess.execute(f"""SELECT answers FROM task WHERE num = {number} AND typ = {typ}""").fetchone()[0]
    return render_template("task.html", number=number, typ=typ, task=task, answer=answer, name=name, surname=surname)


if __name__ == '__main__':
    db_session.global_init("db/DB.db")
    app.run(debug=True, port=8080, host='127.0.0.1')
