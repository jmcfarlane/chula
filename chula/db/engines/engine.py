"""
Chula database engine module
"""

from chula import collection

class Engine(object):
    def __init__(self):
        self.conn = None
        self.error = collection.Collection()

    def set_isolation(self, level=1):
        """
        Set the database connection isolation level
        """

        pass
    
    def close(self):
        """
        Destroy a database connection object
        """
        
        self.conn.close()
        
    def commit(self):
        """
        Perform database commit
        """
        
        self.conn.commit()
        
    def rollback(self):
        """
        Perform query rollback
        """
        
        self.conn.rollback()
    
    def cursor(self):
        """
        Create database cursor

        @return: Instance
        """

        return self.conn.cursor()
