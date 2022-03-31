import inspect
from flask_restful import Resource
from flask import request

from utils.Cursor import Cursor
from utils.Common import formatResponse
from config.db import mysql

class InspectionStates(Resource):
    
    def get(self):
        
        states = None
        columns = None
        
        with Cursor(mysql) as db:
            query = "SELECT ID, NOMBRE FROM ESTADOS_INSPECCION"
            db.execute(query)
            columns = db.description
            states = db.fetchall()
            
            
        info = {
            "success" : True if len(states) > 0 else False,
            "data" : formatResponse(columns, states)
        }
        
        return info
            
            
class InspectionState(Resource):
    
    def get(self, id):
        
        info = {
            "success" : False,
            "data" : ""
        }
        
        state = None
        columns = None
        
        with Cursor(mysql) as db:
            query = "SELECT ID, NOMBRE FROM ESTADOS_INSPECCION WHERE ID = %s"
            db.execute(query, id)
            columns = db.description
            state = db.fetchall()
            
        if len(state) > 0:
            info["success"] = True
            info["data"] = formatResponse(columns, state)
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
                query = "INSERT INTO ESTADOS_INSPECCION(NOMBRE) VALUES (%s)"
                db.execute(query, (request.json["nombre"],))
                
                info["success"] = True
                info["message"] = "created inspection state"
                
                query = "SELECT ID, NOMBRE FROM ESTADOS_INSPECCION WHERE ID = (SELECT MAX(ID) FROM ESTADOS_INSPECCION)"
                db.execute(query)                
                columns = db.description
                inspectionState = db.fetchall()
                
                info["data"] = formatResponse(columns, inspectionState)
                
                return info
            
        except Exception as ex:
            info["message"] = "error " + str(ex)
            return info
        
    def put(self, id):
        
        info = {
            "success" : False,
            "message" : ""
        }
        
        inspectionState = self.get(id)["data"][0]
        
        if inspectionState == None:
            info["message"] = "inspection state does not exist"
            return info
        
        if "nombre" in request.json and request.json["nombre"] != inspectionState["nombre"]:
            inspectionState["nombre"] = request.json["nombre"]
            
        try:
            
            with Cursor(mysql) as db:
                query = "UPDATE ESTADOS_INSPECCION SET NOMBRE = %s WHERE ID = %s"
                db.execute(query, (
                    inspectionState["nombre"],
                    id
                ))
                
                info["success"] = True
                info["message"] = "updated inspection state"
                
                query = "SELECT ID, NOMBRE FROM ESTADOS_INSPECCION WHERE ID = %s"
                db.execute(query, (id, ))
                columns = db.description
                inspectionState = db.fetchall()
                
                info["data"] = formatResponse(columns, inspectionState)
                
            return info
            
            
        except Exception as ex:
            info["message"] = "error " + str(ex)
            return info
    
    def delete(self, id):
        
        info = {
            "success" : True,
            "message" : ""
        }
        
        inspectionState = self.get(id)["data"][0]
        
        if inspectionState == None:
            info["message"] = "inspection state does not exist"
            return info
        
        try:
            
            with Cursor(mysql) as db:
                query = "DELETE FROM ESTADOS_INSPECCION WHERE ID = %s"
                db.execute(query, (id, ))
                
                info["success"] = True
                info["message"] = "deleted inspection state"
                info["data"] = inspectionState
                return info
            
        except Exception as ex:
            info["message"] = "error " + str(ex)
            return info
        