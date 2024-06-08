import argparse
import funciones as fn

def main():
    parser = argparse.ArgumentParser(description="Gestor de Tareas")
    parser.add_argument('--agregar', type=str, nargs='+', help="Agregar una nueva tarea")
    parser.add_argument('--completar', type=int, help="Marcar una tarea como completada")
    parser.add_argument('--eliminar', type=int, help="Eliminar una tarea")
    parser.add_argument('--buscar', type=str, help="Buscar tareas por descripción")
    parser.add_argument('--listar', action='store_true', help="Listar todas las tareas")
    parser.add_argument('--eliminarAll', action='store_true', help="Eliminar todas las tareas")
    parser.add_argument('--filtrar', type=str, help="Filtrar por Prioridad las tareas")
    parser.add_argument('--expirar', action='store_true', help="Mostrar tareas por expirar")
    parser.add_argument('--exportarTareas', action='store_true', help="Exportar todas las tareas CSV file.")


    args = parser.parse_args()

    if args.agregar:
        prioridad = args.agregar[2] if len(args.agregar) > 1 else None
        expireDate = args.agregar[1]
        tarea = fn.agregar_tarea(args.agregar[0],expireDate , prioridad)
       
    elif args.completar:
        tarea = fn.completar_tarea(args.completar)
        if tarea:
            print(f"\nTarea completada: {tarea}")
        else:
            print("\nTarea no encontrada")
    elif args.eliminar:
        if fn.eliminar_tarea(args.eliminar):
            print("\nTarea eliminada")
        else:
            print("\nTarea no encontrada")
    elif args.buscar:
        tareas = fn.buscar_tareas(args.buscar)
        print("\nTareas encontradas:", tareas)
    elif args.listar:
        fn.listar_tareas()
        
    elif args.eliminarAll:
        fn.eliminar_all()

    elif args.filtrar:
        fn.filtrar(args.filtrar)

    elif args.expirar:
        fn.expirar()
    elif args.exportarTareas:
        fn.exportarTareas()
       

if __name__ == "__main__":
    main()
    print("\n*----- FIN DEL PROGRAMA -----*")
    print("\n")