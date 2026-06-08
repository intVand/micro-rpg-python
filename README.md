# 🧬 Micro-RPG Celular

Un juego de combate por turnos en dos dimensiones desarrollado en **Python** utilizando **Tkinter** para la interfaz gráfica y **JSON** para la persistencia de datos. El proyecto simula batallas microscópicas entre diferentes clases de microorganismos (Virus, Bacterias, Glóbulos Blancos, Hongos y Parásitos), aplicando conceptos de Programación Orientada a Objetos (POO).

---

## 🎯 Características Principales

* **Arquitectura POO Sólida:** Uso extensivo de herencia y encapsulamiento mediante una superclase `Personaje`. Implementación de **Polimorfismo** para que cada tipo de microorganismo ejecute una habilidad única y asimétrica.
* **Interfaz Gráfica Unificada (GUI):** Diseñado con Tkinter bajo un enfoque de *Single-Page Application*. Toda la navegación (creación, base de datos, selección y combate) ocurre de forma dinámica en una sola ventana sin molestas pestañas emergentes.
* **Feedback Visual e IA:** Batallas animadas de forma asíncrona (animaciones de salto al atacar y parpadeo de daño). La Inteligencia Enemiga cuenta con tiempos de respuesta aleatorios para simular un comportamiento orgánico y humano.
* **Ampliaciones Mecánicas (Bloque B):**
    * **Efectos de estado:** Mecánicas de daño acumulativo por *Veneno* y pérdida de acción por *Parálisis*.
    * **Estadísticas Avanzadas:** Registro permanente y persistente de victorias, derrotas y métricas de combate para cada personaje individual.
    * **Ranking Dinámico:** Algoritmo que calcula el *Win Rate* real (eficiencia) de los luchadores para generar un Top 3 interactivo con condecoraciones visuales.
* **Persistencia Local:** Serialización nativa a formato JSON para guardar y cargar partidas, incluyendo un filtro inteligente anti-duplicados en memoria.

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.14.0
* **Interfaz Gráfica:** Tkinter (Biblioteca nativa)
* **Formatos de Datos:** JSON (Persistencia local)
* **Lógicas del Motor:** Módulos nativos `os`, `random`, `math`

---

## 📁 Estructura del Proyecto

```text
├── assets/                 # Recursos gráficos (Sprites PNG e Icono .ico)
├── personaje.py            # Superclase base y lógica de propiedades encapsuladas
├── virus.py / hongo.py...  # Subclases polimórficas (Microorganismos)
├── combate.py              # Motor lógico del flujo de turnos e Inteligencia Artificial
├── persistencia.py         # Módulo de lectura/escritura y factoría de objetos JSON
├── gui.py                  # Interfaz gráfica principal y gestor de escenas (Punto de entrada)
└── personajes.json         # Base de datos local de partidas y personajes guardados
```

---

## 🚀 Cómo Ejecutar el Proyecto

Este proyecto ha sido desarrollado utilizando exclusivamente la biblioteca estándar de Python, por lo que **no requiere la instalación de librerías de terceros** a través de `pip`.

1. Clona este repositorio en tu máquina local:
    ```bash
    git clone https://github.com/intVand/micro-rpg-python.git
    ```

2. Accede al directorio del proyecto:
    ```bash
    cd micro-rpg-python
    ```

3. Ejecuta el archivo principal desde la terminal para asegurar una correcta compatibilidad de hilos en la GUI:
    ```bash
    python gui.py
    ```

💡 **Nota de arquitectura:** Todo el flujo visual y los controladores de eventos residen centralizados en `gui.py` para mitigar las limitaciones nativas de Tkinter respecto a las dependencias cruzadas, evitando de forma intencionada fallos de importación circular (Circular Imports).