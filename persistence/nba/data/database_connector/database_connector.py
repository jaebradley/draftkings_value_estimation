class DatabaseConnector:
    def __init__(self, driver_name, host, port, database, server):
        self.server = server
        self.database = database
        self.port = port
        self.host = host
        self.driver_name = driver_name

    def create_database_connection(self):
        pass