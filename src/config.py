
"""El archivo “config.py” almacena las clases con los parámetros necesarios para que el servidor web
pueda ser utilizado, contiene los parámetros necesarios para que la aplicación pueda conectarse con la
base de datos y una clave secreta (SECRET_KEY) que deja las “coockies” utilizadas para el inicio de
sesión con la firma personal de la aplicación web. """
class Config():
    SECRET_KEY = "Bas%367-SX$%S&!9&*24@fsy"

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'sanchez96'
    MYSQL_DB = 'pabot_db'


config = {
    'development': DevelopmentConfig
}
