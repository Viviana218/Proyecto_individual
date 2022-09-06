from flask_app.config.mysqlconnection import  connectToMySQL
from flask import flash

class Imagen:

    def __init__(self, data):
        self.id = data['id']
        self.fecha1 = data['fecha']
        self.descripcion1 = data['descripcion']
        self.documento1 = data['documento']
        self.link = data['link']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

       
    @staticmethod
    def valida_imagen(formulario1):
        es_valido = True

        if formulario1['fecha1'] == "":
            flash('Debe ingresar una fecha', 'img')
            es_valido = False

        if formulario1['descripcion1'] == "":
            flash('El campo debe contener una descripción', 'img')
            es_valido = False
        
        
        return es_valido


    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO imagenes (fecha, descripcion, documento, link, user_id) VALUES (%(fecha1)s, %(descripcion1)s, %(documento1)s, %(link)s, %(user_id)s) "
        result = connectToMySQL('salud').query_db(query, formulario)
        return result

    @classmethod
    def update(cls, formulario):
        if(formulario['documento1'] != ''):
            query = "UPDATE imagenes SET fecha=%(fecha1)s, descripcion=%(descripcion1)s, documento=%(documento1)s, link=%(link)s WHERE id = %(id)s"
        else:
            query = "UPDATE imagenes SET fecha=%(fecha1)s, descripcion=%(descripcion1)s, link=%(link)s WHERE id = %(id)s"
        result = connectToMySQL('salud').query_db(query, formulario)
        return result

    @classmethod
    def delete(cls, formulario): #Recibe formulario con id de receta a borrar
        query = "DELETE FROM imagenes WHERE id = %(id)s"
        result = connectToMySQL('salud').query_db(query, formulario)
        return result
 

    @classmethod
    def get_all(cls, formulario):
        query = "SELECT imagenes.*, fecha FROM imagenes LEFT JOIN users ON users.id = imagenes.user_id WHERE users.id=%(id)s ORDER BY fecha DESC"
        results = connectToMySQL('salud').query_db(query, formulario) #Lista de diccionarios 
        imagenes = []
        for imagen in results:
            #cita = diccionario
            imagenes.append(cls(imagen)) #1.- cls(cita) me crea una instancia en base al diccionario, 2.- Agrego la instancia a mi lista de citas

        return imagenes


    @classmethod
    def get_by_id(cls, formulario): #formulario = {id: 1}
        query = "SELECT imagenes.*, fecha FROM imagenes LEFT JOIN users ON users.id = imagenes.user_id WHERE imagenes.id = %(id)s"
        result = connectToMySQL('salud').query_db(query, formulario) #Lista de diccionarios
        imagen = cls(result[0])
        return imagen