from email import message
from flask import render_template, redirect, session, request, flash, jsonify
from flask_app import app

#Importación del modelo
from flask_app.models.users import User
from flask_app.models.pendientes import Pendiente

#Importación BCrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/') #Pagina principal renderizando index
def index():
    return render_template('index.html')

@app.route('/nuevo_usuario')
def registro():
    return render_template('nuevo_usuario.html')


@app.route('/add_usuario', methods=['POST'])
def registrate():
    #Validar la información ingresada
    validacion = User.valida_usuario(request.form)
    if not validacion[0]: 
        return jsonify(message=validacion[1][0])
    #Aca se encripta la contraseña.
    pwd = bcrypt.generate_password_hash(request.form['password']) #Encriptamos el password del usuario

    #formulario que se va a estar comparando con el request.form 
    formulario = {
        'nombres': request.form['nombres'],
        'apellidos': request.form['apellidos'],
        'email': request.form['email'],
        'password': pwd
    }

    #request.form = FORMULARIO HTML
    id = User.save(formulario) #Recibo el identificador de mi nuevo usuario

    session['user_id'] = id #Se guarda en sesion el id de usuario.

    return jsonify(message="Correcto") #Se retorna

@app.route('/login', methods=['POST'])
def login():
    #Verificar que el email EXISTA
    #request.form RECIBIMOS DE HTML
    #request.form = {email: elena@cd.com, password: 123}
    user = User.get_by_email(request.form) #Recibiendo una instancia de usuario o Falso

    if not user: #Si no hay nada en usuario.
        flash('E-mail no encontrado', 'login')
        return redirect('/')

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Password incorrecto', 'login')
        return redirect('/')

    session['user_id'] = user.id

    return redirect('/dashboard')



@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario)
    pendientes = Pendiente.get_all(formulario)

    return render_template('dashboard.html', user=user, pendientes=pendientes)


    

@app.route('/index')
def logout():
    session.clear()
    return redirect('/')