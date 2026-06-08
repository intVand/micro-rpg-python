from personaje import Personaje

class GlobuloBlanco(Personaje):

    def __init__(self, nombre):

        descripcion = "Se cura a sí mismo 30 puntos de vida (no hace daño al enemigo)."

        super().__init__(
            nombre=nombre,
            vida=130,
            ataque=12,
            defensa=8,
            probabilidad_critico=5,
            habilidad_nombre="Fagocitosis",
            habilidad_descripcion=descripcion,
            recarga_maxima=4
        )

    def usar_habilidad(self, objetivo):
        """Habilidad Fagocitosis: Se cura a si mismo 30 PV, pero no daña al enemigo durante ese turno."""

        if self.puede_usar_habilidad():
            curacion = 30
            self.vida += curacion

            # Limitador para que no se cure por encima de su vida máxima
            if self.vida > 130:
                self.vida = 130

            self.reiniciar_recarga()

            return (f"¡{self.nombre} usa {self.habilidad_nombre}!\n"
                    f"Se recupera 30 PV y ahora tiene {self.vida} PV.")
        
        else:
            return f"{self.habilidad_nombre} aún se está recargando (Faltan {self.recarga_actual} turnos)."