# Importamos librerias, rutas y modelos
from flask import Flask , render_template
from config.config import Config 
from models.db import db
from routes.variedadUva_routes import variedadUva_bp
from routes.loteVino_routes import loteVino_bp
from routes.recepcionUva_routes import recepcionUva_bp
from routes.fermentacionAlcoholica_routes import fermentacion_bp
from routes.crianza_almacenamiento_routes import crianza_bp
from routes.embotellado_routes import embotellado_bp

# Creamos la app, configuraciones e importaciones
app = Flask(__name__)

def create_app():
    
    # Cargamos la configuracion
    app.config.from_object(Config)
    
    # Inicializamos base de datos
    db.init_app(app)
    
    with app.app_context():
        # db.drop_all() #borra todo 
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
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__=="__main__":
    app= create_app()
    app.run(debug=True)

