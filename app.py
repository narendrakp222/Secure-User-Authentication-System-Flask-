from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.secret_key = 'dadhfahfa'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)  

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']

    try:
        hashedpassword = generate_password_hash(password)
        user = User(username=username, password=hashedpassword)
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    except:
        p = 'Try Again With Different Username'
        return render_template('register.html', e=p)

@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        return redirect('/dashboard')

    p = "Wrong username or password"
    return render_template("index.html", p=p)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

@app.route('/update', methods=['GET', 'POST'])
def update():
    if 'user_id' not in session:
        return redirect('/')

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        user.username = request.form['username']
        db.session.commit()
        return redirect('/dashboard')

    return render_template('update.html', user=user)


@app.route('/delete')
def delete():
    if 'user_id' not in session:
        return redirect('/')

    user = User.query.get(session['user_id'])
    return render_template('delete.html', user=user)

@app.route('/confirm_delete', methods=['POST'])
def confirm_delete():
    if 'user_id' not in session:
        return redirect('/')

    user = User.query.get(session['user_id'])
    db.session.delete(user)
    db.session.commit()
    session.pop('user_id')

    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
