from personaje import Personaje

class Parasito(Personaje):

    def __init__(self, nombre):

        descripcion = "Ignora el 50% de la defensa del rival, y roba la misma cantidad de vida que inflige."

        super().__init__(
            nombre=nombre,
            vida=85,
            ataque=14,
            defensa=4,
            probabilidad_critico=15,
            habilidad_nombre="Drenaje Sanguíneo",
            habilidad_descripcion=descripcion,
            recarga_maxima=3
        )

    def usar_habilidad(self, objetivo):
        """Habilidad Drenaje Sanguíneo: Ignora el 50% de la defensa del rival, y roba la misma cantidad de vida que inflige."""

        if self.puede_usar_habilidad():

            defensa_reducida = objetivo.defensa // 2
            danyo = max(1, self.ataque - defensa_reducida)

            objetivo.recibir_danyo(danyo)

            self.vida += danyo

            if self.vida > 120:
                self.vida = 120

            self.reiniciar_recarga()

            return (f"¡{self.nombre} usa {self.habilidad_nombre}!\n"
                    f"Roba {danyo} PV a {objetivo.nombre} y se cura esa misma cantidad.")
        
        else:
            return f"{self.habilidad_nombre} aún se está recargando (Faltan {self.recarga_actual} turnos)."