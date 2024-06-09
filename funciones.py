from models.tarea import Tarea, SessionLocal
from functools import wraps
from sqlalchemy import func
import validation as v
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


@manejar_sesion
def expirar(session):
    now = datetime.now()
    today_str = now.strftime('%Y-%m-%d')
    print(f"\nFecha actual: {now}" )
    print("\nLas tareas proximas a vencer son: " )
    displayList(session.query(Tarea).filter( func.date(Tarea.fecha_vencimiento) == today_str).all())


@manejar_sesion
def filtrar(session, prioridad):
    v.validar_prioridad(prioridad=prioridad)
    print(f"\nLas tareas con PRIORIDAD  {prioridad} son: " )
    displayList(session.query(Tarea).filter(Tarea.prioridad.contains(prioridad)).all())



@manejar_sesion
def agregar_tarea(session, args):
    prioridad = v.validar_prioridad(prioridad=args[2])
    date_fecha_exp = v.validar_expirer(args[1])
    nueva_tarea = Tarea(descripcion=args[0], prioridad=prioridad, fecha_vencimiento = date_fecha_exp)
    session.add(nueva_tarea)
    session.commit()
    session.refresh(nueva_tarea)
    print(f"\nTarea agregada: {nueva_tarea}")



@manejar_sesion
def listar_tareas(session):
    print("\nTodas las tareas:")
    displayList(session.query(Tarea).all())
    

@manejar_sesion
def completar_tarea(session,tarea_id):
    v.validar_id(tarea_id)
    tarea = session.query(Tarea).filter(Tarea.id == tarea_id).first()
    if not tarea:
        print(f"\nTarea con ID = {tarea_id} no encontrada")
        return 
    if tarea.completada:
        print(f"\nTarea con ID = {tarea_id} ya esta finalizada")
    else:
        tarea.completada = True
        tarea.fecha_finalizacion = datetime.now()
        session.commit()
        session.refresh(tarea)
        print(f"\nTarea completada: {tarea}")
    


@manejar_sesion
def eliminar_tarea(session, tarea_id):
    v.validar_id(tarea_id)
    tarea = session.query(Tarea).filter(Tarea.id == tarea_id).first()
    if tarea:
        session.delete(tarea)
        session.commit()
        print(f"\nTarea con ID = {tarea_id} eliminada")
    else:
        print(f"\nTarea con ID = {tarea_id} no encontrada")

@manejar_sesion
def eliminar_all(session):
    session.query(Tarea).delete()
    session.commit()
    print("\nTareas eliminadas")
    

@manejar_sesion
def buscar_tareas(session, descripcion):
    tareas = session.query(Tarea).filter(Tarea.descripcion.contains(descripcion)).all()
    if tareas:
        print("\nTarea encontrada:")
        displayList(tareas)
        return
    print("\nTarea No encontrada:")
    

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


@manejar_sesion
def listarCompletadas(session):
    print("\nTodas las tareas completadas:")
    displayList(session.query(Tarea).filter(Tarea.completada==True).all())


def displayList(tareas):
    for tarea in tareas:
        print(f"\n{tarea}")