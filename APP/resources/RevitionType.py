from flask_restful import Resource
from flask import jsonify, request

from utils.Common import formatResponse
from utils.Cursor import Cursor
from config.db import mysql

class RevitionTypes(Resource):
    
    def get(self):
        types = None
        columns = None        
        
        with Cursor(mysql) as db:
            query = "SELECT ID, NOMBRE FROM TIPOS_REVISION"
            db.execute(query)
            columns = db.description
            types = db.fetchall()        
        
        info = {
            "success": True if len(types) > 0 else False,
            "data": formatResponse(columns, types)
        }
                
        return info

class RevitionType(Resource):
    
    def get(self, id):
        
        info = {
            "success": False,
            "data": ""
        }
        
        revitionType = None
        columns = None        
        
        with Cursor(mysql) as db:
            query = "SELECT ID, NOMBRE FROM TIPOS_REVISION WHERE ID = %s "            
            db.execute(query, (int(id), ))
            columns = db.description
            revitionType = db.fetchall()        
        
        if len(revitionType) > 0:
            info["success"] = True
            info["data"] = formatResponse(columns, revitionType)
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
                query = "INSERT INTO TIPOS_REVISION(NOMBRE) VALUES (%s);"
                db.execute(query, (request.json["nombre"],))
                
                info["success"] = True
                info["message"] = "created revition type"
                
                query = "SELECT ID, NOMBRE FROM TIPOS_REVISION WHERE ID = (SELECT MAX(ID) FROM TIPOS_REVISION)"
                db.execute(query)
                columns = db.description
                revition = db.fetchall()
                
                info["data"] = formatResponse(columns, revition)
                
                return info
            
        except Exception as ex: 
            info["message"] = "error: " + str(ex)
            
            return info
    
    def put(self, id):
        
        info = {
            "success" : False,
            "message" : ""
        }
        
        revition = self.get(id)["data"][0]
        
        if revition == None:
            info["message"] = "revition type does not exist"
            return info
        
        if "nombre" in request.json and request.json["nombre"] != revition["nombre"]:
            revition["nombre"] = request.json["nombre"]
            
        try:
            
            with Cursor(mysql) as db:
                query = "UPDATE TIPOS_REVISION SET NOMBRE = %s WHERE ID = %s"
                db.execute(query, (
                    revition["nombre"],
                    id
                ))
                
                info["success"] = True
                info["message"] = "updated revition type"
                
                query = "SELECT ID, NOMBRE FROM TIPOS_REVISION WHERE ID = %s"
                db.execute(query, (id, ))
                columns = db.description
                revitionUpdated = db.fetchall()
                
                info["data"] = formatResponse(columns, revitionUpdated)
            
            return info
            
            
            
        except Exception as ex:
            info["message"] = "error " + str(ex)
            return info
        
            
        
    def delete(self, id):
        
        revition = self.get(id)["data"][0]
        
        info = {
            "success" : False,
            "message" : ""
        }
        
        if revition == None:
            info["message"] = "revition type does not exist"
            return info
        
        try:
            
            with Cursor(mysql) as db:
                query = "DELETE FROM TIPOS_REVISION WHERE ID = %s"
                db.execute(query, (id, ))
                
                info["success"] = True
                info["message"] = "deleted revition type"
                info["data"] = revition
                return info
            
        except Exception as ex:
            info["message"] = "error " + str(ex)
            return info