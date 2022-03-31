from flask_restful import Resource
from flask import request

from utils.Common import formatResponse
from utils.Cursor import Cursor
from config.db import mysql

class Vehicles(Resource):
    
    def get(self):
        
        vehicles = None
        columns = None
        
        with Cursor(mysql) as db:
            query = "SELECT ID, MARCA, MODELO, PATENTE, YEAR, ID_PERSONA_OWNER FROM VEHICULOS"
            db.execute(query)
            columns = db.description
            vehicles = db.fetchall()
        
        info = {
            "success" : True if len(vehicles) > 0 else False,
            "data" : formatResponse(columns, vehicles)
        }
        
        return info
    
class Vehicle(Resource):
    
    def get(self, id):
        
        info = {
            "success" : False,
            "data" : ""
        }
        
        vehicle = None
        columns = None
        
        with Cursor(mysql) as db:
            query = "SELECT ID, MARCA, MODELO, PATENTE, YEAR, ID_PERSONA_OWNER FROM VEHICULOS WHERE ID = %s"
            db.execute(query, (id, ))
            columns = db.description
            vehicle = db.fetchall()
            
        if len(vehicle) > 0:
            info["success"] = True
            info["data"] = formatResponse(columns, vehicle)
        else:
            info["data"] = [None]
        
        return info
    
    def post(self):
        
        info = {
            "success" : False,
            "message" : ""
        }
        
        with Cursor(mysql) as db:
            query = "INSERT INTO VEHICULOS(MARCA, MODELO, PATENTE, YEAR, ID_PERSONA_OWNER) VALUES (%s, %s, %s, %s, %s)"
            try:
                
                db.execute(query, (
                    request.json["marca"],
                    request.json["modelo"],
                    request.json["patente"],
                    request.json["year"],
                    request.json["id_persona_owner"]
                ))
                
                info["success"] = True
                info["message"] = "created vehicle"
                
                query = "SELECT ID, MARCA, MODELO, PATENTE, YEAR, ID_PERSONA_OWNER FROM VEHICULOS WHERE ID = (SELECT MAX(ID) FROM VEHICULOS)"
                
                db.execute(query)
                columns = db.description
                vehicle = db.fetchall()
                
                info["data"] = formatResponse(columns, vehicle)
                
                return info
                
            except Exception as ex:
                info["message"] = "error " + str(ex)
                return info

    def put(self, id):
        
        info = {
            "success" : False,
            "message" : ""
        }
        
        vehicle = self.get(id)["data"][0]
        
        if vehicle == None:
            info["message"] = "vehicle does not exist"
            return info
        
        if "marca" in request.json and request.json["marca"] != vehicle["marca"]:
            vehicle["marca"] = request.json["marca"]
            
        if "modelo" in request.json and request.json["modelo"] != vehicle["modelo"]:
            vehicle["modelo"] = request.json["modelo"]
            
        if "patente" in request.json and request.json["patente"] != vehicle["patente"]:
            vehicle["patente"] = request.json["patente"]
        
        if "year" in request.json and request.json["year"] != vehicle["year"]:
            vehicle["year"] = request.json["year"]
            
        if "id_persona_owner" in request.json and request.json["id_persona_owner"] != vehicle["id_persona_owner"]:
            vehicle["id_persona_owner"] = request.json["id_persona_owner"]
            
        try:
            
            with Cursor(mysql) as db:
                query = "UPDATE VEHICULOS SET MARCA = %s, MODELO = %s, PATENTE = %s, YEAR = %s, ID_PERSONA_OWNER = %s WHERE ID = %s"
                db.execute(query, (
                    vehicle["marca"],
                    vehicle["modelo"],
                    vehicle["patente"],
                    vehicle["year"],
                    vehicle["id_persona_owner"],
                    id
                ))
                
                info["success"] = True
                info["message"] = "updated vehicle"
                
                query = "SELECT ID, MARCA, MODELO, PATENTE, YEAR, ID_PERSONA_OWNER FROM VEHICULOS WHERE ID = %s"
                db.execute(query, (id, ))
                columns = db.description
                vehicle = db.fetchall()
                
                info["data"] = formatResponse(columns, vehicle)
                return info
            
        except Exception as ex:
            info["message"] = "error " + str(ex)
            return info
        
    def delete(self, id):
        
        info = {
            "success" : False,
            "message" : ""
        }
        
        vehicle = self.get(id)["data"][0]
        
        if vehicle == None:
            info["message"] = "vehicle does not exist"
            return info
        
        try:
            with Cursor(mysql) as db:
                query = "DELETE FROM VEHICULOS WHERE ID = %s"
                db.execute(query, (id, ))
                
                info["success"] = True
                info["message"] = "deleted vehicle"
                info["data"] = vehicle
                return info
            
        except Exception as ex:
            info["message"] = "error " + str(ex)
            
    

            