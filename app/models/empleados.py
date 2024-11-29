from sqlalchemy import Column, Date, Integer, Numeric, String, DateTime, ForeignKey, Sequence, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Modelos de las tablas
class TbEmpleado(Base):
    __tablename__ = 'Empleados'

    id_empleado = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))
    apellido_pat = Column(String(100))
    apellido_mat = Column(String(100))
    id_rol = Column(Integer)
    email = Column(String(100))
    telefono = Column(String(15))

# Modelos de las vistas
class VwEmpleados(Base):
    __tablename__ = 'vw_empleados_roles'

    id_empleado = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido_pat = Column(String)
    apellido_mat = Column(String)
    email = Column(String)
    telefono = Column(String)
    id_rol = Column(Integer)
    rol = Column(String)