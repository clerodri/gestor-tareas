from datetime import datetime


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

def validar_id(id):
    try:
        int(id)
    except ValueError as e:
        raise ValueError("El ID debe ser un número entero.") from e
    if id is None:
        raise ValueError("El ID no puede ser nulo.")