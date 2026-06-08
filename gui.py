import tkinter as tk
import random
import persistencia
import combate

from virus import Virus
from bacteria import Bacteria
from globulo_blanco import GlobuloBlanco
from hongo import Hongo
from parasito import Parasito

# Variables Globales
personajes_creados = []
jugador_actual = None
enemigo_actual = None

# Motor de escenas
def cambiar_escena(escena_nueva):
    """Oculta todas las escenas y muestra la escena solicitada."""

    escena_menu.pack_forget()
    escena_crear.pack_forget()
    escena_ver.pack_forget()
    escena_seleccion.pack_forget()
    escena_combate.pack_forget()

    escena_nueva.pack(fill="both", expand=True)

# Acciones del menu principal
def accion_guardar():
    """
    Valida que existan personajes en memoria y, de ser así, invoca al módulo 
    de persistencia para guardar la lista actual en el archivo JSON.
    """

    if len(personajes_creados) == 0:
        label_estado.config(text="No tienes ningún personaje creado para guardar.", fg="#F39C12")
        return
    
    persistencia.guardar_personajes(personajes_creados)
    label_estado.config(text="Partida guardada en personajes.json.", fg="#2ECC71")

def accion_cargar():
    """
    Carga los personajes desde el archivo JSON utilizando el módulo de persistencia.
    Implementa un filtro para evitar duplicados exactos antes de añadirlos a la lista de personajes.
    """

    global personajes_creados
    personajes_cargados = persistencia.cargar_personajes()

    if not personajes_cargados:
        label_estado.config(text="El archivo JSON está vacío o no existe.", fg="#F39C12")
        return
    
    nuevos_añadidos = 0
    for pj_nuevo in personajes_cargados:
        # Se comprueba si ya existe uno igual en nuestra lista actual
        es_duplicado = False
        for pj_existente in personajes_creados:
            if pj_existente.nombre == pj_nuevo.nombre and pj_existente.__class__.__name__ == pj_nuevo.__class__.__name__:
                es_duplicado = True
                break
        
        # Si no es duplicado, se añade a nuestra lista
        if not es_duplicado:
            personajes_creados.append(pj_nuevo)
            nuevos_añadidos += 1
            
    if nuevos_añadidos > 0:
        label_estado.config(text=f"Se añadieron {nuevos_añadidos} personajes del JSON. (Total: {len(personajes_creados)})", fg="#3498DB")
    else:
        label_estado.config(text="Los personajes del JSON ya estaban en el sistema.", fg="#F39C12")

def accion_ver():
    """
    Prepara y formatea el texto para la escena de 'Ver Personajes'.
    Calcula el 'Win Rate' de cada personaje y genera un Ranking Top 3,
    seguido del listado completo con las estadísticas de todos los personajes.
    """

    area_texto_ver.config(state=tk.NORMAL)
    area_texto_ver.delete(1.0, tk.END)
    
    if not personajes_creados:
        area_texto_ver.insert(tk.END, "No hay personajes creados todavía.\n¡Crea uno o carga tu archivo JSON!")

    else:
        def calcular_win_rate(p):
            total = p.victorias + p.derrotas
            return (p.victorias / total) if total > 0 else 0

        ranking = sorted(personajes_creados, key=calcular_win_rate, reverse=True)
        
        area_texto_ver.insert(tk.END, "RANKING TOP 3 (POR WIN RATE)\n", "titulo")
        area_texto_ver.insert(tk.END, "=" * 55 + "\n")
        
        top = min(3, len(ranking))
        for i in range(top):
            pj = ranking[i]
            rate = calcular_win_rate(pj) * 100
            area_texto_ver.insert(tk.END, f"#{i+1} {pj.nombre} | Win Rate: {rate:.1f}% ({pj.victorias}V/{pj.derrotas}D)\n")
        
        area_texto_ver.insert(tk.END, "\nLISTADO COMPLETO\n")
        area_texto_ver.insert(tk.END, "=" * 55 + "\n")
        
        for pj in personajes_creados:
            area_texto_ver.insert(tk.END, f"{str(pj)}\n")
            area_texto_ver.insert(tk.END, "-" * 55 + "\n")
            
    area_texto_ver.tag_config("titulo", foreground="#F1C40F", font=("Consolas", 12, "bold"))
    area_texto_ver.config(state=tk.DISABLED)
    cambiar_escena(escena_ver)

# Lógica de creación de personajes
def accion_confirmar_creacion():
    """
    Valida la entrada de texto del usuario y la clase seleccionada.
    Previene la creación de personajes con nombres vacíos o duplicados idénticos.
    Si pasa la validación, instancia el objeto de la subclase correspondiente y lo guarda.
    """

    nombre = var_nombre.get().strip()
    clase_elegida = var_clase.get()
    
    # Se valida que se le haya asigando un nombre
    if not nombre:
        label_error_crear.config(text="El nombre no puede estar vacío.")
        return
    
    # Se valida que no exista ya un personaje igual, antes de crearlo
    for pj in personajes_creados:
        if pj.nombre == nombre and pj.__class__.__name__ == clase_elegida:
            label_error_crear.config(text=f"Ya existe un {clase_elegida} llamado '{nombre}'.")
            return
        
    if clase_elegida == "Virus":
        nuevo_pj = Virus(nombre)

    elif clase_elegida == "GlobuloBlanco":
        nuevo_pj = GlobuloBlanco(nombre)

    elif clase_elegida == "Hongo":
        nuevo_pj = Hongo(nombre)

    elif clase_elegida == "Parasito":
        nuevo_pj = Parasito(nombre)

    elif clase_elegida == "Bacteria":
        nuevo_pj = Bacteria(nombre)
        
    personajes_creados.append(nuevo_pj)
    
    var_nombre.set("") 
    label_error_crear.config(text="")
    label_estado.config(text=f"¡{clase_elegida} '{nombre}' creado con éxito!", fg="#2ECC71")
    cambiar_escena(escena_menu)

# Lógica de selección de combate
def abrir_escena_seleccion():
    """
    Prepara la interfaz de selección de luchadores.
    Comprueba que haya suficientes personajes creados, limpia los Listbox anteriores
    y los rellena con las opciones disponibles, incluyendo la opción 'Aleatorio'.
    """

    if len(personajes_creados) < 2:
        label_estado.config(text="Necesitas al menos 2 personajes para combatir.", fg="#E74C3C")
        return

    listbox_jugador.delete(0, tk.END)
    listbox_enemigo.delete(0, tk.END)

    listbox_jugador.insert(tk.END, "Aleatorio")
    listbox_enemigo.insert(tk.END, "Aleatorio")

    for pj in personajes_creados:
        texto_lista = f"{pj.nombre} ({pj.__class__.__name__})"
        listbox_jugador.insert(tk.END, texto_lista)
        listbox_enemigo.insert(tk.END, texto_lista)

    # Por defecto se deja seleccionado el aleatorio
    listbox_jugador.selection_set(0)
    listbox_enemigo.selection_set(0)
    label_error_seleccion.config(text="")

    cambiar_escena(escena_seleccion)

def confirmar_seleccion_combate():
    """
    Procesa la selección de los Listbox para determinar el jugador y el enemigo.
    Resuelve las selecciones 'Aleatorio' asegurando que no se enfrente el mismo
    personaje contra sí mismo. Finaliza preparando la arena gráfica y los sprites.
    """

    global jugador_actual, enemigo_actual

    sel_jugador = listbox_jugador.curselection()
    sel_enemigo = listbox_enemigo.curselection()

    if not sel_jugador or not sel_enemigo:
        label_error_seleccion.config(text="Selecciona un luchador en ambas listas.")
        return

    idx_jugador = sel_jugador[0]
    idx_enemigo = sel_enemigo[0]

    # Jugador
    if idx_jugador == 0: # 0 es la posición de "Aleatorio"
        jugador_actual = random.choice(personajes_creados)

    else:
        # Restamos 1 porque el índice 0 lo ocupa "Aleatorio"
        jugador_actual = personajes_creados[idx_jugador - 1]

    # Enemigo
    if idx_enemigo == 0:
        # Filtramos para que el enemigo aleatorio no sea el jugador que ya tenemos
        enemigos_validos = [p for p in personajes_creados if p != jugador_actual]

        if not enemigos_validos:
            label_error_seleccion.config(text="No hay suficientes personajes distintos.")
            return
        
        enemigo_actual = random.choice(enemigos_validos)

    else:
        enemigo_actual = personajes_creados[idx_enemigo - 1]

    # Validación final
    if jugador_actual == enemigo_actual:
        label_error_seleccion.config(text="¡No puedes elegir al mismo personaje para ambos bandos!")
        return
    
    log_combate.config(state=tk.NORMAL)
    log_combate.delete(1.0, tk.END)
    log_combate.config(state=tk.DISABLED)
    
    btn_atacar.config(state=tk.NORMAL)
    btn_habilidad.config(state=tk.NORMAL)
    btn_salir_combate.pack_forget()
    
    img_jugador = diccionario_sprites.get(jugador_actual.__class__.__name__)
    img_enemigo = diccionario_sprites.get(enemigo_actual.__class__.__name__)
    
    lbl_sprite_jugador.config(image=img_jugador)
    lbl_sprite_enemigo.config(image=img_enemigo)

    imprimir_log(f"¡COMBATE INICIADO!\n{jugador_actual.nombre} VS {enemigo_actual.nombre}\n")
    cambiar_escena(escena_combate)
    preparar_turno_jugador()

# Motor de combate y animaciones
def animar_salto(label_sprite, relx_original):
    """Mueve el sprite hacia arriba y lo devuelve a su sitio 150ms después."""

    label_sprite.place(relx=relx_original, rely=0.3, anchor="center") # Sube (rely más pequeño)
    ventana.after(150, lambda: label_sprite.place(relx=relx_original, rely=0.5, anchor="center")) # Baja al centro

def animar_parpadeo(label_sprite, relx_original, iteracion=0):
    """Hace que el sprite desaparezca y aparezca rápidamente simulando daño."""

    if iteracion < 4: # Lo hacemos parpadear un par de veces
        if iteracion % 2 == 0:
            label_sprite.place_forget() # Oculta la imagen
        else:
            label_sprite.place(relx=relx_original, rely=0.5, anchor="center") # La muestra
            
        # Vuelve a llamarse a sí misma tras 100ms
        ventana.after(100, lambda: animar_parpadeo(label_sprite, relx_original, iteracion + 1))
    else:
        # Al terminar, nos aseguramos de que se quede visible
        label_sprite.place(relx=relx_original, rely=0.5, anchor="center")

def imprimir_log(mensaje):
    """
    Muestra información acerca del combate en la caja de texto del combate y realiza 
    un auto-scroll hacia abajo para mostrar siempre la acción más reciente.
    """
    log_combate.config(state=tk.NORMAL)
    log_combate.insert(tk.END, mensaje + "\n")
    log_combate.see(tk.END)
    log_combate.config(state=tk.DISABLED)

def actualizar_barras_vida():
    """Refresca visualmente las etiquetas de los Puntos de Vida y las recargas de habilidad."""

    lbl_hp_jugador.config(text=f"{jugador_actual.nombre} [PV: {jugador_actual.vida}/{jugador_actual.vida_maxima}]\nRecarga: {jugador_actual.recarga_actual}")
    lbl_hp_enemigo.config(text=f"{enemigo_actual.nombre} [PV: {enemigo_actual.vida}/{enemigo_actual.vida_maxima}]")

def evaluar_victoria():
    """
    Comprueba mediante el módulo de combate si los PV de alguien han llegado a 0.
    De ser así, detiene el combate, reparte los puntos de estadística (victorias/derrotas),
    cura a los personajes y muestra el botón de salida.
    Return: True si el combate ha terminado, False si continúa.
    """

    resultado = combate.comprobar_victoria(jugador_actual, enemigo_actual)

    if resultado != 0:
        actualizar_barras_vida()

        btn_atacar.config(state=tk.DISABLED)
        btn_habilidad.config(state=tk.DISABLED)
        btn_salir_combate.pack(pady=10)
        
        imprimir_log("\n" + "="*30)

        if resultado == 1:
            imprimir_log(f"¡VICTORIA! Has derrotado a {enemigo_actual.nombre}.")
            jugador_actual.victorias += 1
            enemigo_actual.derrotas += 1

        elif resultado == 2:
            imprimir_log(f"DERROTA... {enemigo_actual.nombre} te ha aniquilado.")
            enemigo_actual.victorias += 1
            jugador_actual.derrotas += 1

        jugador_actual.curar_y_limpiar()
        enemigo_actual.curar_y_limpiar()

        return True
    return False

def preparar_turno_jugador():
    """
    Gestiona el inicio del turno del jugador. 
    Aplica estados alterados y reduce recargas de habilidad mediante el módulo 'combate'. 
    Si el jugador está paralizado, le hace perder el turno automáticamente.
    """

    imprimir_log(f"\n--- NUEVO TURNO ---")

    msg_estado, puede_actuar = combate.gestionar_inicio_turno(jugador_actual)

    if msg_estado: imprimir_log(msg_estado)

    actualizar_barras_vida()
    
    if evaluar_victoria(): return
    
    if not puede_actuar:
        imprimir_log("Estás paralizado y pierdes tu turno.")
        iniciar_retraso_enemigo()

    else:
        btn_atacar.config(state=tk.NORMAL)
        btn_habilidad.config(state=tk.NORMAL)

def accion_atacar(es_habilidad):
    """
    Callback de los botones de ataque. 
    Ejecuta el ataque o la habilidad, 
    dispara las animaciones correspondientes y cede el turno al enemigo.
    """

    btn_atacar.config(state=tk.DISABLED)
    btn_habilidad.config(state=tk.DISABLED)
    
    animar_salto(lbl_sprite_jugador, 0.25)

    if es_habilidad:
        imprimir_log(jugador_actual.usar_habilidad(enemigo_actual))

    else:
        imprimir_log(jugador_actual.atacar(enemigo_actual))
        
    animar_parpadeo(lbl_sprite_enemigo, 0.75)    
    actualizar_barras_vida()

    if evaluar_victoria(): return

    iniciar_retraso_enemigo()

def iniciar_retraso_enemigo():
    """
    Simula que el enemigo está pensando antes de atacar.
    Lo que proporciona realismo y tiempo al usuario para leer el log de combate.
    """

    imprimir_log("\nEl enemigo está preparando su movimiento...")
    tiempo_espera = random.randint(1000, 2000) # De 1 a 2 segundos aleatorios
    ventana.after(tiempo_espera, procesar_turno_enemigo)    

def procesar_turno_enemigo():
    """
    Ejecuta el turno de la IA, gestionando primero sus efectos de estado,
    realizando su animación de salto y aplicando el daño al jugador.
    """

    imprimir_log(f"\nTurno de la máquina...")

    animar_salto(lbl_sprite_enemigo, 0.75)

    imprimir_log(combate.ia_enemigo(enemigo_actual, jugador_actual))

    animar_parpadeo(lbl_sprite_jugador, 0.25)

    actualizar_barras_vida()

    if evaluar_victoria(): return

    preparar_turno_jugador()

# Construcción de la Interfaz
def construir_menu():
    """Construye los widgets estáticos de la pantalla de Menú Principal."""

    tk.Label(escena_menu, text="MICRO-RPG", font=("Helvetica", 28, "bold"), bg="#1A252C", fg="white").pack(pady=30)
    frame_btn = tk.Frame(escena_menu, bg="#1A252C")
    frame_btn.pack(pady=10)

    tk.Button(frame_btn, text="1. Crear Personaje", command=lambda: cambiar_escena(escena_crear), **estilo_btn).grid(row=0, column=0, padx=10, pady=10)
    tk.Button(frame_btn, text="2. Ver Personajes", command=accion_ver, **estilo_btn).grid(row=0, column=1, padx=10, pady=10)
    tk.Button(frame_btn, text="3. INICIAR COMBATE", command=abrir_escena_seleccion, font=("Arial", 14, "bold"), bg="#E74C3C", fg="white", width=34, height=2).grid(row=1, column=0, columnspan=2, padx=10, pady=15)
    tk.Button(frame_btn, text="4. Guardar (JSON)", command=accion_guardar, **estilo_btn).grid(row=2, column=0, padx=10, pady=10)
    tk.Button(frame_btn, text="5. Cargar (JSON)", command=accion_cargar, **estilo_btn).grid(row=2, column=1, padx=10, pady=10)
    tk.Button(frame_btn, text="6. Salir", command=ventana.quit, **estilo_btn).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

def construir_crear():
    """Construye los widgets estáticos del formulario de Creación de Personajes."""

    tk.Label(escena_crear, text="Crear Microorganismo", font=("Arial", 20, "bold"), bg="#1A252C", fg="white").pack(pady=30)
    tk.Label(escena_crear, text="Nombre del personaje:", bg="#1A252C", fg="white", font=("Arial", 12)).pack(pady=5)
    tk.Entry(escena_crear, textvariable=var_nombre, font=("Arial", 14), width=25).pack(pady=5)

    tk.Label(escena_crear, text="Elige su Clase:", bg="#1A252C", fg="white", font=("Arial", 12)).pack(pady=15)
    frame_cls = tk.Frame(escena_crear, bg="#1A252C")
    frame_cls.pack()
    tk.Radiobutton(frame_cls, text="Virus", variable=var_clase, value="Virus", bg="#1A252C", fg="white", selectcolor="#34495E", font=("Arial", 11)).grid(row=0, column=0, padx=10)
    tk.Radiobutton(frame_cls, text="Glóbulo Blanco", variable=var_clase, value="GlobuloBlanco", bg="#1A252C", fg="white", selectcolor="#34495E", font=("Arial", 11)).grid(row=0, column=1, padx=10)
    tk.Radiobutton(frame_cls, text="Hongo", variable=var_clase, value="Hongo", bg="#1A252C", fg="white", selectcolor="#34495E", font=("Arial", 11)).grid(row=0, column=2, padx=10)
    tk.Radiobutton(frame_cls, text="Parásito", variable=var_clase, value="Parasito", bg="#1A252C", fg="white", selectcolor="#34495E", font=("Arial", 11)).grid(row=0, column=3, padx=10)
    tk.Radiobutton(frame_cls, text="Bacteria", variable=var_clase, value="Bacteria", bg="#1A252C", fg="white", selectcolor="#34495E", font=("Arial", 11)).grid(row=0, column=4, padx=10)

    label_error_crear.pack(pady=10)
    tk.Button(escena_crear, text="Confirmar y Crear", command=accion_confirmar_creacion, bg="#27AE60", fg="white", font=("Arial", 12, "bold"), width=20, height=2).pack(pady=10)
    tk.Button(escena_crear, text="Cancelar", command=lambda: cambiar_escena(escena_menu), bg="#7F8C8D", fg="white", font=("Arial", 10, "bold")).pack(pady=5)

def construir_ver():
    """Construye los widgets estáticos de la información de los personajes y Rankings."""

    tk.Label(escena_ver, text="Base de Datos Celular", font=("Arial", 20, "bold"), bg="#1A252C", fg="white").pack(pady=20)
    area_texto_ver.pack(pady=10, padx=10)
    tk.Button(escena_ver, text="Volver al Menú", command=lambda: cambiar_escena(escena_menu), bg="#7F8C8D", fg="white", font=("Arial", 12, "bold"), width=20, height=2).pack(pady=15)

def construir_seleccion():
    """Construye los widgets estáticos de la antesala al combate (Elección de rivales)."""

    tk.Label(escena_seleccion, text="Preparar Combate", font=("Arial", 20, "bold"), bg="#1A252C", fg="white").pack(pady=20)

    frame_columnas.pack(pady=10)

    # Columna jugador
    frame_jugador.grid(row=0, column=0, padx=20)
    tk.Label(frame_jugador, text="Tu Luchador:", font=("Arial", 12, "bold"), bg="#1A252C", fg="#2ECC71").pack()
    listbox_jugador.pack(pady=5)

    # Columna Enemigo
    frame_enemigo.grid(row=0, column=1, padx=20)
    tk.Label(frame_enemigo, text="Rival:", font=("Arial", 12, "bold"), bg="#1A252C", fg="#E74C3C").pack()
    listbox_enemigo.pack(pady=5)

    label_error_seleccion.pack(pady=10)

    tk.Button(escena_seleccion, text="¡COMBATIR!", command=confirmar_seleccion_combate, bg="#E74C3C", fg="white", font=("Arial", 14, "bold"), width=20, height=2).pack(pady=10)
    tk.Button(escena_seleccion, text="Volver al Menú", command=lambda: cambiar_escena(escena_menu), bg="#7F8C8D", fg="white", font=("Arial", 10, "bold")).pack(pady=5)

def construir_combate():
    """Construye los widgets estáticos de la Arena de Combate (HUD, Log, Sprites, Controles)."""

    frame_cabecera.pack(fill="x", pady=10, padx=10)
    lbl_hp_jugador.pack(side="left", padx=20, pady=10)
    tk.Label(frame_cabecera, text="VS", font=("Arial", 16, "bold"), bg="#34495E", fg="white").pack(side="left", expand=True)
    lbl_hp_enemigo.pack(side="right", padx=20, pady=10)

    frame_log.pack(pady=10)
    scrollbar.pack(side="right", fill="y")
    log_combate.pack(side="left")
    scrollbar.config(command=log_combate.yview)

    frame_acciones.pack(pady=10)
    btn_atacar.grid(row=0, column=0, padx=10)
    btn_habilidad.grid(row=0, column=1, padx=10)

# Inicialización del juego
ventana = tk.Tk()
ventana.title("Micro-RPG")

# Carga del Favicon
try:
    ventana.iconbitmap("assets/icono.ico")

except: 
    print("No se ha podido cargar el icono correctamente")

ventana.geometry("700x600")
ventana.config(bg="#1A252C")
estilo_btn = {"font": ("Arial", 12, "bold"), "width": 18, "height": 2, "bg": "#34495E", "fg": "white", "cursor": "hand2"}

# Variables y Escenas principales
var_nombre = tk.StringVar()
var_clase = tk.StringVar(value="Virus")

escena_menu = tk.Frame(ventana, bg="#1A252C")
escena_crear = tk.Frame(ventana, bg="#1A252C")
escena_ver = tk.Frame(ventana, bg="#1A252C")
escena_seleccion = tk.Frame(ventana, bg="#1A252C")
escena_combate = tk.Frame(ventana, bg="#2C3E50")

# Carga de Sprites en memoria
diccionario_sprites = {
    "Virus": tk.PhotoImage(file="assets/virus.png"),
    "GlobuloBlanco": tk.PhotoImage(file="assets/globulo_blanco.png"),
    "Bacteria": tk.PhotoImage(file="assets/bacteria.png"),
    "Hongo": tk.PhotoImage(file="assets/hongo.png"),
    "Parasito": tk.PhotoImage(file="assets/parasito.png")
}

# Widgets Globales Compartidos

#Sprites
frame_sprites = tk.Frame(escena_combate, bg="#2C3E50", height=150)
frame_sprites.pack(pady=10, fill="x")

lbl_sprite_jugador = tk.Label(frame_sprites, bg="#2C3E50")
lbl_sprite_enemigo = tk.Label(frame_sprites, bg="#2C3E50")

lbl_sprite_jugador.place(relx=0.25, rely=0.5, anchor="center")
lbl_sprite_enemigo.place(relx=0.75, rely=0.5, anchor="center")

# Etiquetas de estado e información general
label_estado = tk.Label(escena_menu, text="Bienvenid@ al sistema. Todo listo.", font=("Arial", 11, "italic"), bg="#1A252C", fg="#BDC3C7")
label_error_crear = tk.Label(escena_crear, text="", bg="#1A252C", fg="#E74C3C", font=("Arial", 11, "bold"))
area_texto_ver = tk.Text(escena_ver, font=("Consolas", 11), bg="#34495E", fg="white", width=65, height=15)

# Widgets de Selección
frame_columnas = tk.Frame(escena_seleccion, bg="#1A252C")
frame_jugador = tk.Frame(frame_columnas, bg="#1A252C")
frame_enemigo = tk.Frame(frame_columnas, bg="#1A252C")

listbox_jugador = tk.Listbox(frame_jugador, font=("Arial", 11), width=25, height=8, exportselection=False)
listbox_enemigo = tk.Listbox(frame_enemigo, font=("Arial", 11), width=25, height=8, exportselection=False)
label_error_seleccion = tk.Label(escena_seleccion, text="", bg="#1A252C", fg="#E74C3C", font=("Arial", 11, "bold"))

# Widgets del Combate
frame_cabecera = tk.Frame(escena_combate, bg="#34495E", bd=2, relief="groove")
frame_log = tk.Frame(escena_combate, bg="#2C3E50")
frame_acciones = tk.Frame(escena_combate, bg="#2C3E50")

lbl_hp_jugador = tk.Label(frame_cabecera, font=("Arial", 12, "bold"), bg="#34495E", fg="#2ECC71")
lbl_hp_enemigo = tk.Label(frame_cabecera, font=("Arial", 12, "bold"), bg="#34495E", fg="#E74C3C")

scrollbar = tk.Scrollbar(frame_log)
log_combate = tk.Text(frame_log, height=12, width=65, font=("Consolas", 10), bg="#1A252C", fg="white", yscrollcommand=scrollbar.set)

btn_atacar = tk.Button(frame_acciones, text="Atacar", command=lambda: accion_atacar(False), font=("Arial", 12, "bold"), bg="#E67E22", fg="white", width=15, height=2)
btn_habilidad = tk.Button(frame_acciones, text="Habilidad", command=lambda: accion_atacar(True), font=("Arial", 12, "bold"), bg="#9B59B6", fg="white", width=15, height=2)
btn_salir_combate = tk.Button(escena_combate, text="Finalizar Combate y Volver", command=lambda: cambiar_escena(escena_menu), font=("Arial", 12, "bold"), bg="#7F8C8D", fg="white", width=25, height=2)

# Construir las vistas e iniciar
construir_menu()
construir_crear()
construir_ver()
construir_seleccion()
construir_combate()

label_estado.pack(side="bottom", pady=20)
cambiar_escena(escena_menu)
ventana.mainloop()