from flask import render_template, redirect, session, request, flash
from flask_app import app

#Importación del modelo
from flask_app.models.users import User
from flask_app.models.examenes import Examen

from werkzeug.utils import secure_filename
import os

@app.route('/examenes')
def examenes():
    if 'user_id' not in session:
        return redirect('/')

    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario)
    examenes = Examen.get_all(formulario)

    return render_template('examenes.html', user=user, examenes=examenes)

@app.route('/nuevo_examen')
def nuevo_examen():
    if 'user_id' not in session: #Comprobamos que el usuario haya iniciado sesiónh
        return redirect('/')

    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario) #Instancia del usuario que inicio sesión

    return render_template('nuevo_lab.html', user=user)


@app.route('/add_lab', methods=['POST'])
def add_lab():
    if 'user_id' not in session: #Comprobamos que el usuario haya iniciado sesión
        return redirect('/')

    if not Examen.valida_examen(request.form): #llama a la función de valida_cita enviándole el formulario, comprueba que sea valido 
        return redirect('/nuevo_examen')

    if 'documento' not in request.files:
        flash('Documento no encontrado', 'examen')
        return redirect('/nuevo_examen')

    documento = request.files['documento']

    if documento.filename == "":
        flash ('Nombre de documento vacío', 'examen')
        return redirect ('/nuevo_examen')   

    nombre_documento = secure_filename(documento.filename)    
    documento.save(os.path.join(app.config ['UPLOAD_FOLDER'],nombre_documento)) 
   
    formulario = {
        'fecha' : request.form['fecha'],
        'descripcion' : request.form['descripcion'],
        'user_id' : request.form['user_id'],
        'documento' : nombre_documento
    }

    Examen.save(formulario)
    return redirect('/examenes')



@app.route('/editar_lab/<int:id>') #a través de la URL recibimos el ID de la cita
def edit_lab(id):
    if 'user_id' not in session: #Comprobamos que el usuario haya iniciado sesión
        return redirect('/')

    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario) #Instancia del usuario que inicio sesión

    #La instancia de la cita que queremos editar
    formulario_lab = {"id": id}
    examen = Examen.get_by_id(formulario_lab)

    return render_template('edit_lab.html', user=user, examen=examen)


@app.route('/update_lab', methods=['POST'])
def update_lab():
    if 'user_id' not in session: #Comprobamos que el usuario haya iniciado sesión
        return redirect('/')
    
    if not Examen.valida_examen(request.form): #llama a la función de valida_cita enviándole el formulario, comprueba que sea valido 
        return redirect('/editar_lab/'+request.form['id'])

    nombre_documento = ''
    
    if 'documento' in request.files:
        documento = request.files['documento']

        if documento.filename != "":
            nombre_documento = secure_filename(documento.filename)    
            documento.save(os.path.join(app.config ['UPLOAD_FOLDER'],nombre_documento)) 
   
    formulario = {
        'fecha' : request.form['fecha'],
        'descripcion' : request.form['descripcion'],
        'user_id' : request.form['user_id'],
        'documento' : nombre_documento,
        'id': request.form['id']
    }

    
    Examen.update(formulario)
    return redirect('/examenes')

@app.route('/borrar_lab/<int:id>')
def borrar_lab(id):
    if 'user_id' not in session: #Solo puede ver la página si ya inició sesión 
        return redirect('/')
    
    formulario = {"id": id}
    Examen.delete(formulario)

    return redirect('/examenes')