from flask import render_template, redirect, session, request, flash
from flask_app import app

#Importación del modelo
from flask_app.models.users import User
from flask_app.models.pendientes import Pendiente

from werkzeug.utils import secure_filename
import os

@app.route('/nuevo_pendiente')
def nuevo_pendiente():
    if 'user_id' not in session: #Comprobamos que el usuario haya iniciado sesiónh
        return redirect('/')

    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario) #Instancia del usuario que inicio sesión

    return render_template('nuevo_pendiente.html', user=user)


@app.route('/add_pend', methods=['POST'])
def add_pend():
    if 'user_id' not in session: #Comprobamos que el usuario haya iniciado sesión
        return redirect('/')

    if not Pendiente.valida_pendiente(request.form): #llama a la función de valida_cita enviándole el formulario, comprueba que sea valido 
        return redirect('/nuevo_pendiente')

    
    Pendiente.save(request.form)
    return redirect('/dashboard')

    



@app.route('/editar_pend/<int:id>') #a través de la URL recibimos el ID de la cita
def edit_pend(id):
    if 'user_id' not in session: #Comprobamos que el usuario haya iniciado sesión
        return redirect('/')

    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario) #Instancia del usuario que inicio sesión

    #La instancia de la cita que queremos editar
    formulario_pend = {"id": id}
    pendiente = Pendiente.get_by_id(formulario_pend)

    return render_template('edit_pend.html', user=user, pendiente=pendiente)


@app.route('/update_pend', methods=['POST'])
def update_pend():
    if 'user_id' not in session: #Comprobamos que el usuario haya iniciado sesión
        return redirect('/')
    
    if not Pendiente.valida_pendiente(request.form): #llama a la función de valida_cita enviándole el formulario, comprueba que sea valido 
        return redirect('/editar_pend/'+request.form['id'])
    
    Pendiente.update(request.form)
    return redirect('/dashboard')


@app.route('/borrar_pend/<int:id>')
def borrar_pend(id):
    if 'user_id' not in session: #Solo puede ver la página si ya inició sesión 
        return redirect('/')
    
    formulario = {"id": id}
    Pendiente.delete(formulario)

    return redirect('/dashboard')