# Importamos librerias, rutas y modelos
from flask import Flask, render_template, request, redirect, url_for, flash # ### NUEVO: Agregamos request, redirect, url_for, flash
from config.config import Config 
from models.db import db
from routes.variedadUva_routes import variedadUva_bp
from routes.loteVino_routes import loteVino_bp
from routes.recepcionUva_routes import recepcionUva_bp
from routes.fermentacionAlcoholica_routes import fermentacion_bp
from routes.crianza_almacenamiento_routes import crianza_bp
from routes.embotellado_routes import embotellado_bp

# ### NUEVO: Importaciones para Flask-Login
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user 

# Creamos la app, configuraciones e importaciones
app = Flask(__name__)

# ### NUEVO: Configuración de Flask-Login
login_manager = LoginManager() 
login_manager.init_app(app)
login_manager.login_view = 'login' # La vista a la que redirigir si se necesita login

# ### NUEVO: Configuración de la clave secreta para sesiones (¡MUY IMPORTANTE!)
# ### CAMBIA ESTO POR UNA CLAVE REAL Y COMPLEJA PARA PRODUCCIÓN
app.config['SECRET_KEY'] = 'una_clave_secreta_muy_segura_y_larga_para_tu_proyecto_de_bodega' 

# ### NUEVO: Clase de Usuario para Flask-Login
# Esto es una simplificación. En un proyecto real, se integraría con tu modelo de base de datos.
class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def get_id(self):
        return str(self.id)

# ### NUEVO: Usuario de prueba (hardcodeado)
# En un proyecto real, esto vendría de una base de datos o de un modelo de usuario.
USERS = {
    "admin": {"password": "1234"} # Puedes cambiar el usuario y la contraseña
}

# ### NUEVO: Función para recargar el usuario desde la sesión
@login_manager.user_loader
def load_user(user_id):
    if user_id in USERS:
        return User(user_id)
    return None

def create_app():
    # Cargamos la configuracion
    app.config.from_object(Config)
    
    # Inicializamos base de datos
    db.init_app(app)
    
    with app.app_context():
        #db.drop_all() #borra todo 
        db.create_all()  # Aquí se crean las tablas si no existen
    
    # Registramos los blueprints
    app.register_blueprint(variedadUva_bp, url_prefix="/variedades") # Se usa el url_prefix para acortar la ruta en routes y definirla directamente aca
    app.register_blueprint(loteVino_bp, url_prefix="/lotes")
    app.register_blueprint(recepcionUva_bp, url_prefix="/recepcion")
    app.register_blueprint(fermentacion_bp, url_prefix="/fermentacion")
    app.register_blueprint(crianza_bp, url_prefix="/crianza")
    app.register_blueprint(embotellado_bp, url_prefix="/embotellado")
    
    return app

#visualizamos index
@app.route("/")
@login_required # ### NUEVO: Protegemos la ruta del index para que requiera login
def index():
    return render_template("index.html")

@app.route("/about")
def about(): # Puedes proteger esta ruta también con @login_required si lo deseas
    return render_template("about.html")

# ### NUEVO: Rutas de Login y Logout ###
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Si el usuario ya está autenticado, lo redirigimos a la página de inicio
        return redirect(url_for('index')) 

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in USERS and USERS[username]['password'] == password:
            user = User(username)
            login_user(user) # Inicia sesión el usuario
            flash('Inicio de sesión exitoso.', 'success')
            
            # Redirige a la página que intentaba acceder antes del login, o al index si no hay 'next'
            next_page = request.args.get('next') 
            return redirect(next_page or url_for('index')) 
        else:
            flash('Credenciales inválidas. Inténtalo de nuevo.', 'danger')
            
    # Si es un GET o si las credenciales son inválidas, muestra el formulario de login
    return render_template('login.html')

@app.route('/logout')
@login_required # Solo permite cerrar sesión si ya estás logueado
def logout():
    logout_user() # Cierra la sesión del usuario
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('login')) # Redirige a la página de login

if __name__=="__main__":
    app = create_app()
    # ### NUEVO: Se recomienda añadir host='0.0.0.0' para que sea accesible desde otras IPs en la red
    app.run(debug=True, host='0.0.0.0', port=5000)