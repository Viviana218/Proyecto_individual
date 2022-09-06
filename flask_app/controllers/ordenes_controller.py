from flask import render_template, redirect, session, request, flash
from flask_app import app

#Importación del modelo
from flask_app.models.users import User
from flask_app.models.ordenes import Orden

from werkzeug.utils import secure_filename
import os

@app.route('/ordenes')
def ordenes():
    if 'user_id' not in session:
        return redirect('/')

    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario)
    ordenes = Orden.get_all(formulario)

    return render_template('ordenes.html', user=user, ordenes=ordenes)

@app.route('/nueva_orden')
def nueva_orden():
    if 'user_id' not in session: #Comprobamos que el usuario haya iniciado sesiónh
        return redirect('/')

    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario) #Instancia del usuario que inicio sesión

    return render_template('nueva_orden.html', user=user)


@app.route('/add_om', methods=['POST'])
def add_om():
    if 'user_id' not in session: #Comprobamos que el usuario haya iniciado sesión
        return redirect('/')

    if not Orden.valida_orden(request.form): #llama a la función de valida_cita enviándole el formulario, comprueba que sea valido 
        return redirect('/nueva_orden')
    
    if 'documento3' not in request.files:
        flash('Documento no encontrado', 'orden')
        return redirect('/nueva_orden')

    documento3 = request.files['documento3']

    if documento3.filename == "":
        flash ('Nombre de documento vacío', 'orden')
        return redirect ('/nueva_orden')   

    nombre_documento = secure_filename(documento3.filename)    
    documento3.save(os.path.join(app.config ['UPLOAD_FOLDER'],nombre_documento)) 
   
    formulario = {
        'servicio' : request.form['servicio'],
        'prestador' : request.form['prestador'],
        'telefonos' : request.form['telefonos'],
        'direccion' : request.form['direccion'],
        'solicitada' : request.form['solicitada'],
        'user_id' : request.form['user_id'],
        'documento3' : nombre_documento
    }

    Orden.save(formulario)
    return redirect('/ordenes')



@app.route('/editar_om/<int:id>') #a través de la URL recibimos el ID de la cita
def edit_com(id):
    if 'user_id' not in session: #Comprobamos que el usuario haya iniciado sesión
        return redirect('/')

    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario) #Instancia del usuario que inicio sesión

    #La instancia de la cita que queremos editar
    formulario_om = {"id": id}
    orden = Orden.get_by_id(formulario_om)

    return render_template('edit_om.html', user=user, orden=orden)


@app.route('/update_om', methods=['POST'])
def update_cita():
    if 'user_id' not in session: #Comprobamos que el usuario haya iniciado sesión
        return redirect('/')
    
    if not Orden.valida_orden(request.form): #llama a la función de valida_cita enviándole el formulario, comprueba que sea valido 
        return redirect('/editar_om'+request.form['id'])
    
    nombre_documento3 = ''

    if 'documento3' in request.files:
        documento3 = request.files['documento3']

        if documento3.filename != "":
            nombre_documento3 = secure_filename(documento3.filename)    
            documento3.save(os.path.join(app.config ['UPLOAD_FOLDER'],nombre_documento3)) 

    formulario = {
        'servicio' : request.form['servicio'],
        'prestador' : request.form['prestador'],
        'telefonos' : request.form['telefonos'],
        'direccion' : request.form['direccion'],
        'solicitada' : request.form['solicitada'],
        'user_id' : request.form['user_id'],
        'documento3' : nombre_documento3,
        'id': request.form['id']
    }

    Orden.update(formulario)
    return redirect('/ordenes')



@app.route('/borrar_om/<int:id>')
def borrar_om(id):
    if 'user_id' not in session: #Solo puede ver la página si ya inició sesión 
        return redirect('/')
    
    formulario = {"id": id}
    Orden.delete(formulario)

    return redirect('/ordenes')