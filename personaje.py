import random

class Personaje:

    def __init__(self, nombre, vida, ataque, defensa, probabilidad_critico, habilidad_nombre, habilidad_descripcion, recarga_maxima):

        self.nombre = nombre
        self.ataque = ataque
        self.defensa = defensa
        self.probabilidad_critico = probabilidad_critico
        self.habilidad_nombre = habilidad_nombre
        self.habilidad_descripcion = habilidad_descripcion
        self.recarga_maxima = recarga_maxima
        self.estado = "normal" # Se utiliza para aplicar estados como envenenado, quemado, etc
        self.danyo_veneno_acumulado = 0 # Se utiliza para almacenar el daño acumulado por el efecto de envenenamiento

        self.vida_maxima = vida # Nos permite recordar la vida originaria
        self.vida = vida
        self.recarga_actual = 0 # Se inicializa en 0 lista para usarse

        # Registro del ratio de victorias
        self.victorias = 0
        self.derrotas = 0

    # Métodos getters y setters
    @property
    def vida(self):
        return self.__vida
    
    @vida.setter
    def vida(self, valor):
        # Aseguramos que la vida no baje de 0
        if valor < 0:
            self.__vida = 0

        else:
            self.__vida = int(valor)

    @property
    def recarga_actual(self):
        return self.__recarga_actual
    
    @recarga_actual.setter
    def recarga_actual(self, valor):
        # Aseguramos que la recarga_actual no baje de 0, ni supere a la recarga_maxima
        if valor < 0:
            self.__recarga_actual = 0
        
        elif valor > self.recarga_maxima:
            self.__recarga_actual = self.recarga_maxima

        else:
            self.__recarga_actual = int(valor)
    
    def esta_vivo(self):
        return self.vida > 0
    
    def recibir_danyo(self, cantidad):
        self.vida -= cantidad

    def reducir_recarga(self):
        if self.recarga_actual > 0:
            self.recarga_actual -= 1

    def puede_usar_habilidad(self):
        return self.recarga_actual == 0
    
    def reiniciar_recarga(self):
        self.recarga_actual = self.recarga_maxima

    def atacar(self, objetivo):
        """Realiza un ataque normal calculando posibilidades de fallos, críticos, variaciones, etc."""

        # Se calcula la probabilidad de fallar el ataque (5%)
        if random.randint(1, 100) <= 5:
            return f"¡{self.nombre} ha intentado atacar, pero falló el ataque!"

        # Se calcula el daño de base, que será el ataque del atacante menos la defensa del objetivo
        danyo_base = self.ataque - objetivo.defensa

        if danyo_base < 1:
            danyo_base = 1 # Como mínimo el daño será de 1 (nunca negativo)

        # Se aplica una variación del daño posible, de está forma cada ataque será diferente 
        variacion = random.uniform(0.9, 1.1)
        danyo_final = int(danyo_base * variacion)

        mensaje_critico = ""

        # Se calcula la probabilidad de un ataque crítico, dependiendo del tipo de atacante
        if random.randint(1, 100) <= self.probabilidad_critico:
            danyo_final = int(danyo_final * 1.5)
            mensaje_critico = "¡El ataque ha sido crítico!"

        # Se aplica el daño final
        objetivo.recibir_danyo(danyo_final)
        return f"{mensaje_critico}\n{self.nombre} ataca a {objetivo.nombre} y le quita {danyo_final} PV."
    
    def usar_habilidad(self, objetivo):
        """Este método se redefine mediante polimorfismo en cada subclase."""
        pass

    def curar_y_limpiar(self):
        """Restaura al personaje para el siguiente combate o para guardarlo."""

        self.vida = self.vida_maxima
        self.estado = "normal"
        self.danyo_veneno_acumulado = 0
        self.recarga_actual = 0

    # Persistencia
    def to_dict(self):
        """Convierte el objeto en un diccionario para guardarlo en JSON."""
        
        return {
            "tipo": self.__class__.__name__,
            "nombre": self.nombre,
            "victorias": self.victorias,
            "derrotas": self.derrotas
        }

    def __str__(self):

        total_partidas = self.victorias + self.derrotas

        if total_partidas > 0:
            win_rate = (self.victorias / total_partidas) * 100
        
        else:
            win_rate = 0.0

        return ("Información sobre el personaje:\n"
                f"\n[{self.__class__.__name__}] {self.nombre}"
                f"\nPV: {self.vida} | ATQ: {self.ataque} | DEF: {self.defensa}"
                f"\nHabilidad: {self.habilidad_nombre} | Tiempo de recarga: {self.recarga_maxima}"
                f"\nInformación sobre la habilidad: {self.habilidad_descripcion}"
                f"\nVictorias: {self.victorias} | Derrotas: {self.derrotas} | Win Rate: {win_rate:.1f}%")
                