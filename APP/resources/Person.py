from flask_restful import Resource
from flask import jsonify, request

from utils.Cursor import Cursor
from utils.Common import formatResponse
from config.db import mysql

class Persons(Resource):
    
    def get(self):
        persons = None
        columns = None        
        
        with Cursor(mysql) as db:
            query = "SELECT ID, IDENTIFICACION, NOMBRE, APELLIDO FROM PERSONAS"
            db.execute(query)
            columns = db.description
            persons = db.fetchall()        
        
        info = {
            "success": True if len(persons) > 0 else False,
            "data": formatResponse(columns, persons)
        }
                
        return info

class Person(Resource):
    
    def get(self, id):
        
        info = {
            "success": False,
            "data": ""
        }
        
        person = None
        columns = None        
        
        with Cursor(mysql) as db:
            query = "SELECT ID, IDENTIFICACION, NOMBRE, APELLIDO FROM PERSONAS WHERE ID = %s"
            db.execute(query, (id, ))
            columns = db.description
            person = db.fetchall()        
        
        if len(person) > 0:
            info["success"] = True
            info["data"] = formatResponse(columns, person)        
        else:
            info["data"] = [None]

        return info
    
    def post(self):
        
        info = {
            "success" : False,
            "message" : ""
        }
        
        try:
            with Cursor(mysql) as db:
                query = "INSERT INTO PERSONAS(IDENTIFICACION, NOMBRE, APELLIDO) VALUES (%s, %s, %s)"            
                
                db.execute(query, (
                    request.json["identificacion"],
                    request.json["nombre"],
                    request.json["apellido"]
                ))
                
                info["success"] = True
                info["message"] = "created person"
                
                query = "SELECT ID, IDENTIFICACION, NOMBRE, APELLIDO FROM PERSONAS WHERE ID = (SELECT MAX(ID) FROM PERSONAS)"
                db.execute(query)
                columns = db.description
                person = db.fetchall()
                
                info["data"] = formatResponse(columns, person)
                return info
            
        except Exception as ex: 
            info["message"] = "error: " + str(ex)                
            return info
        
    
    def put(self, id):
        
        info = {
            "success" : False,
            "message" : ""
        }
        
        person = self.get(id)["data"][0]
        
        if person == None:
            info["message"] = "person does not exist"
            return info                     
        
        if "identificacion" in request.json and request.json["identificacion"] != person["identificacion"]:
            person["identificacion"] = request.json["identificacion"]
            
        
        if "nombre" in request.json and request.json["nombre"] != person["nombre"]:
            person["nombre"] = request.json["nombre"]
            
        if "apellido" in request.json and request.json["apellido"] != person["apellido"]:
            person["apellido"] = request.json["apellido"]
            
        try:
            with Cursor(mysql) as db:
                query = "UPDATE PERSONAS SET IDENTIFICACION = %s, NOMBRE = %s, APELLIDO = %s WHERE ID = %s"
                db.execute(query, (
                    person["identificacion"],
                    person["nombre"],
                    person["apellido"],
                    id,
                ))
                
                info["success"] = True
                info["message"] = "updated person"
                
                query = "SELECT ID, IDENTIFICACION, NOMBRE, APELLIDO FROM PERSONAS WHERE ID = %s"
                db.execute(query, (id, ))
                columns = db.description
                person = db.fetchall()
                
                person = formatResponse(columns, person)
                info["data"] = person
                
            return info
        
        except Exception as ex: 
            info["message"] = "error: " + str(ex) 
            
            return info
    
    def delete(self, id):
        
        person = self.get(id)["data"][0]
        
        info = {
            "success" : False,
            "message" : ""
        }
        
        if person == None:
            info["message"] = "person does not exist"
            return info
        
        try:
            with Cursor(mysql) as db:
                query = "DELETE FROM PERSONAS WHERE ID = %s"
                db.execute(query, (id, ))
                
                info["success"] = True
                info["message"] = "deleted person"
                info["data"] = person
                return info
        
        except Exception as ex:
            info["message"] = "error " + str(ex)
            return info
        