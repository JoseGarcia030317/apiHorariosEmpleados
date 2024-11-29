from datetime import datetime
import logging
from models.horarios import TbHorarioEncabezado, TbHorarioDetalle, VwHorariosCompletos
from sqlalchemy.exc import SQLAlchemyError
from utils.conexiondb import get_session

# Configurar el registro de errores
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HorarioClass:
    def __init__(self):
        self.session_factory = get_session()

    # Insertar (/horarios/guardar_horario)
    def guardar_horario(self, data):
        session = self.session_factory
        try:
            data["clave_horario"] = self.generar_clave_horario()
            # Insertar el encabezado
            new_horario_encb = TbHorarioEncabezado(
                clave_horario=data["clave_horario"],
                fecha_inicio=data["fecha_inicio"],
                fecha_fin=data["fecha_fin"]
            )
            session.add(new_horario_encb)
            session.commit()
            session.refresh(new_horario_encb)
            logger.info(
                f'Encabezado creado con ID: {new_horario_encb.id_horario_encb}')

            # Insertar los detalles
            detalles = data.pop("detalles", [])

            for detalle in detalles:
                horario_detalle = TbHorarioDetalle(
                    id_horario_encb=new_horario_encb.id_horario_encb,
                    id_empleado=detalle["id_empleado"],
                    empleado=detalle["nombre_empleado"],
                    rol=detalle["rol_empleado"],
                    turno_viernes=detalle["turnos"]["viernes"],
                    turno_sabado=detalle["turnos"]["sabado"],
                    turno_domingo=detalle["turnos"]["domingo"],
                    turno_lunes=detalle["turnos"]["lunes"],
                    turno_martes=detalle["turnos"]["martes"],
                    turno_miercoles=detalle["turnos"]["miercoles"],
                    turno_jueves=detalle["turnos"]["jueves"]
                )
                session.add(horario_detalle)
                session.commit()
                session.refresh(horario_detalle)
                logger.info(
                    f'Detalle creado con ID: {horario_detalle.id_horario_deta}')

            return True
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error creando el insumo: {str(e)}")
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error: {str(e)}")
            return False
        finally:
            session.close()

    # Actualizar (/horarios/guardar_horario)
    def actualizar_horario(self, data):
        session = self.session_factory
        try:
            horario_encb = session.query(TbHorarioEncabezado).filter(
                TbHorarioEncabezado.estatus == 1, TbHorarioEncabezado.id_horario_encb == data["id_horario_encb"]).first()
            if horario_encb:
                # Actualizar encabezado
                horario_encb.fecha_inicio = data["fecha_inicio"]
                horario_encb.fecha_fin = data["fecha_fin"]

                # Actualizar estatus a cero los detalles asociados
                detalles = data.pop("detalles", [])
                session.query(TbHorarioDetalle).filter(TbHorarioDetalle.id_horario_encb == data["id_horario_encb"]).update(
                    {"estatus": 0, "fecha_actualiza": datetime.now()})
                session.commit()

                # Insertar detalles
                for detalle in detalles:
                    new_detalle = TbHorarioDetalle(
                        id_horario_encb=horario_encb.id_horario_encb,
                        id_empleado=detalle["id_empleado"],
                        empleado=detalle["nombre_empleado"],
                        rol=detalle["rol_empleado"],
                        turno_viernes=detalle["turnos"]["viernes"],
                        turno_sabado=detalle["turnos"]["sabado"],
                        turno_domingo=detalle["turnos"]["domingo"],
                        turno_lunes=detalle["turnos"]["lunes"],
                        turno_martes=detalle["turnos"]["martes"],
                        turno_miercoles=detalle["turnos"]["miercoles"],
                        turno_jueves=detalle["turnos"]["jueves"]
                    )
                    session.add(new_detalle)
                    session.commit()
                    session.refresh(new_detalle)
                    logger.info(
                        f'Detalle creado con ID: {new_detalle.id_horario_deta}')

                return True
            else:
                logger.warning(
                    f"No se encontró el horario con ID {horario_encb.id_horario_encb}.")
                return False
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error actualizando proveedor: {str(e)}")
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error: {str(e)}")
            return False
        finally:
            session.close()

    # Eliminar horario (/horarios/eliminar_horario)
    def eliminar_horario(self, id_horario_encb):
        session = self.session_factory
        try:
            horario = session.query(TbHorarioEncabezado).filter(
                TbHorarioEncabezado.id_horario_encb == id_horario_encb, TbHorarioEncabezado.estatus == 1).first()
            if not horario:
                return False

            # Eliminar encabezado
            horario.estatus = 0
            session.commit()
            logger.info(f"Horario con ID {id_horario_encb} eliminado")

            horarios_detalles = session.query(TbHorarioDetalle).filter(
                TbHorarioDetalle.id_horario_encb == id_horario_encb, TbHorarioDetalle.estatus == 1).all()
            if not horarios_detalles:
                return False

            for detalle in horarios_detalles:
                detalle.estatus = 0
                session.commit()
                logger.info(
                    f"Detalle de horario con ID {detalle.id_horario_deta} eliminado")

            return True
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error eliminando proveedor: {str(e)}")
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error: {str(e)}")
            return False
        finally:
            session.close()

    # Leer (encb/deta) (/horarios/obtener_horarios_por_fecha)
    def obtener_horarios_por_fecha(self, fecha_inicio, fecha_fin):
        session = self.session_factory
        try:
            horarios = session.query(VwHorariosCompletos).filter(VwHorariosCompletos.fecha_inicio >= fecha_inicio, VwHorariosCompletos.fecha_fin <= fecha_fin, VwHorariosCompletos.estatus == 1).all()
            
            if not horarios:
                return True, {}
            horarios_respuesta = []
            current_encabezado = None
            detalles = []

            for row in horarios:
                if current_encabezado != row.id_horario_encb:
                    # Si ya hay un encabezado previo, añadirlo a la respuesta
                    if current_encabezado is not None:
                        horarios_respuesta.append({
                            "id_horario_encb": current_encabezado,
                            "fecha_inicio": fecha_inicio.isoformat(),
                            "fecha_fin": fecha_fin.isoformat(),
                            "detalles": detalles
                        })
                    # Actualizar con el nuevo encabezado
                    current_encabezado = row.id_horario_encb
                    fecha_inicio = row.fecha_inicio
                    fecha_fin = row.fecha_fin
                    detalles = []

                # Crear la estructura del detalle para cada empleado
                detalles.append(
                    {
                        "id_empleado": row.id_empleado,
                        "nombre_empleado": row.nombre_empleado,
                        "rol_empleado": row.rol_empleado,
                        "turnos": {
                            "domingo": row.turno_domingo,
                            "lunes": row.turno_lunes,
                            "martes": row.turno_martes,
                            "miercoles": row.turno_miercoles,
                            "jueves": row.turno_jueves,
                            "sabado": row.turno_sabado,
                            "viernes": row.turno_viernes
                        }
                    }
                )

            # Añadir el último encabezado con sus detalles
            if current_encabezado is not None:
                horarios_respuesta.append({
                    "id_horario_encb": current_encabezado,
                    "fecha_inicio": fecha_inicio.isoformat(),
                    "fecha_fin": fecha_fin.isoformat(),
                    "detalles": detalles
                })

            # Formar la respuesta final
            if horarios_respuesta:
                respuesta = horarios_respuesta[0]  # Solo tomamos el primer horario
                return True, respuesta  # Retornar la respuesta en formato esperado

            return False, {}
        except SQLAlchemyError as e:
            logger.error(f"Error obteniendo los horarios: {str(e)}")
            return False, {}
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return False, {}
        finally:
            session.close()            
    
    # Leer (detalles) (/horarios/obtener_horarios_por_id)
    def obtener_horarios_por_id(self, id_horario_encb):
        sesion = self.session_factory
        try:
            # Ejecutar la consulta para obtener todos los horarios completos
            horarios = sesion.query(VwHorariosCompletos).filter(VwHorariosCompletos.id_horario_encb == id_horario_encb, VwHorariosCompletos.estatus == 1).all()

            horarios_respuesta = []  # Lista para almacenar los horarios completos
            current_encabezado = None
            detalles = []

            for row in horarios:
                if current_encabezado != row.id_horario_encb:
                    # Si ya hay un encabezado previo, añadirlo a la respuesta
                    if current_encabezado is not None:
                        horarios_respuesta.append({
                            "id_horario_encb": current_encabezado,
                            "fecha_inicio": fecha_inicio.isoformat(),
                            "fecha_fin": fecha_fin.isoformat(),
                            "detalles": detalles
                        })
                    # Actualizar con el nuevo encabezado
                    current_encabezado = row.id_horario_encb
                    fecha_inicio = row.fecha_inicio
                    fecha_fin = row.fecha_fin
                    detalles = []

                # Crear la estructura del detalle para cada empleado
                detalles.append(
                    {
                        "id_empleado": row.id_empleado,
                        "nombre_empleado": row.nombre_empleado,
                        "rol_empleado": row.rol_empleado,
                        "turnos": {
                            "domingo": row.turno_domingo,
                            "lunes": row.turno_lunes,
                            "martes": row.turno_martes,
                            "miercoles": row.turno_miercoles,
                            "jueves": row.turno_jueves,
                            "sabado": row.turno_sabado,
                            "viernes": row.turno_viernes
                        }
                    }
                )

            # Añadir el último encabezado con sus detalles
            if current_encabezado is not None:
                horarios_respuesta.append({
                    "id_horario_encb": current_encabezado,
                    "fecha_inicio": fecha_inicio.isoformat(),
                    "fecha_fin": fecha_fin.isoformat(),
                    "detalles": detalles
                })

            # Formar la respuesta final
            if horarios_respuesta:
                respuesta = horarios_respuesta[0]  # Solo tomamos el primer horario
                return True, respuesta  # Retornar la respuesta en formato esperado

            return False, {}

        except SQLAlchemyError as e:
            logger.error(f"Error obteniendo los horarios: {str(e)}")
            return False, {}
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return False, {}
        finally:
            sesion.close()

    # Leer (encabezado) (/horarios/obtener_horarios_enc)
    def obtener_horarios_enc(self):
        session = self.session_factory
        try:
            # Ejecutar la consulta para obtener todos los horarios completos
            horarios = session.query(TbHorarioEncabezado).filter(
                TbHorarioEncabezado.estatus == 1).all()

            if not horarios:
                return True, []

            horarios_list = [
                {
                    "id_horario_encb": horario.id_horario_encb,
                    "clave_horario": horario.clave_horario,
                    "fecha_inicio": horario.fecha_inicio.isoformat() if horario.fecha_inicio else None,
                    "fecha_fin": horario.fecha_fin.isoformat() if horario.fecha_fin else None,
                }
                for horario in horarios
            ]
            return True, horarios_list
        except SQLAlchemyError as e:
            logger.error(f"Error obteniendo los horarios: {str(e)}")
            return False, []
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return False, []
        finally:
            session.close()

    def generar_clave_horario(self):
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        clave = f'HORARIO_{timestamp}'
        return clave
