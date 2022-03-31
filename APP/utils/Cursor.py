class Cursor:
    
    def __init__(self, db):
        self.__db = db
        self.__cursor = None
        
    def __enter__(self):
        try:
            self.__cursor = self.__db.connect.cursor()
            return self.__cursor
        except:
            return None
        
    def __exit__(self, exc_type, exc_val, exc_trace):
        try:
            if exc_type:
                self.__db.rollback()
            else:
                self.__cursor.nextset()
                self.__cursor.connection.commit()
        except:
            pass