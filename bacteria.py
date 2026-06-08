from personaje import Personaje

class Bacteria(Personaje):

    def __init__(self, nombre):

        descripcion = "Ataca dos veces seguidas en el mismo turno con el 80% de su daño base."

        super().__init__(
            nombre=nombre,
            vida=100,
            ataque=16,
            defensa=5,
            probabilidad_critico=10,
            habilidad_nombre="Multiplicación",
            habilidad_descripcion=descripcion,
            recarga_maxima=3
        )

    def usar_habilidad(self, objetivo):
        """Habilidad Multiplicación: Ataca dos veces en el mismo turno pero usando un 80% de su daño base."""
        
        if self.puede_usar_habilidad():

            # Calcula el 80% del daño a aplicar asegurando que como mínimo sea 1
            danyo_golpe = max(1, int((self.ataque * 0.8) - objetivo.defensa))

            objetivo.recibir_danyo(danyo_golpe)
            objetivo.recibir_danyo(danyo_golpe)

            danyo_total = danyo_golpe * 2

            self.reiniciar_recarga()

            return (f"¡{self.nombre} usa {self.habilidad_nombre}!\n"
                    f"Golpea dos veces seguidas causando un total de {danyo_total} PV a {objetivo.nombre}.")
        
        else:
            return f"{self.habilidad_nombre} aún se está recargando (Faltan {self.recarga_actual} turnos)."