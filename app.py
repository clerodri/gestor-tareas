import  funciones as fn


def mostrar_menu():
    print("\n******** ---- Gestor de tareas ----  ********\n")
    print("Menú de opciones")
    print("1. Añadir tarea")
    print("2. Ver tareas")
    print("3. Marcar tarea como completada")
    print("4. Eliminar tarea")
    print("5. Salir")

def main():
    while True:
        mostrar_menu()
        print("\n")
        opcion = input("Ingresar opcion: ")
        print("\n")
        if opcion == '1':
            fn.agregar_tarea(fn.tareas);
        elif opcion == '2':
            fn.ver_tareas(fn.tareas);
        elif opcion == '3':
            fn.tarea_completada(fn.tareas);
        elif opcion == '4':
            fn.eliminar_tarea(fn.tareas);
        elif opcion == '5':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()
