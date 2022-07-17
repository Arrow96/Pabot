"""Se importa “check_password_hash” de la librería “werzeug.security” con el objetivo de usar sus propiedad
de encriptación, mientras que “UserMixin” de la librería “flask_login” permite heredar propiedades útiles
para crear usuarios como la clase creada “User(UserMixin)”. """
from werkzeug.security import check_password_hash
from flask_login import UserMixin


class User(UserMixin):

    """La función o metodo “__init__()” cumple el rol de constructor de la clase “User(UserMixin)”, posee
     sus respectivos atributos, algunos con valores predeterminados que pueden ser modificados según se vea
     necesario."""
    def __init__(self, id, email, password, alias='', tipo='', state='') -> None:
        self.id = id
        self.email = email
        self.password = password
        self.alias = alias
        self.tipo = tipo
        self.state = state

    """La función o método “check_password()” toma un valor del tipo string para devolverlo encriptado,
     este luego será utilizado como una contraseña segura para un usuario. """
    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)