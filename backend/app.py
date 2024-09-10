from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Start of the app Flask and database 
app = Flask(__name__) 
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEM_TRACK_MODFICATIONS'] = False 

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

# User Model 
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150),nullable=False)

# Create tables 
with app.app_context():
    db.create_all()

# Route for load users 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route of register 
@app.route('/register', methods = ['POST','GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Usuario registrado exitosamente!')
        return redirect(url_for('login'))
    return render_template('register.html')

# Route of Login 
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        return 'Login successful', 200  # Respuesta para PyQt5
    else:
        return 'Invalid credentials', 401  # Respuesta de error para PyQt5

# Route of Dashboard bloqued 
@app.route('/dashboard')
@login_required
def dashboard():
    return f'Bienvenido {current_user.username} a la simulacion de semiconductores'

# Route of logout 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesion correctamente')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)