from personaje import Personaje

class Virus(Personaje):

    def __init__(self, nombre):

        descripcion = "Ataca al objetivo y le aplica el estado 'Veneno' (Se acumula daño por veneno en cada uso de habilidad)."

        super().__init__(
            nombre=nombre,
            vida=70,
            ataque=25,
            defensa=2,
            probabilidad_critico=20,
            habilidad_nombre="Carga Viral",
            habilidad_descripcion=descripcion,
            recarga_maxima=3
        )

    def usar_habilidad(self, objetivo):
        """Habilidad Carga Viral: Ataca y envenena (el veneno se acumula cada vez que se usa la habilidad)."""

        if self.puede_usar_habilidad():

            danyo_habilidad = max(1, self.ataque - objetivo.defensa)

            objetivo.recibir_danyo(danyo_habilidad)

            objetivo.estado = "veneno"
            objetivo.danyo_veneno_acumulado += 5

            self.reiniciar_recarga()

            return (f"¡{self.nombre} usa {self.habilidad_nombre}!\n"
                    f"Ignora la defensa de {objetivo.nombre}, le quita {danyo_habilidad} PV"
                    f" y le aplica estado 'Veneno'.")
        
        else:
            return f"{self.habilidad_nombre} aún se está recargando (Faltan {self.recarga_actual} turnos)."