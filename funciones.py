from models.tarea import Tarea, SessionLocal
from functools import wraps
from sqlalchemy import func
from datetime import datetime
import csv
def manejar_sesion(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = SessionLocal()
        try:
            resultado = func(session, *args, **kwargs)
            return resultado
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()
    return wrapper


def validar_expirer(expirer):
    try:
        expirer_datetime = datetime.strptime(expirer, '%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        raise ValueError(f"Fecha inválida: {expirer} . Debe ser formato: '%Y-%m-%d %H:%M:%S'") from e
    
    now = datetime.now()
    if(expirer_datetime < now):
        raise ValueError(f"Fecha de Vencimiento Invalida: {expirer} . Debe ser una fecha futura a la actual")
    return expirer_datetime


def validar_prioridad(prioridad):
    valid_prioridades = ["Baja", "Alta", "Media"]
    if prioridad not in valid_prioridades:
        raise ValueError(f"Prioridad inválida: {prioridad}. Opciones Validas: {valid_prioridades}.")
    return prioridad



@manejar_sesion
def expirar(session):
    now = datetime.now()
    today_str = now.strftime('%Y-%m-%d')
    print(f"\nFecha actual: {now}" )
    print("\nLas tareas proximas a vencer son: " )
    print("\n", session.query(Tarea).filter( func.date(Tarea.fecha_vencimiento) == today_str).all())


@manejar_sesion
def filtrar(session, prioridad):
    validar_prioridad(prioridad=prioridad)
    print(f"\nLas tareas con PRIORIDAD  {prioridad} son: " )
    print("\n", session.query(Tarea).filter(Tarea.prioridad.contains(prioridad)).all())


@manejar_sesion
def agregar_tarea(session, descripcion: str, fecha_exp, prioridad: str = None ):
    validar_prioridad(prioridad=prioridad)
    date_fecha_exp = validar_expirer(fecha_exp)
    nueva_tarea = Tarea(descripcion=descripcion, prioridad=prioridad, fecha_vencimiento = date_fecha_exp)
    session.add(nueva_tarea)
    session.commit()
    session.refresh(nueva_tarea)
    print(f"\nTarea agregada: {nueva_tarea}")
    return nueva_tarea


@manejar_sesion
def listar_tareas(session):
    print("\nTodas las tareas:", session.query(Tarea).all())
    

@manejar_sesion
def completar_tarea(session,tarea_id):
    tarea = session.query(Tarea).filter(Tarea.id == tarea_id).first()
    if tarea:
        tarea.completada = True
        session.commit()
        session.refresh(tarea)
    return tarea

@manejar_sesion
def eliminar_tarea(session, tarea_id):
    tarea = session.query(Tarea).filter(Tarea.id == tarea_id).first()
    if tarea:
        session.delete(tarea)
        session.commit()
        return True
    return False

@manejar_sesion
def eliminar_all(session):
    session.query(Tarea).delete()
    session.commit()
    print("\nTareas eliminadas")
    

@manejar_sesion
def buscar_tareas(session, termino):
    return session.query(Tarea).filter(Tarea.descripcion.contains(termino)).all()
    

@manejar_sesion
def exportarTareas(session,filename='tareas_data.csv'):
    try:
        tareas = session.query(Tarea).all()
        if not tareas:
            raise ValueError("No hay tareas para exportar.")
        headers = ['id', 'descripcion', 'completada', 'prioridad' ,'fecha_vencimiento']  
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            
            for tarea in tareas:
                writer.writerow([
                    tarea.id, 
                    tarea.descripcion, 
                    tarea.completada,
                    tarea.prioridad,
                    tarea.fecha_vencimiento.strftime('%Y-%m-%d %H:%M:%S')  
                ])
        print(f"Las tareas exportadas exitosamente a {filename}.")
    except Exception as e:
        print(f"Error al exportar: {e}")