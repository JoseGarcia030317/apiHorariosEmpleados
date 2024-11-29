from sqlalchemy import Column, Date, Integer, PrimaryKeyConstraint, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TbHorarioEncabezado(Base):
    __tablename__ = 'Horario_Encabezado'

    id_horario_encb = Column(Integer, primary_key=True, autoincrement=True)
    clave_horario = Column(String(50))
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    estatus = Column(Integer, default=1)

class TbHorarioDetalle(Base):
    __tablename__ = 'Horario_Detalle'

    id_horario_deta = Column(Integer, primary_key=True, autoincrement=True)
    id_horario_encb = Column(Integer)
    id_empleado = Column(Integer)
    empleado = Column(String)
    rol = Column(String)
    turno_viernes = Column(String(10))
    turno_sabado = Column(String(10))
    turno_domingo = Column(String(10))
    turno_lunes = Column(String(10))
    turno_martes = Column(String(10))
    turno_miercoles = Column(String(10))
    turno_jueves = Column(String(10))
    estatus = Column(Integer, default=1)
    fecha_actualiza = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=True)

class VwHorariosCompletos(Base):
    __tablename__ = 'vw_horarios_completo'
    __table_args__ = (
        PrimaryKeyConstraint('id_horario_encb', 'id_horario_deta'),
    )

    # Encabezado
    id_horario_encb = Column(Integer)
    clave_horario = Column(String)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)

    # Detalle
    id_horario_deta= Column(Integer)
    id_empleado = Column(Integer)
    nombre_empleado = Column(String)
    # apellido_pat = Column(String)
    # apellido_mat = Column(String)
    rol_empleado = Column(String)
    turno_viernes = Column(String)
    turno_sabado = Column(String)
    turno_domingo = Column(String)
    turno_lunes = Column(String)
    turno_martes = Column(String)
    turno_miercoles = Column(String)
    turno_jueves = Column(String)
    estatus = Column(Integer)
    # fecha_actualiza = Column(DateTime)