from flask_restful import Resource
from flask import request

from utils.Cursor import Cursor
from utils.Common import formatResponse
from config.db import mysql

class Inspections(Resource):
    
    def get(self):
        
        inspections = None
        columns = None
    
        
        with Cursor(mysql) as db:
            query = "SELECT ID, OBSERVACIONES, ID_ESTADO, ID_TIPO_REVISION, ID_PERSONA_ENCARGADO, ID_REVISION FROM INSPECCIONES"
            db.execute(query)
            columns = db.description
            inspections = db.fetchall()
            
        info = {
            "success" : True if len(inspections) > 0 else False,
            "data" : formatResponse(columns, inspections)
        }
        
        return info
    
    
class Inspection(Resource):
    
    def get(self, id):
        
        info = {
            "success" : False,
            "data" : ""
        }
        
        inspection = None
        columns = None
        
        with Cursor(mysql) as db:
            query = "SELECT ID, OBSERVACIONES, ID_ESTADO, ID_TIPO_REVISION, ID_PERSONA_ENCARGADO, ID_REVISION FROM INSPECCIONES WHERE ID = %s"
            db.execute(query, id)
            columns = db.description
            inspection = db.fetchall()
            
        if len(inspection) > 0:
            info["success"] = True
            info["data"] = formatResponse(columns, inspection)
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
                query = "INSERT INTO INSPECCIONES(OBSERVACIONES, ID_ESTADO, ID_TIPO_REVISION, ID_PERSONA_ENCARGADO, ID_REVISION) VALUES (%s, %s, %s, %s, %s)"
                db.execute(query, (
                    request.json["observaciones"],
                    request.json["id_estado"],
                    request.json["id_tipo_revision"],
                    request.json["id_persona_encargado"],
                    request.json["id_revision"]
                ))
                
                info["success"] = True
                info["message"] = "created inspection"
                
                query = "SELECT ID, OBSERVACIONES, ID_ESTADO, ID_TIPO_REVISION, ID_PERSONA_ENCARGADO, ID_REVISION FROM INSPECCIONES WHERE ID = (SELECT MAX(ID) FROM INSPECCIONES)"
                db.execute(query)
                columns = db.description
                inspection = db.fetchall()
                
                info["data"] = formatResponse(columns, inspection)
                
            return info
                
            
        except Exception as ex:
            info["message"] = "erro " + str(ex)
            return info

    def put(self, id):
        
        info = {
            "success" : False,
            "message" : ""
        }
        
        inspection = self.get(id)["data"][0]
        
        if inspection == None:
            info["message"] = "inspection does not exist"
            return info
        
        if "observaciones" in request.json and request.json["observaciones"] != inspection["observaciones"]:
            inspection["observaciones"] = request.json["observaciones"]
            
        if "id_estado" in request.json and request.json["id_estado"] != inspection["id_estado"]:
            inspection["id_estado"] = request.json["id_estado"]
            
        if "id_tipo_revision"  in request.json and request.json["id_tipo_revision"] != inspection["id_tipo_revision"]:
            inspection["id_tipo_revision"] = request.json["id_tipo_revision"]
            
        if "id_persona_encargado" in request.json and request.json["id_persona_encargado"] != inspection["id_persona_encargado"]:
            inspection["id_persona_encargado"] = request.json["id_persona_encargado"]
            
        if "id_revision" in request.json and request.json["id_revision"] != inspection["id_revision"]:
            inspection["id_revision"] = request.json["id_revision"]
            
        try:
            
            with Cursor(mysql) as db:
                query = "UPDATE INSPECCIONES SET OBSERVACIONES = %s, ID_ESTADO = %s, ID_TIPO_REVISION = %s, ID_PERSONA_ENCARGADO = %s, ID_REVISION = %s WHERE ID = %s"
                db.execute(query, (
                    inspection["observaciones"],
                    inspection["id_estado"],
                    inspection["id_tipo_revision"],
                    inspection["id_persona_encargado"],
                    inspection["id_revision"],
                    id
                ))
                
                info["success"] = True
                info["message"] = "updated inspection"
                
                query = "SELECT ID, OBSERVACIONES, ID_ESTADO, ID_TIPO_REVISION, ID_PERSONA_ENCARGADO, ID_REVISION FROM INSPECCIONES WHERE ID = %s"
                db.execute(query, (id, ))
                columns = db.description
                inspection = db.fetchall()
                
                info["data"] = formatResponse(columns, inspection)
            return info
            
        except Exception as ex:
            info["messge"] = "error " + str(ex)
            return info
        
    def delete(self, id):
        
        info = {
            "success" : False,
            "message" : ""
        }
        
        inspection = self.get(id)["data"][0]
        
        if inspection == None:
            info["message"] = "inspection does not exist"
            return info
        
        try:
            
            with Cursor(mysql) as db:
                query = "DELETE FROM INSPECCIONES WHERE ID = %s"
                db.execute(query, (id, ))
                
                info["success"] = True
                info["message"] = "deleted inspection"
                info["data"] = inspection
                return info 
            
        except Exception as ex:
            info["message"] = "error " + str(ex)
            return info