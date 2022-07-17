"""Importa la clase User() del archivo User.py del directorio “entities”, luego crea la clase ModelUser() que
 será usada para almacenar los métodos utilizados para generar un inicio de sesión por parte del usuario. """
from .entities.User import User

class ModelUser():
    """El método “login()” crea una conexión con la base de dato y ejecuta una sentencia MySQL con parámetros
     obtenidos de un objeto del tipo “User()”, los datos obtenidos los guarda en la variable “row”, en el caso
     de que estas variables existan, serán transformadas en un objeto de tipo “User()”, además de almacenadas y
     retornadas en la variable “user”, si no existen dichas variables se retornara un valor vacío. Este método
     es utilizado para realizar el inicio de sesión de un usuario."""
    @classmethod
    def login(self, mysql, user):
        try:
            cursor = mysql.connection.cursor()
            sql = """SELECT id, email, password, alias, tipo, state FROM usuarios 
                    WHERE email = '{}'""".format(user.email)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], User.check_password(row[2], user.password), row[3], row[4], row[5])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    """El método “get_by_id()” crea una conexión con la base de datos y ejecuta una sentencia MySQL con valores 
    obtenidos de un usuario que ha realizado un inicio sesión, las variables obtenidas de dicha sentencia se 
    guardan en la variable “row”, en el caso de que estas variables existan, serán transformadas en un objeto 
    de tipo “User()”, además de almacenadas y retornadas en la variable “user”, si no existen dichas variables 
    se retornara un valor vacío. Con este método se puede cargar los datos personales de un usuario que autentifico 
    su inicio de sesión. """
    @classmethod
    def get_by_id(self, mysql, id):
        try:
            cursor = mysql.connection.cursor()
            sql = "SELECT id, email, alias, tipo FROM usuarios WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2], row[3])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)