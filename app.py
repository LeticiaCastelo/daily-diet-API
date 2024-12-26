from flask import Flask, request, jsonify
from database import db
from models.user import User
from models.meal import Meal
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
     return User.query.get(user_id)

@app.route("/login", methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User.query.filter_by(username=username).first()

        if user and password == password:
                login_user(user)
                print(current_user.is_authenticated)
                return jsonify({'message': "Login realizado com sucesso"})
    
    return jsonify({"message": "Credenciais inválidas"}), 400

@app.route('/logout', methods=['GET'])
@login_required
def logout():
      logout_user()
      return jsonify({"message": "Logout realizado com sucesso"})

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        message = {"message": f"Usuário {username} cadastrado com sucesso"}
        return jsonify(message)
    
    return jsonify({"message": "Credenciais inválidas"}), 400

if __name__ == '__main__':
    app.run(debug=True)