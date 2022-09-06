#EJECUTA nuestra aplicación
from flask_app import app

#Importando mi controlador
from flask_app.controllers import examenes_controller, historias_controller, imagenes_controller, ordenes_controller, users_controller, pendientes_controller

#pipenv install flask pymysql flask-bcrypt
#pipenv shell
#python server.py -> python3 py python

if __name__=="__main__":
    app.run(debug=True)