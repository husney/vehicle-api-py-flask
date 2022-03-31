from flask import Flask
from config.db import mysql, dbInfo
from flask_restful import Api

import sys
sys.path.append('../')
from resources.Person import Person, Persons
from resources.RevitionType import RevitionType, RevitionTypes
from resources.Vehicle import  Vehicle, Vehicles
from resources.Revition import Revition, Revitions
from resources.InspectionStates import InspectionState, InspectionStates
from resources.Inspection import Inspection, Inspections


 
app = Flask(__name__)
api = Api(app)

app.config['MYSQL_HOST'] = dbInfo['host']
app.config['MYSQL_USER'] = dbInfo['user']
app.config['MYSQL_PASSWORD'] = dbInfo['password']
app.config['MYSQL_DB'] = dbInfo['database']

mysql.init_app(app)


api.add_resource(Person, '/person', '/person/<id>')
api.add_resource(Persons, '/persons')
api.add_resource(RevitionType, '/revitionType', '/revitionType/<id>')
api.add_resource(RevitionTypes, '/revitionTypes')
api.add_resource(Vehicle, '/vehicle', '/vehicle/<id>')
api.add_resource(Vehicles, '/vehicles')
api.add_resource(Revition, '/revition', '/revition/<id>')
api.add_resource(Revitions, '/revitions')
api.add_resource(InspectionState, '/inspectionState', '/inspectionState/<id>')
api.add_resource(InspectionStates, '/inspectionStates')
api.add_resource(Inspection, '/inspection', '/inspection/<id>')
api.add_resource(Inspections, '/inspections')


if __name__ == "__main__":
    app.run(port=8090)