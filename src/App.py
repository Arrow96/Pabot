"""“app.py” es el archivo principal del proyecto, que ejecuta todas las funciones del servidor,
controla el flujo de información y la comunicación entre los “models” y los “templates”, en el
se importan las librerías necesarias para utilizar el framework “Flask”, conectarse a la base
de datos (flask_mysqldb), ejecutar las funciones necesarias para los inicios de sesion (flask_login)
y mantener la autenticación de esta (flask_wtf.csrf). Por supuesto, también importa las clases de
pertenecientes al directorio “models”."""
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from textblob import TextBlob

# Librerias del Chatbot
from models.ChatbotBrain import ChatbotBrain

from config import config

# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.User import User

"""Se crea la aplicación de tipo “ Flask” y se almacena en la variable “app”, con la variable 
“csrf” de tipo “CSRFProtect()” entregamos un token de autenticación a nuestra aplicación web 
para entregar seguridad a estas, con la variable mysql de tipo MySQL() enlazamos nuestra base 
de datos a la aplicación y no la variable “login_manager_app” de tipo “LoginManager()” entregamos 
a la aplicación web las propiedades necesarias para ejecutar inicios de sesión de usuarios. """
app = Flask(__name__)

csrf = CSRFProtect()
mysql = MySQL(app)
login_manager_app = LoginManager(app)
chatbot = ChatbotBrain()


"""La función “load_user()” retorna los datos de un usuario que ya ha autentificado su inicio de 
sesión, mientras que la función “index()” es ejecutada por defecto y una vez abierta la aplicación 
en el navegador redirecciona al usuario hacia la página de inicio de sesión. """
@login_manager_app.user_loader
def load_user(email):
    return ModelUser.get_by_id(mysql, email)
@app.route('/')
def index():
    return render_template('auth/index.html')

"""La función “login()” es la que realiza el inicio de sesión del usuario con parámetros ingresados 
por este, identificando cualquier error de tipeo por parte del usuario con su respectiva alerta de error, 
finalmente dependiendo de si el usuario es un usuario común o un administrador, la función lo dirige a su 
interfaz correspondiente."""
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
            user = User(0, request.form['email'], request.form['password'])
            logged_user = ModelUser.login(mysql, user)
            if logged_user != None:
                if logged_user.password:
                    login_user(logged_user)
                    if logged_user.state == 'habilitado':
                        if logged_user.tipo == 'user':
                            return redirect(url_for('home'))
                        elif logged_user.tipo == 'admin':
                            return redirect(url_for('userManager'))
                    else:
                        flash("Cuenta desabilitada, contacte a soporte tecnico...")
                        return render_template('auth/login.html')
                else:
                    flash("Contraseña invalida...")
                    return render_template('auth/login.html')
            else:
                flash("Usuario no encontrado...")
                return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

"""La función “logout()” lo que realiza es el cierre de sesión por parte del usuario, quitándole su token
de autenticación y redirigiéndolo a la interfaz de inicio de sesión."""
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

"""La función “userManager” crea una conexión con la base de datos y ejecuta una sentencia MySQL la cual 
obtiene todos los registros de tabla usuarios y los clasifica según sean “usuarios” o “administradores”, 
luego esos datos son retornados en las variables “users” y “admins”, además de mostrarle al usuario la interfaz 
web “user-manager.html”. """
@app.route('/user-manager', methods=['GET', 'POST'])
@login_required
def userManager():
    cursor1 = mysql.connection.cursor()
    cursor1.execute("SELECT id, email, alias, state FROM usuarios WHERE tipo = 'user'")
    data_user = cursor1.fetchall()
    cursor1.close()
    cursor2 = mysql.connection.cursor()
    cursor2.execute("SELECT id, email, alias, state FROM usuarios WHERE tipo = 'admin'")
    data_admin = cursor2.fetchall()
    cursor2.close()
    return render_template('auth/user-manager.html', users=data_user, admins=data_admin)

"""La función “createUser()” crea una conexión con la base de datos y ejecuta una sentencia MySQL con 
parámetros ingresados por el usuario, esto para generar un nuevo registro en la tabla “usuarios” de la 
base de datos. Luego finaliza redireccionando al usuario de regreso a la interfaz web “user-manager.html”."""
@app.route('/new-user', methods=['POST'])
def createUser():
    email = request.form['email']
    password = generate_password_hash(request.form['password'])
    alias = request.form['alias']
    tipo = request.form['tipo']
    try:
        cursor = mysql.connection.cursor()
        sql = f"INSERT INTO usuarios(email, password, alias, tipo, state) VALUES('{email}','{password}','{alias}','{tipo}','habilitado')"
        cursor.execute(sql)
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('userManager'))
    except Exception as e:
        return redirect(url_for('userManager'))

"""La función “updateUser()” crea una conexión con la base de datos y ejecuta una sentencia MySQL con 
parámetros ingresados por el usuario, esto para modificar un registro preexistente en la tabla “usuarios” 
de la base de datos. Luego finaliza redireccionando al usuario de regreso a la interfaz web 
“user-manager.html”. """
@app.route('/update-user', methods=['POST'])
def updateUser():
    id = request.form['id']
    password = generate_password_hash(request.form['password'])
    alias = request.form['alias']
    tipo = request.form['tipo']
    state = request.form['state']
    cursor = mysql.connection.cursor()
    sql = f"UPDATE usuarios SET password='{password}', alias='{alias}', tipo='{tipo}', state='{state}' WHERE id={id}"
    cursor.execute(sql)
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('userManager'))

"""La función “deleteUser()” crea una conexión con la base de datos y ejecuta una sentencia MySQL con 
parámetros obtenidos del usuario, esto para modificar un registro preexistente en la tabla “usuarios” 
de la base de datos, para que este registro quede deshabilitado para su uso. Luego finaliza redireccionando 
al usuario de regreso a la interfaz web “user-manager.html”. """
@app.route('/delete-user/<string:id>', methods=['GET'])
def deleteUser(id):
    cursor = mysql.connection.cursor()
    sql = f"UPDATE usuarios SET state='deshabilitado' WHERE id={id}"
    cursor.execute(sql)
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('userManager'))

"""La función “home()” le retorna al usuario la interfaz web “home1.html”."""
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('auth/home1.html')

"""La función “home2()” le retorna al usuario la interfaz web “home2.html”."""
@app.route('/home2', methods=['GET', 'POST'])
@login_required
def home2():
    return render_template('auth/home2.html')

"""La función “home3()” le retorna al usuario la interfaz web “home3.html”."""
@app.route('/home3', methods=['GET', 'POST'])
@login_required
def home3():
    return render_template('auth/home3.html')

"""La función “get_bot_response_english()” guarda un parámetro ingresado por el usuario y lo 
utiliza para ejecutar la función “talk()” de la variable “chatbot”, obteniendo un resultado en 
el idioma nativo de la inteligencia artificial(ingles), luego esto es almacenado en la variable 
“botResponse” que luego es retornado en formato “string”."""
@app.route("/get-english")
def get_bot_response_english():
    userText = request.args.get('msg')
    t = TextBlob(userText)
    ten = t.translate(from_lang='en', to='es')
    botResponse = chatbot.talk(str(ten))
    b = TextBlob(str(botResponse))
    bot = b.translate(from_lang='es', to='en')
    return str(bot)

"""La función “get_bot_response_spanish()” guarda un parámetro ingresado por el usuario el cual es 
traducido al idioma nativo de la inteligencia artificial(Ingles) mediante la funcion translate() de 
la clase TextBlob(), esto lo utiliza para ejecutar la función “talk()” de la variable “chatbot”, 
obteniendo un resultado en el idioma nativo de la inteligencia artificial(Ingles), que traduce a un 
idioma prestablecido(Español), luego esto es almacenado en la variable “bot” que luego es retornado 
en formato “string”."""
@app.route("/get-spanish")
def get_bot_response_spanish():
    userText = request.args.get('msg')
    botResponse = chatbot.talk(str(userText))
    return str(botResponse)

"""La función “get_bot_response_italian()” guarda un parámetro ingresado por el usuario el cual es 
traducido al idioma nativo de la inteligencia artificial(Ingles) mediante la funcion translate() de 
la clase TextBlob(), esto lo utiliza para ejecutar la función “talk()” de la variable “chatbot”, 
obteniendo un resultado en el idioma nativo de la inteligencia artificial(Ingles), que traduce a un 
idioma prestablecido(Italiano), luego esto es almacenado en la variable “bot” que luego es retornado 
en formato “string”."""
@app.route("/get-italian")
def get_bot_response_italian():
    userText = request.args.get('msg')
    t = TextBlob(userText)
    ten = t.translate(from_lang='it', to='es')
    botResponse = chatbot.talk(str(ten))
    b = TextBlob(str(botResponse))
    bot = b.translate(from_lang='es', to='it')
    return str(bot)

"""La función “status_404()” retorna un texto HTML en caso de que ocurra un error 404."""
def status_404(error):
    return "<h1>Página no encontrada</h1>", 404

"""Esta condicional es la responsable de ejecutar la aplicación web activando la configuración 
y la seguridad de autenticación. """
if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(404, status_404)
    app.run()