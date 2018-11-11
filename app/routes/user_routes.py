from app import app
from app.controllers.user_controller import User_Controller

   
@app.route('/api/v1/users', methods =['POST'])
def create_user():
    return User_Controller.create_user()