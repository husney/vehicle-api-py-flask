
def formatResponse(columns, data):
    
    """
        Formatea los datos y les agrega el nombre de las columnas como llave
        
        Parameters: 
            tuple : Columns
            tuple : Data
            
        Returns: 
            list: Información formateada
        
    """
    
    response = []    
    for info in data:
            temp = {}
            for (index, value) in enumerate(info):
                temp[str(columns[index][0]).lower()] = value            
            response.append(temp)
            
    return response