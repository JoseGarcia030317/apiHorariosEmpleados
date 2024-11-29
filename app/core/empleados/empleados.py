import logging
from models.empleados import TbEmpleado, VwEmpleados
from sqlalchemy.exc import SQLAlchemyError
from utils.conexiondb import get_session

# Configurar el registro de errores
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmpleadoClass:
    def __init__(self):
        self.session_factory = get_session()
    
    # Leer (/empleados/obtener_empleados)
    def obtener_empleados(self):
        sesion = self.session_factory
        try:
            empleados = sesion.query(VwEmpleados).all()
            if not empleados:
                return True, []
            empleados_lista = [
                {
                    "id_empleado" : empleado.id_empleado,
                    "empleado" : empleado.nombre + " " + empleado.apellido_pat + " " + empleado.apellido_mat,
                    #"apellido_pat" : empleado.apellido_pat,
                    #"apellido_mat" : empleado.apellido_mat,
                    "email" : empleado.email,
                    "telefono" : empleado.telefono,
                    "id_rol" : empleado.id_rol,
                    "rol" : empleado.rol
                }
                for empleado in empleados
            ]
            return True, empleados_lista
        except SQLAlchemyError as e:
            logger.error(f"Error obteniendo los insumos: {str(e)}")
            return False, []
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return False, []
        finally:
            sesion.close()