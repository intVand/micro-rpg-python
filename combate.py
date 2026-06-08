# Lógica de estados y turnos
def gestionar_inicio_turno(personaje):
    """
    Se ejecuta al inicio del turno de cualquier personaje.
    Controla las siguientes acciones:
    1. Reducir el contador de recarga de la habilidad.
    2. Aplicar daño por Veneno.
    3. Comprobar si está Paralizado.

    Return:
    - mensaje (str): Texto que describe que ha ocurrido.
    - puede_actuar (bool): True si puede jugar, False si está paralizado.
    """
    mensaje = ""
    puede_actuar = True

    # Reducir el contador de recarga de habilidad
    personaje.reducir_recarga()

    # Efecto Veneno
    if personaje.estado == "veneno":
        danyo_veneno = personaje.danyo_veneno_acumulado
        personaje.recibir_danyo(danyo_veneno)
        mensaje += f"{personaje.nombre} sufre {danyo_veneno} de daño por el Veneno.\n"

    # Efecto Paralizado
    if personaje.estado == "paralizado":
        mensaje += f"{personaje.nombre} está paralizado y pierde su turno.\n"
        puede_actuar = False
        personaje.estado = "normal"

    return mensaje, puede_actuar


# IA del enemigo
def ia_enemigo(atacante, defensor):
    """
    Decide qué hace la máquina.
    Prioridad: Si puede usar la habilidad, la usa. Si no, ataque normal.
    """

    mensaje_turno = ""

    # Se gestionan los estados
    mensaje_estado, puede_actuar = gestionar_inicio_turno(atacante)
    mensaje_turno += mensaje_estado

    # Si está vivo y no está paralizado, actúa
    if atacante.esta_vivo() and puede_actuar:
        
        if atacante.puede_usar_habilidad():
            resultado = atacante.usar_habilidad(defensor)
            mensaje_turno += resultado

        else:
            resultado = atacante.atacar(defensor)
            mensaje_turno += resultado

    elif not atacante.esta_vivo():
        mensaje_turno += f"{atacante.nombre} ha sido derrotado por el veneno antes de moverse."

    return mensaje_turno


# Comprobación de victoria
def comprobar_victoria(jugador, enemigo):
    """
    Return:
    - 0: El combate sigue.
    - 1: Ganó el Jugador.
    - 2: Ganó el Enemigo.
    """

    if not enemigo.esta_vivo():
        return 1
    
    if not jugador.esta_vivo():
        return 2
    
    return 0