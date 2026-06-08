import json
import os

from bacteria import Bacteria
from globulo_blanco import GlobuloBlanco
from hongo import Hongo
from parasito import Parasito
from virus import Virus

ARCHIVO_JSON = "personajes.json"

def guardar_personajes(lista_personajes):
    """Convierte la lista de objetos a diccionarios y los guarda en JSON."""

    lista_dict = []

    for personaje in lista_personajes:
        lista_dict.append(personaje.to_dict())

    with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
        json.dump(lista_dict, archivo, indent=4, ensure_ascii=False)

    return "Personajes guardados correctamente"

def cargar_personajes():
    """Lee el JSON, extrae los diccionarios y reconstruye los objetos."""

    # Si no existe el JSON, devuelve una lista vacía
    if not os.path.exists(ARCHIVO_JSON):
        return []
    
    lista_objetos = []

    with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
        lista_dict = json.load(archivo)

    for diccionario in lista_dict:
        tipo = diccionario.get("tipo")
        nombre = diccionario.get("nombre")
        victorias = diccionario.get("victorias", 0)
        derrotas = diccionario.get("derrotas", 0)

        personaje = None

        if tipo == "Virus":
            personaje = Virus(nombre)

        elif tipo == "GlobuloBlanco":
            personaje = GlobuloBlanco(nombre)

        elif tipo == "Bacteria":
            personaje = Bacteria(nombre)

        elif tipo == "Hongo":
            personaje = Hongo(nombre)

        elif tipo == "Parasito":
            personaje = Parasito(nombre)

        if personaje is not None:
            personaje.victorias = victorias
            personaje.derrotas = derrotas
            
            lista_objetos.append(personaje)

    return lista_objetos