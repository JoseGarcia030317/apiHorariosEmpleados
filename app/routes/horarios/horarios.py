from flask import Blueprint, jsonify, request
from core.horarios.horarios import HorarioClass

horarios = Blueprint('horarios', __name__)

@horarios.route('/horarios/guardar_horario', methods=['POST'])
def guardar_horario():
  """
  Guardar un horario en la base de datos
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
    data = request.get_json()

    if not data:
      return jsonify({"error" : "Datos faltantes"}), 500
    
    horario = HorarioClass()

    if data["id_horario_encb"] == 0:
      flag = horario.guardar_horario(data)
    else:
      flag = horario.actualizar_horario(data)

    if flag:
      return jsonify({"message" : "Horario guardado exitosamente"}), 200
    else:
      return jsonify({"error" : "Error interno del servidor al guardar los datos"}), 500
  except Exception as e:
    return jsonify({"error": str(e)}), 500  

@horarios.route('/horarios/eliminar_horarios', methods=['PUT'])
def eliminar_horario():
  """
  En base a el ID, eliminar un horario de manera lógica de la base de datos
  ---
  responses:
    200:
      description : Insumo eliminado exitosamente
    400:
      description : ID de insumo faltante o inválido
    401:
      description : Sin credenciales válidas para acceder al recurso
    500: 
      description : Error interno del servidor
  """
  # Obtener el ID del horario de la petición en JSON
  data = request.get_json()
  if not data or "id_horario_encb" not in data or data["id_horario_encb"] <= 0:
     return jsonify({
                      "error" : "ID del horario faltante o inválido"
                    }), 400

  try:
    horario = HorarioClass()
    bandera = horario.eliminar_horario(data["id_horario_encb"])
    if bandera:
      return jsonify({"message": "Horario eliminado exitosamente"}), 200
    else: 
      return jsonify({"error" : "Error interno del servidor al eliminar la información"}), 500
  except Exception as e:
      return jsonify({"error": str(e)}), 500

@horarios.route('/horarios/obtener_horarios_enc', methods=['GET'])
def obtener_horarios_enc():
   """Obtiene una lista de los encabezados de los horarios de la base de datos
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
      horario = HorarioClass()
      bandera, respuesta = horario.obtener_horarios_enc()
      if bandera:
        return jsonify(respuesta), 200
      else:
        return jsonify({"error" : "Error interno del servidor al acceder a los datos"}), 500
   except Exception as e:
      return jsonify({"error": str(e)}), 500 

@horarios.route('horarios/obtener_horarios_por_fecha', methods=['POST'])
def obtener_horarios_por_fecha():
  """
  Obtiene el horario de una semana para todos los trabajadores asociados al horario
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
    data = request.get_json()
    horario = HorarioClass()
    bandera, respuesta = horario.obtener_horarios_por_fecha(data["fecha_inicio"], data["fecha_fin"])

    if not bandera:
      return jsonify({"error" : "Error interno del servidor al acceder a los datos"}), 500
    
    if not respuesta:
      return jsonify({"message" : "No hay horarios registrados para el rango de fechas indicado"}), 200
    
    return jsonify(respuesta), 200
  except Exception as e:
    return jsonify({"error": str(e)}), 500  

@horarios.route('/horarios/obtener_horarios_por_id', methods=['POST'])
def obtener_horarios():
    """Obtiene una lista de horarios de la base de datos
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
        data = request.get_json()
        horario = HorarioClass()
        bandera, respuesta = horario.obtener_horarios_por_id(data["id_horario_encb"])

        if bandera:
          return jsonify(respuesta), 200
        else:
          return jsonify({"error" : "Error interno del servidor al acceder a los datos"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500   