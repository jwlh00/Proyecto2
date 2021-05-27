import pandas as pd
import numpy as np
import heapq
from py2neo import Graph
from neo4j import GraphDatabase

# Variables que guardan las preferencias del usuario segun la encuesta inicial.
global genSuspenso
global genTerror
global genAnime
global genComedia
global genAccion
global genRomance

graphdp = GraphDatabase.driver(uri="bolt://184.72.122.172:7687", auth=("algoritmos123", "algoritmos123"))

##iniciando la sesion de neo4j##
global session
session = graphdp.session()

#session.run("MATCH (Genero {name:Anime})--(Pelicula)", "RETURN Pelicula.Nombre")


""""
iniciando la sesion de neo4j
session = graphdp.session()
nomusuario="PablishPrrueba12"
nomcancion="PruebaReplit "
duracion="5"
session.run("CREATE (p:Pelicula {Pelicula:'"+nomcancion+"',Duracion: '"+duracion+"'})")
"""

granted = False

def menu():
    '''funcion para el menu principal, con la defensa para que el usuario solo
    ingrese lo que le es pedido. Haciendo que el variable "num" sea global para que
    se pueda utilizar a travez de todo el codigo.'''
    global num
    print('\n-----Sistema de Recomendaciones-----\n1. Recomendar pelicula. \n2. Agregar pelicula. \n3. Eliminar Pelicula.\n4. Puntuar pelicula.\n5. Salir.')
    x = False
    while not x:

        try:
            num = input("\nIngrese el numero de la opcion deseada: ")
            num = int(num)
            x = True
        except Exception:
            print("\nEl valor ingresado, no es un número, por favor ingrese un número nuevamente")
    while num < 1 or num > 5:
        print('numero fuera de rango, por favor ingresar otra vez:')
        num = input('Ingrese el numero de lo que quiere hacer')

def menu_genero():
    '''funcion para el menu principal, con la defensa para que el usuario solo
    ingrese lo que le es pedido. Haciendo que el variable "num" sea global para que
    se pueda utilizar a travez de todo el codigo.'''
    global num_genero
    print("\n-----Generos disponibles-----\n")
    print('1. Suspenso\n2. Terror\n3. Anime\n4. Comedia\n5. Accion\n6. Romance\n7. Regresar al menu previo')
    x = False
    while not x:

        try:
            num_genero = input("\nIngrese el numero de la opcion deseada: ")
            num_genero = int(num_genero)
            x = True
        except Exception:
            print("\nEl valor ingresado, no es un número, por favor ingrese un número nuevamente")
    while num_genero < 1 or num_genero > 5:
        print('numero fuera de rango, por favor ingresar otra vez:')
        num_genero = input('Ingrese el numero de lo que quiere hacer')


def grant():
    global granted
    granted = True
