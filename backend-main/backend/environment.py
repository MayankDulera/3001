from sqlalchemy import create_engine
from flask import *
from sqlalchemy.orm import scoped_session, sessionmaker
from psycopg2.errors import UniqueViolation
import psycopg2.extras






# HOST = "192.168.56.101"
# USER = "postgres"
# PASSWORD = "postgres"
# PORT = "1105"
# DATABASE = "application"


HOST = "localhost"
USER = "postgres"
PASSWORD = "postgres"
PORT = "5432"
DATABASE = "webscrapper"

def database_connection():

    connection = psycopg2.connect(
                    user=USER, 
                    password=PASSWORD,
                    host=HOST, 
                    port=PORT, 
                    database=DATABASE)
    return connection

# def database_connection():

#     connection = psycopg2.connect(
#                     user=USER, 
#                     password=PASSWORD,
#                     host=HOST, 
#                     port=PORT, 
#                     database=DATABASE,
#                     keepalives=1,
#                     keepalives_idle=30,
#                     keepalives_interval=10,
#                     keepalives_count=5)
#     return connection