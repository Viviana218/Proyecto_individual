from flask_app.config.mysqlconnection import  connectToMySQL
from flask import flash

class Orden:

    def __init__(self, data):
        self.id = data['id']
        self.servicio = data['servicio']
        self.prestador = data['prestador']
        self.telefonos = data['telefonos']
        self.direccion = data['direccion']
        self.documento3 = data['documento']
        self.solicitada = data['solicitada']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

       
    @staticmethod
    def valida_orden(formulario):
        es_valido = True

        if formulario['servicio'] == "":
            flash('Debe ingresar el tipo de servicio', 'orden')
            es_valido = False

        if formulario['prestador'] == "":
            flash('El campo debe contener información sobre el prestador', 'orden')
            es_valido = False

        if formulario['telefonos'] == "":
            flash('El campo debe contener los telefonos del prestador', 'orden')
            es_valido = False
        
        if formulario['direccion'] == "":
            flash('El campo debe contener la direccion', 'orden')
            es_valido = False
        
        if formulario['solicitada'] == "":
            flash('Debe indicar si la cita ya fue solicitada', 'orden')
            es_valido = False
        
        return es_valido



    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO ordenes (servicio, prestador, telefonos, direccion, documento, solicitada, user_id) VALUES (%(servicio)s, %(prestador)s, %(telefonos)s, %(direccion)s, %(documento3)s, %(solicitada)s, %(user_id)s) "
        result = connectToMySQL('salud').query_db(query, formulario)
        return result

    @classmethod
    def update(cls, formulario):
        if(formulario['documento3'] != ''):
            query = "UPDATE ordenes SET servicio=%(servicio)s, prestador=%(prestador)s, telefonos=%(telefonos)s, direccion=%(direccion)s, documento=%(documento3)s, solicitada=%(solicitada)s WHERE id = %(id)s"
        else:
            query = "UPDATE ordenes SET servicio=%(servicio)s, prestador=%(prestador)s, telefonos=%(telefonos)s, direccion=%(direccion)s, solicitada=%(solicitada)s WHERE id = %(id)s"
        result = connectToMySQL('salud').query_db(query, formulario)
        return result

    @classmethod
    def delete(cls, formulario): #Recibe formulario con id de receta a borrar
        query = "DELETE FROM ordenes WHERE id = %(id)s"
        result = connectToMySQL('salud').query_db(query, formulario)
        return result
 

    @classmethod
    def get_all(cls, formulario):
        query = "SELECT ordenes.*, servicio FROM ordenes LEFT JOIN users ON users.id = ordenes.user_id WHERE users.id=%(id)s ORDER BY created_at DESC"
        results = connectToMySQL('salud').query_db(query, formulario) #Lista de diccionarios 
        ordenes = []
        for orden in results:
            #cita = diccionario
            ordenes.append(cls(orden)) #1.- cls(cita) me crea una instancia en base al diccionario, 2.- Agrego la instancia a mi lista de citas
        return ordenes


    @classmethod
    def get_by_id(cls, formulario): #formulario = {id: 1}
        query = "SELECT ordenes.*, servicio FROM ordenes LEFT JOIN users ON users.id = ordenes.user_id WHERE ordenes.id = %(id)s"
        result = connectToMySQL('salud').query_db(query, formulario) #Lista de diccionarios
        orden = cls(result[0])
        return orden