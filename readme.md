

* Ingreso de vehículo a revisión (POST)
    http://host:port/revition (Post)

    {
        "aprobado" : true,
        "observaciones" : "ninguna",
        "fecha_revision" : "2021-01-01",
        "id_persona_encargado" : 4,
        "id_vehiculo" : 4
    }

* Ingreso de inspecciones (Post)

    http://host:port/inspection (Post)

    {
        "observaciones" : "ninguna",
        "id_estado" : 1,
        "id_tipo_revision" : 2,
        "id_persona_encargado" : 6,
        "id_revision" : 1
    }

* Borrar inspección (Delete)
    http://host:port/inspection/<id> (Delete)

* Obtener historial de revisiones por patente (Get)
    http://host:port/revitions?patent=1
    http://host:port/revitions

Nota: la collección de postman esta adjunta en este proyecto, "Vehicle_api.postman_collection.json" dentro de ella se encuentran agregadas las pruebas para ejecutarlas con el runner de postman.