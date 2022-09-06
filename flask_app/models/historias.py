from flask_app.config.mysqlconnection import  connectToMySQL
from flask import flash

class Historia:

    def __init__(self, data):
        self.id = data['id']
        self.fecha2 = data['fecha']
        self.origen = data['origen']
        self.documento2 = data['documento']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    
    @staticmethod
    def valida_historia(formulario):
        es_valido = True

        if formulario['fecha2'] == "":
            flash('Debe ingresar una fecha', 'hc')
            es_valido = False

        if formulario['origen'] == "":
            flash('Debe indicar donde se generó la Historia Clínica', 'hc')
            es_valido = False
        
        return es_valido
    


    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO historias (fecha, origen, documento, user_id) VALUES (%(fecha2)s, %(origen)s, %(documento2)s,%(user_id)s) "
        result = connectToMySQL('salud').query_db(query, formulario)
        return result

    @classmethod
    def update(cls, formulario):
        if(formulario['documento2'] != ''):
            query = "UPDATE historias SET fecha=%(fecha2)s, origen=%(origen)s, documento=%(documento2)s WHERE id = %(id)s"
        else:
            query = "UPDATE historias SET fecha=%(fecha2)s, origen=%(origen)s WHERE id = %(id)s"
        result = connectToMySQL('salud').query_db(query, formulario)
        return result

    @classmethod
    def delete(cls, formulario): #Recibe formulario con id de receta a borrar
        query = "DELETE FROM historias WHERE id = %(id)s"
        result = connectToMySQL('salud').query_db(query, formulario)
        return result
 

    @classmethod
    def get_all(cls, formulario):
        query = "SELECT historias.*, fecha FROM historias LEFT JOIN users ON users.id = historias.user_id WHERE users.id=%(id)s ORDER BY fecha DESC"
        results = connectToMySQL('salud').query_db(query, formulario) #Lista de diccionarios 
        historias = []
        for historia in results:
            #cita = diccionario
            historias.append(cls(historia)) #1.- cls(cita) me crea una instancia en base al diccionario, 2.- Agrego la instancia a mi lista de citas

        return historias


    @classmethod
    def get_by_id(cls, formulario): #formulario = {id: 1}
        query = "SELECT historias.*, fecha FROM historias LEFT JOIN users ON users.id = historias.user_id WHERE historias.id = %(id)s"
        result = connectToMySQL('salud').query_db(query, formulario) #Lista de diccionarios
        historia = cls(result[0])
        return historia