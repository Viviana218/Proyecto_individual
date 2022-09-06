from flask import render_template, redirect, session, request, flash
from flask_app import app

#Importación del modelo
from flask_app.models.users import User
from flask_app.models.imagenes import Imagen

from werkzeug.utils import secure_filename
import os

@app.route('/imagenes')
def imagenes():
    if 'user_id' not in session:
        return redirect('/')

    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario)
    imagenes = Imagen.get_all(formulario)

    return render_template('imagenes.html', user=user, imagenes=imagenes)

@app.route('/nueva_img')
def nueva_imagen():
    if 'user_id' not in session: #Comprobamos que el usuario haya iniciado sesiónh
        return redirect('/')

    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario) #Instancia del usuario que inicio sesión

    return render_template('nueva_img.html', user=user)


@app.route('/add_img', methods=['POST'])
def add_img():
    if 'user_id' not in session: #Comprobamos que el usuario haya iniciado sesión
        return redirect('/')

    if not Imagen.valida_imagen(request.form): #llama a la función de valida_cita enviándole el formulario, comprueba que sea valido 
        return redirect('/nueva_img')

    if 'documento1' not in request.files:
        flash('Documento no encontrado', 'examen')
        return redirect('/nueva_img')

    documento1 = request.files['documento1']

    if documento1.filename == "":
        flash ('Nombre de documento vacío', 'examen')
        return redirect ('/nueva_img')   

    nombre_documento = secure_filename(documento1.filename)    
    documento1.save(os.path.join(app.config ['UPLOAD_FOLDER'],nombre_documento)) 
   
    formulario = {
        'fecha1' : request.form['fecha1'],
        'descripcion1' : request.form['descripcion1'],
        'link' : request.form ['link'],
        'user_id' : request.form['user_id'],
        'documento1' : nombre_documento
    }

    Imagen.save(formulario)
    return redirect('/imagenes')



@app.route('/editar_img/<int:id>') #a través de la URL recibimos el ID de la cita
def edit_img(id):
    if 'user_id' not in session: #Comprobamos que el usuario haya iniciado sesión
        return redirect('/')

    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario) #Instancia del usuario que inicio sesión

    #La instancia de la cita que queremos editar
    formulario_img = {"id": id}
    imagen = Imagen.get_by_id(formulario_img)

    return render_template('edit_img.html', user=user, imagen=imagen)


@app.route('/update_img', methods=['POST'])
def update_img():
    if 'user_id' not in session: #Comprobamos que el usuario haya iniciado sesión
        return redirect('/')
    
    if not Imagen.valida_imagen(request.form): #llama a la función de valida_cita enviándole el formulario, comprueba que sea valido 
        return redirect('/editar_img/'+request.form['id'])
    
    nombre_documento1 = ''

    if 'documento1' in request.files:
        documento1 = request.files['documento1']

        if documento1.filename != "":
            nombre_documento1 = secure_filename(documento1.filename)    
            documento1.save(os.path.join(app.config ['UPLOAD_FOLDER'],nombre_documento1))
    
    formulario = {
        'fecha1' : request.form['fecha1'],
        'descripcion1' : request.form['descripcion1'],
        'documento1' : nombre_documento1,
        'link' : request.form['link'],
        'user_id' : request.form['user_id'],
        'id': request.form['id']
    }

    Imagen.update(formulario)
    return redirect('/imagenes')



@app.route('/borrar_img/<int:id>')
def borrar_img(id):
    if 'user_id' not in session: #Solo puede ver la página si ya inició sesión 
        return redirect('/')
    
    formulario = {"id": id}
    Imagen.delete(formulario)

    return redirect('/imagenes')