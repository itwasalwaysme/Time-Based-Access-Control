from ..models.user_table import User
from datetime import datetime
from src.database.db import db

def check_hours(id):
    user = User.query.get(id)

    if user:
        if datetime.now() > user.access_time:
            user.is_active = False
            db.session.commit()
            return {
                "message": "Tempo esgotado",
                "is_active": user.is_active
            }

        return {
            "data": {
                "user": user.username,
                "access_time": user.access_time,
                "is_active": user.is_active
            }
        }

    return {
        "error": {
            "data": {
                "message": "Nenhum usuario encontrado com este ID"
            },
            "status_code": 404
        }
    }