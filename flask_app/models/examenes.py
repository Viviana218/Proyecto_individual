from flask_app.config.mysqlconnection import  connectToMySQL
from flask import flash

class Examen:

    def __init__(self, data):
        self.id = data['id']
        self.fecha = data['fecha']
        self.descripcion = data['descripcion']
        self.documento = data['documento']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

       
    @staticmethod
    def valida_examen(formulario):
        es_valido = True

        if formulario['fecha'] == "":
            flash('Debe ingresar una fecha', 'examen')
            es_valido = False

        if formulario['descripcion'] == "":
            flash('El campo debe contener una descripción', 'examen')
            es_valido = False
        
        return es_valido



    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO examenes (fecha, descripcion, documento, user_id) VALUES (%(fecha)s, %(descripcion)s, %(documento)s,%(user_id)s) "
        result = connectToMySQL('salud').query_db(query, formulario)
        return result

    @classmethod
    def update(cls, formulario):

        if(formulario['documento'] != ''):
            query = "UPDATE examenes SET fecha=%(fecha)s, descripcion=%(descripcion)s, documento=%(documento)s WHERE id = %(id)s"
        else:
             query = "UPDATE examenes SET fecha=%(fecha)s, descripcion=%(descripcion)s WHERE id = %(id)s"
        result = connectToMySQL('salud').query_db(query, formulario)
        return result

    @classmethod
    def delete(cls, formulario): #Recibe formulario con id de receta a borrar
        query = "DELETE FROM examenes WHERE id = %(id)s"
        result = connectToMySQL('salud').query_db(query, formulario)
        return result
 

    @classmethod
    def get_all(cls, formulario):
        query = "SELECT examenes.*, fecha FROM examenes LEFT JOIN users ON users.id = examenes.user_id WHERE users.id=%(id)s ORDER BY fecha DESC"
        results = connectToMySQL('salud').query_db(query, formulario) #Lista de diccionarios 
        examenes = []
        for examen in results:
            #cita = diccionario
            examenes.append(cls(examen)) #1.- cls(cita) me crea una instancia en base al diccionario, 2.- Agrego la instancia a mi lista de citas

        return examenes


    @classmethod
    def get_by_id(cls, formulario): #formulario = {id: 1}
        query = "SELECT examenes.*, fecha FROM examenes LEFT JOIN users ON users.id = examenes.user_id WHERE examenes.id = %(id)s"
        result = connectToMySQL('salud').query_db(query, formulario) #Lista de diccionarios
        examen = cls(result[0])
        return examen