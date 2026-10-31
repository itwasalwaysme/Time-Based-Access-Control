from typing import Dict
from src.database.db import db
from flask_login import UserMixin
from datetime import datetime, timedelta
import uuid

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    key = db.Column(db.String(150), unique=True, nullable=False)
    access_time = db.Column(db.DATETIME)
    role = db.Column(db.String(10), default='user')
    is_active = db.Column(db.Boolean, default=True)

    def __validate_create_body(self, body: Dict) -> Dict:
        if "username" not in body or "access_time" not in body or "role" not in body:
            return {
                "error": {
                    "message": "Campos obrigatórios invalidos"
                },
                "status_code": 403
            }

        if "username" is None or "access_time" is None or "role" is None:
            return {
                "error": {
                    "message": "Nenhum campo deve ficar vazio",
                },
                "status_code": 400
            }   

        find_user = User.query.filter_by(username=body['username']).first()

        if find_user:
            return {
                "error": {
                    "message": "Username não disponivel"
                },
                "status_code": 409
            }
        
        return {
            "success": {
                "username": body.get("username"),
                "access_time": body.get("access_time"),
                "message": "Usuario cadastrado"
            },
            "status_code": 200
        }

    def __validate_login_body(self, data: Dict):
        if "key" not in data or "key" is None:
            return {
                "error": {
                    "message": "Campos obrigatórios invalidos"
                },
                "status_code": 403
            }

        user = User.query.filter_by(key=data['key']).first()

        if user:
            return {
                "success": {
                    "username": user.username,
                    "message": "Usuario encontrado"
                },
                "status_code": 200
            }

        return {
            "errors": {
                "data": {
                    "message": "Key inválida"
                },
            },
            "status_code": 400
        }
    
    def create_user(self, data: Dict):
        validate = self.__validate_create_body(data)

        if validate.get("success"):
            time = datetime.now() + timedelta(hours=data['access_time'])
            user = User(username=data['username'], key=str(uuid.uuid4()), access_time=time, role='user')
            db.session.add(user)
            db.session.commit()
            return validate

        return validate

    def user_login(self, data: Dict):
        validate = self.__validate_login_body(data)

        if validate.get("success"):
            return validate

        return validate