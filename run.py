from app import app
from src.models.user_table import User

if __name__ == "__main__":
    app.run(debug=True, port=3030)