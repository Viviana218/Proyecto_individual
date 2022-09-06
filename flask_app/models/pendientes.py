from flask_app.config.mysqlconnection import  connectToMySQL
from flask import flash

class Pendiente:

    def __init__(self, data):
        self.id = data['id']
        self.clase = data['clase']
        self.fecha3 = data['fecha']
        self.hora = data['hora']
        self.lugar = data['lugar']
        self.detalles = data['detalles']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

       
    @staticmethod
    def valida_pendiente(formulario):
        es_valido = True

        if formulario['clase'] == "":
            flash('Debe ingresar una clase', 'pendiente')
            es_valido = False
        
        if formulario['fecha3'] == "":
            flash('Debe ingresar una fecha', 'pendiente')
            es_valido = False

        if formulario['hora'] == "":
            flash('Debe ingresar una hora', 'pendiente')
            es_valido = False

        if formulario['lugar'] == "":
            flash('Debe ingresar el lugar', 'pendiente')
            es_valido = False
        
        return es_valido



    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO pendientes (clase, fecha, hora, lugar, detalles, user_id) VALUES (%(clase)s, %(fecha3)s,%(hora)s, %(lugar)s, %(detalles)s,%(user_id)s) "
        result = connectToMySQL('salud').query_db(query, formulario)
        return result

    @classmethod
    def update(cls, formulario):
        query = "UPDATE pendientes SET clase=%(clase)s, fecha=%(fecha3)s, hora=%(hora)s, lugar=%(lugar)s, detalles=%(detalles)s WHERE id = %(id)s"
        result = connectToMySQL('salud').query_db(query, formulario)
        return result

    @classmethod
    def delete(cls, formulario): #Recibe formulario con id de receta a borrar
        query = "DELETE FROM pendientes WHERE id = %(id)s"
        result = connectToMySQL('salud').query_db(query, formulario)
        return result
 

    @classmethod
    def get_all(cls, formulario):
        query = "SELECT pendientes.*, clase FROM pendientes LEFT JOIN users ON users.id = pendientes.user_id WHERE users.id=%(id)s ORDER BY fecha DESC"
        results = connectToMySQL('salud').query_db(query, formulario) #Lista de diccionarios 
        pendientes = []
        for pendiente in results:
            #cita = diccionario
            pendientes.append(cls(pendiente)) #1.- cls(cita) me crea una instancia en base al diccionario, 2.- Agrego la instancia a mi lista de citas

        return pendientes


    @classmethod
    def get_by_id(cls, formulario): #formulario = {id: 1}
        query = "SELECT pendientes.*, clase FROM pendientes LEFT JOIN users ON users.id = pendientes.user_id WHERE pendientes.id = %(id)s"
        result = connectToMySQL('salud').query_db(query, formulario) #Lista de diccionarios
        pendiente = cls(result[0])
        return pendiente