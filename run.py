from app import app
from app.controllers.db import DatabaseConnection

db = DatabaseConnection()
db.setUp()

if __name__ == '__main__':
    app.run(debug=True)   