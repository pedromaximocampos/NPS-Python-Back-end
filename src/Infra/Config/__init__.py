from .ConnectionSQL import ConnectionSQL
from .ConnectionNoSQL import MongoDB
from globalvars import SQL_CONNECTION_STRING, MONGO_CONNECTION_STRING, MONGO_DATABASE_NAME

sql_connection = ConnectionSQL(connection_string=SQL_CONNECTION_STRING)
mongo_connection = MongoDB(connectionString=MONGO_CONNECTION_STRING, dataBaseName=MONGO_DATABASE_NAME)


def init_connections_with_database(app):
    
    app.config['SQLALCHEMY_DATABASE_URI'] = SQL_CONNECTION_STRING
    app.config['MONGO_URI'] = MONGO_CONNECTION_STRING
    
    sql_connection.init_app(app)
    mongo_connection.connect()
   
    return sql_connection, mongo_connection

