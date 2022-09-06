from flask import render_template, redirect, session, request, flash
from flask_app import app

#Importación del modelo
from flask_app.models.users import User
from flask_app.models.historias import Historia

from werkzeug.utils import secure_filename
import os

@app.route('/historias')
def historias():
    if 'user_id' not in session:
        return redirect('/')

    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario)
    historias = Historia.get_all(formulario)

    return render_template('historias.html', user=user, historias=historias)

@app.route('/nueva_hc')
def nueva_hc():
    if 'user_id' not in session: #Comprobamos que el usuario haya iniciado sesiónh
        return redirect('/')

    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario) #Instancia del usuario que inicio sesión

    return render_template('nueva_hc.html', user=user)


@app.route('/add_hc', methods=['POST'])
def add_hc():
    if 'user_id' not in session: #Comprobamos que el usuario haya iniciado sesión
        return redirect('/')
    
    if not Historia.valida_historia(request.form): #llama a la función de valida_cita enviándole el formulario, comprueba que sea valido 
        return redirect('/nueva_hc')

    if 'documento2' not in request.files:
        flash('Documento no encontrado', 'hc')
        return redirect('/nueva_hc')

    documento2 = request.files['documento2']

    if documento2.filename == "":
        flash ('Nombre de documento vacío', 'hc')
        return redirect ('/nueva_hc')   

    nombre_documento = secure_filename(documento2.filename)    
    documento2.save(os.path.join(app.config ['UPLOAD_FOLDER'],nombre_documento)) 
   
    formulario = {
        'fecha2' : request.form['fecha2'],
        'origen' : request.form['origen'],
        'user_id' : request.form['user_id'],
        'documento2' : nombre_documento
    }

    Historia.save(formulario)
    return redirect('/historias')



@app.route('/editar_hc/<int:id>') #a través de la URL recibimos el ID de la cita
def editar_hc(id):
    if 'user_id' not in session: #Comprobamos que el usuario haya iniciado sesión
        return redirect('/')

    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario) #Instancia del usuario que inicio sesión

    #La instancia de la cita que queremos editar
    formulario_historia = {"id": id}
    historia = Historia.get_by_id(formulario_historia)

    return render_template('edit_hc.html', user=user, historia=historia)


@app.route('/update_hc', methods=['POST'])
def update_hc():
    if 'user_id' not in session: #Comprobamos que el usuario haya iniciado sesión
        return redirect('/')
    
    if not Historia.valida_historia(request.form): #llama a la función de valida_cita enviándole el formulario, comprueba que sea valido 
        return redirect('/edit_hc/'+request.form['id'])

    nombre_documento2 = ''

    if 'documento2' in request.files:
        documento2 = request.files ['documento2']
        

        if documento2.filename != "":
            nombre_documento2 = secure_filename(documento2.filename)
            documento2.save(os.path.join(app.config ['UPLOAD_FOLDER'],nombre_documento2)) 
              
   
    formulario = {
        'fecha2' : request.form['fecha2'],
        'origen' : request.form['origen'],
        'user_id' : request.form['user_id'],
        'documento2' : nombre_documento2,
        'id': request.form ['id']
    }

    Historia.update(formulario)
    return redirect('/historias')



@app.route('/borrar_hc/<int:id>')
def borrar_hc(id):
    if 'user_id' not in session: #Solo puede ver la página si ya inició sesión 
        return redirect('/')
    
    formulario = {"id": id}
    Historia.delete(formulario)

    return redirect('/historias')