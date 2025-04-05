import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv

load_dotenv()

class PostgreSQLConnectionPool:
    __instance = None
    __connection_pool = None

    @staticmethod
    def get_instance():
        if PostgreSQLConnectionPool.__instance is None:
            PostgreSQLConnectionPool()
        return PostgreSQLConnectionPool.__instance

    def __init__(self):
        if PostgreSQLConnectionPool.__instance is not None:
            raise Exception("Esta clase es un Singleton!")
        else:
            PostgreSQLConnectionPool.__instance = self
            self.__connection_pool = self.__create_connection_pool()

    def __create_connection_pool(self):
        try:
            # Usar URL de conexión
            db_url = os.getenv("DATABASE_URL")
            
            # Crear un pool de conexiones
            connection_pool = pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=10,
                dsn=db_url
            )
            return connection_pool
        except Exception as e:
            print(f"Error al crear el pool de conexiones: {e}")
            return None

    def get_connection(self):
        return self.__connection_pool.getconn()

    def release_connection(self, connection):
        self.__connection_pool.putconn(connection)

    def close_all_connections(self):
        self.__connection_pool.closeall()