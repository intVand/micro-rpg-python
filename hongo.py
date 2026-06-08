from personaje import Personaje

class Hongo(Personaje):

    def __init__(self, nombre):
       
       descripcion = "Hace daño moderado y aplica 'Paralizado' (el enemigo pierde su proximo turno)."

       super().__init__(
           nombre=nombre,
           vida=90,
           ataque=18,
           defensa=4,
           probabilidad_critico=10,
           habilidad_nombre="Nube de Esporas",
           habilidad_descripcion=descripcion,
           recarga_maxima=4
       )

    def usar_habilidad(self, objetivo):
        """Habilidad Nube de Esporas: Realiza un ataque moderado, además de paralizar al objetivo (pierde un turno)."""

        if self.puede_usar_habilidad():

            danyo = max(1, self.ataque - objetivo.defensa)

            objetivo.recibir_danyo(danyo)

            objetivo.estado = "paralizado"

            self.reiniciar_recarga()

            return (f"¡{self.nombre} usa {self.habilidad_nombre}!\n"
                    f"Quita {danyo} PV y deja a {objetivo.nombre} 'Paralizado'.")
        
        else:
            return f"{self.habilidad_nombre} aún se está recargando (Faltan {self.recarga_actual} turnos)."