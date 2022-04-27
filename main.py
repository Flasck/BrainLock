from flask import Flask, render_template, request
from werkzeug.utils import redirect
from forms.user_forms import RegisterForm, LoginForm
from data.users import User
from data import db_session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandex_lyceum_secret_key'
name = ""
surname = ""
email = ""


@app.route("/")
@app.route("/home")
def home():
    global name, surname, email
    gr = [0]
    r = [0]
    if name:
        db_sess = db_session.create_session()
        gr = [int(el) for el in db_sess.execute(f"""SELECT green FROM users WHERE email = '{str(email)}'""").fetchone()[0].split()]
        r = [int(el) for el in db_sess.execute(f"""SELECT red FROM users WHERE email = '{str(email)}'""").fetchone()[0].split()]
        db_sess.close()
    return render_template("home.html", name=name, surname=surname, gr=gr, r=r)


@app.route("/registration", methods=['GET', 'POST'])
def register():
    global name, surname, email
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
        email = user.email
        db_sess.close()
        return redirect("/home")
    return render_template('reg.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global name, surname, email
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
            email = user.email
            db_sess.close()
            return redirect("/home")
        return render_template('login.html',  form=form, message="Ошибка! Логин или пароль введены неверно!")
    return render_template('login.html', form=form)


@app.route("/task/<typ>/<number>")
def task(typ, number):
    global name, surname
    db_sess = db_session.create_session()
    task = db_sess.execute(f"""SELECT tasks FROM task WHERE num = {number} AND typ = {typ}""").fetchone()[0]
    answer = db_sess.execute(f"""SELECT answers FROM task WHERE num = {number} AND typ = {typ}""").fetchone()[0]
    db_sess.close()
    return render_template("task.html", number=number, typ=typ, task=task, answer=answer, name=name, surname=surname)


@app.route('/pass_val/<resp>', methods=['GET', 'POST'])
def pass_val(resp):
    global email
    db_sess = db_session.create_session()
    user_id = db_sess.execute(f"""SELECT id FROM users WHERE email = '{str(email)}'""").fetchone()[0]
    user_green = str(db_sess.execute(f"""SELECT green FROM users WHERE email = '{str(email)}'""").fetchone()[0])
    user_red = str(db_sess.execute(f"""SELECT red FROM users WHERE email = '{str(email)}'""").fetchone()[0])

    if resp.startswith("g") and resp[1:] not in user_green:
        db_sess.execute(f"""UPDATE users SET green = '{user_green}{str(resp[1:])} ' WHERE id = {user_id}""")

    elif resp.startswith("b") and resp[1:] not in user_green and resp[1:] not in user_red:
        db_sess.execute(f"""UPDATE users SET red = '{user_red}{str(resp[1:])} ' WHERE id = {user_id}""")
    else:
        return

    db_sess.commit()
    db_sess.close()
    return resp


if __name__ == '__main__':
    db_session.global_init("db/DB.db")
    app.run(port=5000, host='127.0.0.1')
