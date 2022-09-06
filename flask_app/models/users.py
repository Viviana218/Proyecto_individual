from flask_app.config.mysqlconnection import  connectToMySQL

import re #Importando Expresiones regulares
#Expresion Regular de Email
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

from flask import flash

class User:

    def __init__(self, data):
        self.id = data['id']
        self.nombres = data['nombres']
        self.apellidos = data['apellidos']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO users (nombres, apellidos, email, password) VALUES (%(nombres)s, %(apellidos)s, %(email)s, %(password)s)"
        result = connectToMySQL('salud').query_db(query, formulario) #me regresan el nuevo ID de la persona registrada
        #result = 5
        return result

    @staticmethod
    def valida_usuario(formulario): #El formulario es 
        #formulario = { DICCIONARIO
        #   first_name = "Elena",    
        #   last_name = "De Troya",    
        #   email = "elena@codingdojo.com",    
        #   password = "123",    
        #   confirm_password = "234",    
        #}

        es_valido = True #Siempre va ser true hasta que sea false por
        #la sentencia if.
        
        errores=[]

        #Validar que el nombre y el apellido no esten vacios
        if len(formulario['nombres']) < 3:
            #flash('Nombres debe tener un valor ingresado', 'registro')
            errores.append('Nombres debe tener al menos 3 caracteres')
            es_valido = False

        if len(formulario['apellidos']) < 3:
            #flash('Apellidos debe tener un valor ingresado', 'registro')
            errores.append('Apellido debe tener al menos 3 caracteres')
            es_valido = False

        #Verificar que el email tenga formato correcto - EXPRESIONES REGULARES
        if not EMAIL_REGEX.match(formulario['email']):
            #flash('E-mail inválido', 'registro')
            errores.append('E-mail inválido')
            es_valido = False
        
        #Password con al menos 8 caracteres
        if len(formulario['password']) < 8:
            #flash('Contraseña debe tener al menos 8 caracteres', 'registro')
            errores.append('Contraseña debe tener al menos 8 caracteres')
            es_valido = False
        
        #Verificamos que las contraseñas coincidan
        if formulario['password'] != formulario['confirm_password']:
            #flash('Contraseñas no coinciden', 'registro')
            errores.append('Contraseñas no coinciden')
            es_valido = False
        
        #Consultar si ya existe ese correo electrónico
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('salud').query_db(query, formulario)
        if len(results) >= 1:
            #flash('E-mail registrado previamente', 'registro')
            errores.append('E-mail registrado previamente')
            es_valido = False
        
        return (es_valido, errores)


    @classmethod
    def get_by_email(cls, formulario):
        #formulario = {
        #      email: elena@cd.com
        #      password: 123
        #}
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('salud').query_db(query, formulario) #Los SELECT regresan una lista
        if len(result) < 1: #NO existe registro con ese correo
            #result = []
            return False
        else:
            #result = [
            #    {id: 1, first_name: elena, last_name:de troya.....} -> POSICION 0
            #]
            user = cls(result[0])  #User({id: 1, first_name: elena, last_name:de troya.....})
            return user
    
    @classmethod
    def get_by_id(cls, formulario):
        #formulario = {id: 4}
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('salud').query_db(query, formulario) #RECIBIMOS UNA LISTA
        user = cls(result[0]) #creamos una instancia de usuario
        return user