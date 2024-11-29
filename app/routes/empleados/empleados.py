from flask import Blueprint, jsonify, request
from core.empleados.empleados import EmpleadoClass

empleados = Blueprint('empleados', __name__)

@empleados.route('/empleados/obtener_empleados', methods=['GET'])
def obtener_empleados():
    """Obtiene una lista de empleados activos de la base de datos
    ---
    responses:
      200:
        description : Respuesta exitosa
      401:
        description : Sin credenciales válidas para acceder al recurso
      500: 
        description : Error interno del servidor
    """
    try:
        empleado = EmpleadoClass()
        bandera, respuesta = empleado.obtener_empleados()

        if bandera:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error" : "Error interno del servidor al acceder a los datos"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500    