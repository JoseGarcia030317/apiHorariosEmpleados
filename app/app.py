from flask import Flask, jsonify
from config import Config
from flask_cors import CORS
from flasgger import Swagger

# Importar los Blueprints de las nuevas ubicaciones
from routes.empleados.empleados import empleados
from routes.horarios.horarios import horarios

# Configuración de la aplicación
PORT = Config.PORT
API_PREFIX = Config.API_PREFIX

# Crear instancia de Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inicializar extensiones
swagger = Swagger(app)
CORS(app)

# Registrar los Blueprints
app.register_blueprint(empleados, url_prefix=API_PREFIX)
app.register_blueprint(horarios, url_prefix=API_PREFIX)

# Manejo de errores personalizados
@app.errorhandler(404)
def handle_404(error):
    """Manejo de error 404 - Recurso no encontrado."""
    return jsonify({"code": 404, "error": "Resource not found"}), 404

@app.errorhandler(500)
def handle_500(error):
    """Manejo de error 500 - Error interno del servidor."""
    return jsonify({"code": 500, "error": "Internal server error"}), 500

# Ejecutar la aplicación localmente
# if __name__ == '__main__':
    # app.run(app.run(host="0.0.0.0", port=PORT))
    #app.run(port=PORT)