from flask import Flask, request, jsonify
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from src.database.db import db
from src.models.user_table import User
from src.hours_check.hours_check import check_hours

app = Flask(__name__)
app.config['SECRET_KEY'] = "key"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    user_response = User()
    user_result = user_response.user_login(data)
    
    if user_result.get("success"):
        user = User.query.filter_by(username=user_result['success']['username']).first()
        login_user(user,)
        return jsonify(user_result), user_result['status_code']
    
    return jsonify(user_result), user_result['status_code']

@app.route("/admin/create", methods=['POST'])
@login_required
def create_user():
    if current_user.role != "admin":
        return jsonify({"error": {
            "data": {
                "message": "Acesso negado"
            }
        }}), 403
    
    data = request.get_json()
    user = User()
    create_user = user.create_user(data)
    return jsonify(create_user), create_user['status_code']

@app.route("/user/check_session", methods=['POST'])
@login_required
def check_session():
    userId = current_user.id
    check = check_hours(userId)
    return jsonify(check)

@app.route("/logout", methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"success": {
        "message": "Usuario deslogado"
    }}), 200