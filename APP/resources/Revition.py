from flask_restful import Resource
from flask import request
from itsdangerous import json

from utils.Cursor import Cursor
from utils.Common import formatResponse
from config.db import mysql

class Revitions(Resource):
    
    def get(self):
        
        revitions = None
        columns = None
        
        filters = ""
                
        if "patent" in request.args and request.args["patent"] != "":
            filters += f"INNER JOIN VEHICULOS ON VEHICULOS.ID = REVISIONES.ID_VEHICULO AND VEHICULOS.PATENTE = {request.args['patent']} "
        
        with Cursor(mysql) as db:
            query = "SELECT REVISIONES.ID, REVISIONES.APROBADO, REVISIONES.OBSERVACIONES, CAST(REVISIONES.FECHA_REVISION AS nchar) AS FECHA_REVISION, REVISIONES.ID_PERSONA_ENCARGADO, REVISIONES.ID_VEHICULO FROM REVISIONES " + filters            
            db.execute(query)
            columns = db.description
            revitions = db.fetchall()
            
        info = {
            "success" : True if len(revitions) > 0 else False,
            "data" : formatResponse(columns, revitions)
        }
        
        for revition in info["data"]:
            revition["aprobado"] = True if revition["aprobado"] == 1 else False
        
        return info
    
    
class Revition(Resource):
    
    def get(self, id):
        
        info = {
            "success" : False,
            "data" : ""
        }
        
        revition = None
        columns = None
        
        with Cursor(mysql) as db:
            query = "SELECT ID, APROBADO, OBSERVACIONES, CAST(FECHA_REVISION AS nchar) AS FECHA_REVISION, ID_PERSONA_ENCARGADO, ID_VEHICULO FROM REVISIONES WHERE ID = %s"
            db.execute(query, (id, ))
            columns = db.description
            revition = db.fetchall()
            
        if len(revition) > 0:            
            
            info["success"] = True
            info["data"] = formatResponse(columns, revition)
            
            info["data"][0]["aprobado"] = True if info["data"][0]["aprobado"] == 1 else False
            
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
                query = "INSERT INTO REVISIONES(APROBADO, OBSERVACIONES, FECHA_REVISION, ID_PERSONA_ENCARGADO, ID_VEHICULO) VALUES (%s, %s, %s, %s, %s)"
                db.execute(query, (
                    request.json["aprobado"],
                    request.json["observaciones"],
                    str(request.json["fecha_revision"]),
                    request.json["id_persona_encargado"],
                    request.json["id_vehiculo"]
                ))
                
                info["success"] = True
                info["message"] = "created revition"
                
                query = "SELECT ID, APROBADO, OBSERVACIONES, CAST(FECHA_REVISION AS nchar) AS FECHA_REVISION, ID_PERSONA_ENCARGADO, ID_VEHICULO FROM REVISIONES WHERE ID = (SELECT MAX(ID) FROM REVISIONES)"
                db.execute(query)
                columns = db.description
                revition = db.fetchall()
                
                info["data"] = formatResponse(columns, revition)
                info["data"][0]["aprobado"] = True if info["data"][0]["aprobado"] == 1 else False
                return info
            
        except Exception as ex:
            info["message"] = "error " + str(ex)
            return info
        
    def put(self, id):
        
        info = {
            "success" : False,
            "message" : ""
        }
        
        revition = self.get(id)["data"][0]
        
        if revition == None:
            info["message"] = "revition does not exist"
            return info
        
        if "aprobado" in request.json and request.json["aprobado"] != revition["aprobado"]:
            revition["aprobado"] = request.json["aprobado"]
            
        if "observaciones" in request.json and request.json["observaciones"] != revition["observaciones"]:
            revition["observaciones"] = request.json["observaciones"]
            
        if "fecha_revision" in request.json and request.json["fecha_revision"] != revition["fecha_revision"]:
            revition["fecha_revision"] = request.json["fecha_revision"]
            
        if "id_persona_encargado" in request.json and request.json["id_persona_encargado"] != revition["id_persona_encargado"]:
            revition["id_persona_encargado"] = request.json["id_persona_encargado"]
            
        if "id_vehiculo" in request.json and request.json["id_vehiculo"] != revition["id_vehiculo"]:
            revition["id_vehiculo"] = request.json["id_vehiculo"]
            
        try:
            with Cursor(mysql) as db:
                query = "UPDATE REVISIONES SET APROBADO = %s, OBSERVACIONES = %s, FECHA_REVISION = %s, ID_PERSONA_ENCARGADO = %s, ID_VEHICULO = %s WHERE ID = %s"
                db.execute(query, (
                    revition["aprobado"],
                    revition["observaciones"],
                    str(revition["fecha_revision"]),
                    revition["id_persona_encargado"],
                    revition["id_vehiculo"],
                    id
                ))
                
                info["success"] = True
                info["message"] = "updated revition"
                
                query = "SELECT ID, APROBADO, OBSERVACIONES, CAST(FECHA_REVISION AS nchar) AS FECHA_REVISION, ID_PERSONA_ENCARGADO, ID_VEHICULO FROM REVISIONES WHERE ID = %s"
                db.execute(query, (id, ))
                
                columns = db.description
                revition = db.fetchall()
                
                info["data"] = formatResponse(columns, revition)
                info["data"][0]["aprobado"] = True if info["data"][0]["aprobado"] == 1 else False
                return info
            
        except Exception as ex:
            info["message"] = "error " + str(ex)
            return info
    
    def delete(self, id):
        
        info = {
            "success" : False,
            "message" : ""
        }
        
        revition = self.get(id)["data"][0]
        
        if revition == None:
            info["message"] = "revition does not exist"
            return info
        
        try:
            
            with Cursor(mysql) as db:
                query = "DELETE FROM REVISIONES WHERE ID = %s"
                db.execute(query, (id, ))
                
                info["success"] = True
                info["message"] = "deleted revition"
                info["data"] = revition
                return info
            
        except Exception as ex:
            info["message"] = "error " + ex
            return info
        