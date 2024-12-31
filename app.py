from flask import Flask, request, jsonify
from sqlalchemy.orm import session
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
     return db.session.get(User, user_id)

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

@app.route('/user/new-meal', methods=['POST'])
@login_required
def create_meal():
    data = request.json
    user_id = current_user.id
    name = data.get('name')
    description = data.get('description')
    date = data.get('date')
    time = data.get('time')
    in_diet = data.get("in_diet")

    if name:
        meals = Meal(name=name, description=description, date=date, time=time, in_diet=in_diet, user_id=user_id)
        db.session.add(meals)
        db.session.commit()
        return jsonify({"message": "Refeição adicionada"}), 201
    
    return jsonify({"message": "Erro ao adicionar a refeição"}), 400

@app.route("/user/meals", methods=['GET'])
@login_required
def meals_list():
    meals = Meal.query.filter_by(user_id=current_user.id).all()

    if meals:
        result = [
            {"id": meal.id, 
             "name": meal.name, 
             "description": meal.description, 
             "date": meal.date, 
             "time": meal.time, 
             "in_diet": meal.in_diet
             }

            for meal in meals
        ]
        return jsonify(result), 200
    
    return jsonify({"message": "Nenhuma refeição encontrada."}), 404

@app.route("/user/meal/<int:meal_id>", methods=['GET'])
@login_required
def meal(meal_id):
    print(f"Usuário autenticado: {current_user.id}")
    meal = Meal.query.filter_by(id=meal_id, user_id=current_user.id).first()

    if meal:
        result_meal = {
            "id": meal.id,
            "name": meal.name,
            "description": meal.description,
            "date": meal.date,
            "time": meal.time,
            "in_diet": meal.in_diet                   
            }
        return jsonify(result_meal)
    return jsonify({"message": "Refeição não encontrada"}), 404

@app.route("/user/edit-meal/<int:meal_id>", methods=['PUT'])
@login_required
def edit_meal(meal_id):
    meal = Meal.query.filter_by(id=meal_id, user_id=current_user.id).first()

    if meal:
    
        data = request.get_json()
        meal.name = data['name']
        meal.description = data['description']
        meal.date = data['date']
        meal.time = data['time']
        meal.in_diet = data['in_diet']

        db.session.commit()
        print(meal)
        return jsonify({"message": "Refeição atualizada com sucesso"})
    else:
        return jsonify({"message": "Refeição não encontrada"}), 400



    


@app.route("/test", methods=["GET"])
def test():
    return "Testando a Rota"

if __name__ == '__main__':
    app.run(debug=True)
