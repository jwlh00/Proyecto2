##########################################################################
# Sistema de Recomendaciones
##########################################################################
# main.py
##########################################################################
# Integrantes:
# Pablo Gonzalez 20362
# Jun Woo Lee 20358
# Andres de la Roca 20332
##########################################################################
# Este programa se centra en un sistema de recomendaciones
# para peliculas dependiendo del genero y la decada a la que pertenece.
#
# La base de datos que utiliza este programa es basada en grafos y se
# creo con la ayuda de la plataforma para bases de datos Neo4j.
##########################################################################

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

# session.run("MATCH (Genero {name:Anime})--(Pelicula)", "RETURN Pelicula.Nombre")


granted = False


def menu():
    '''funcion para el menu principal, con la defensa para que el usuario solo
    ingrese lo que le es pedido. Haciendo que el variable "num" sea global para que
    se pueda utilizar a travez de todo el codigo.'''
    global num
    print(
        '\n-----Sistema de Recomendaciones-----\n1. Recomendar pelicula. \n2. Agregar pelicula. \n3. Eliminar Pelicula.\n4. Puntuar pelicula.\n5. Salir.')
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


def login(name, password):
    success = False
    file = open("userInfo.txt", "r")
    for i in file:
        a, b = i.split(",")
        b = b.strip()
        if (a == name and b == password):
            success = True
            break
    file.close()
    if (success):
        print("Logged in")
        grant()
    else:
        print("Usuario o contrasenia incorrecta\n")
        begin()
        access(option)


def register(name, password):
    file = open("userInfo.txt", "a")
    file.write("\n" + name + "," + password)


def access(option):
    if (option == "L"):
        print("Login")
        print("-----")
        name = input("Ingrese su usuario: ")
        password = input("Ingrese su contrasenia: ")
        login(name, password)
    elif (option == "R"):
        print("Registrar")
        print("---------")
        name = input("Ingrese su usuario: ")
        password = input("Ingrese su contrasenia: ")
        register(name, password)


def begin():
    global option
    option = input(
        "Ingrese una de las siguientes opciones \n(L) para log in: \n(R) para registrar:\n(S) para salir:\n ")
    if (option != "L" and option != "R" and option != "S"):
        begin()


def delete():
    deleteRun = True
    while (deleteRun):
        try:
            nombrePelicula = input("Ingrese el nombre de la pelicula: ")
            nombreEnBase = session.run("MATCH (n {Nombre:'" + nombrePelicula + "'})" "DETACH DELETE n")
            print("La pelicula ha sido borrada con exito.")
            deleteRun = False
        except:
            print("Ha ingresado un nombre invalido")


def encuesta():
    pregunta1 = True
    genSuspenso = 0
    genTerror = 0
    genAnime = 0
    genComedia = 0
    genAccion = 0
    genRomance = 0
    decada = "0.0"
    while (pregunta1):
        try:
            print("Para iniciar las recomendaciones le pedimos que conteste esta breve encuesta.")
            print(
                "\nPregunta No. 1\nDe las siguientes peliculas, ¿cual podrias considerar tu preferida?:\n1. A Quiet Place\n2. It\n3. Wolf Children\n4. Mean Girls\n5. Mad Max\n6. Call Me By Your Name")
            option1 = input()
            if option1 == "1":
                genSuspenso = genSuspenso + 1
                genTerror = genTerror + 1
                pregunta1 = False
                break
            elif option1 == "2":
                genTerror = genTerror + 1
                pregunta1 = False
                break
            elif option1 == "3":
                genAnime = genAnime + 1
                pregunta1 = False
                break
            elif option1 == "4":
                genComedia = genComedia + 1
                pregunta1 = False
                break
            elif option1 == "5":
                genAccion = genAccion + 1
                pregunta1 = False
                break
            elif option1 == "6":
                genRomance = genRomance + 1
                pregunta1 = False
                break
            else:
                print("La respuesta elegida no es valida, intentelo de nuevo")
        except:
            print("Ha elegido una opcion invalida, intentelo de nuevo")

    pregunta2 = True
    while (pregunta2):
        try:
            print(
                "\nPregunta No. 2\n¿Que genero de peliculas es tu favorito?:\n1. Suspenso\n2. Terror\n3. Anime\n4. Comedia\n5. Accion\n6. Romance")
            option2 = input()
            if option2 == "1":
                genSuspenso = genSuspenso + 1
                pregunta2 = False
                break
            elif option2 == "2":
                genTerror = genTerror + 1
                pregunta2 = False
                break
            elif option2 == "3":
                genAnime = genAnime + 1
                pregunta2 = False
                break
            elif option2 == "4":
                genComedia = genComedia + 1
                pregunta2 = False
                break
            elif option2 == "5":
                genAccion = genAccion + 1
                pregunta2 = False
                break
            elif option2 == "6":
                genRomance = genRomance + 1
                pregunta2 = False
                break
            else:
                print("La respuesta elegida no es valida, intentelo de nuevo")
        except:
            print("Ha elegido una opcion invalida, intentelo de nuevo")

    pregunta3 = True
    while (pregunta3):
        try:
            print(
                "\nPregunta No. 3\nDe las siguientes, cual pelicula elegirias para ver segun su trama o descripcion: \n1. Donde haya una trama seria con momentos de tension \n2. Que el escenario donde se desarrolle sea oscuro y con aspectos de miedo\n3. Que sean peliculas con personajes animados\n4. Donde la historia sea graciosa y que contenga muchas bromas y chistes\n5. Donde el protagonista sea un heroe y que la trama sea sobre sus aventuras\n6. Donde sea una historia de amor entre dos personajes")
            option3 = input()
            if option3 == "1":
                genSuspenso = genSuspenso + 1
                pregunta3 = False
                break
            elif option3 == "2":
                genTerror = genTerror + 1
                pregunta3 = False
                break
            elif option3 == "3":
                genAnime = genAnime + 1
                pregunta3 = False
                break
            elif option3 == "4":
                genComedia = genComedia + 1
                pregunta3 = False
                break
            elif option3 == "5":
                genAccion = genAccion + 1
                pregunta3 = False
                break
            elif option3 == "6":
                genRomance = genRomance + 1
                pregunta3 = False
                break
            else:
                print("La respuesta elegida no es valida, intentelo de nuevo")
        except:
            print("Ha elegido una opcion invalida, intentelo de nuevo")

    pregunta4 = True
    while (pregunta4):
        try:
            print(
                "\nPregunta No. 4\nDe que decada preferiria ver peliculas?: \n1. 1930\n2. 1940\n3. 1950\n4. 1960\n5. 1970\n6. 1980\n7. 1990\n8. 2000\n9. 2010\n10. 2020")
            option4 = input()
            if option4 == "1":
                decada = "1930"
                pregunta4 = False
                break
            elif option4 == "2":
                decada = "1940"
                pregunta4 = False
                break
            elif option4 == "3":
                decada = "1950"
                pregunta4 = False
                break
            elif option4 == "4":
                decada = "1960"
                pregunta4 = False
                break
            elif option4 == "5":
                decada = "1970"
                pregunta4 = False
                break
            elif option4 == "6":
                decada = "1980"
                pregunta4 = False
                break
            elif option4 == "7":
                decada = "1990"
                pregunta4= False
                break
            elif option4 == "8":
                decada = "2000"
                pregunta4 = False
                break
            elif option4 == "9":
                decada = "2010"
                pregunta4 = False
                break
            elif option4 == "10":
                decada = "2020"
                pregunta4 = False
                break

            else:
                print("La respuesta elegida no es valida, intentelo de nuevo")
        except:
            print("Ha elegido una opcion invalida, intentelo de nuevo")

    if genSuspenso >= max(genAccion, genAnime, genRomance, genTerror, genComedia):
        session = graphdp.session()
        result = session.run("MATCH (Genero {name: 'Suspenso'})--(Pelicula)--(Decada {name:'"+decada+"'})"
                             "RETURN Pelicula.Nombre")
        result2 = session.run("MATCH (Genero {name: 'Suspenso'})--(Pelicula)--(Decada {name:'"+decada+"'})"
                              "RETURN Pelicula.Puntuacion")
        lista = result.value()
        lista2 = result2.value()
        if not lista:
            print("No se encontraron peliculas con estos parametros.")
        else:
            print("Se le recomendaran algunas canciones basadas en el genero de su eleccion")
            variable = heapq.nlargest(5, zip(lista2, lista))
            for i in range(len(variable)):
                print(variable[i][1] + "| Calificacion: " + variable[i][0] + "| Decada: " + decada)

    elif genAccion >= max(genSuspenso, genAnime, genRomance, genTerror, genComedia):
        session = graphdp.session()
        result = session.run("MATCH (Genero {name: 'Accion'})--(Pelicula)--(Decada {name:'"+decada+"'})"
                             "RETURN Pelicula.Nombre")
        result2 = session.run("MATCH (Genero {name: 'Accion'})--(Pelicula)--(Decada {name:'"+decada+"'})"
                              "RETURN Pelicula.Puntuacion")
        lista = result.value()
        lista2 = result2.value()
        if not lista:
            print("No se encontraron peliculas con estos parametros.")
        else:
            print("Se le recomendaran algunas canciones basadas en el genero de su eleccion")
            variable = heapq.nlargest(5, zip(lista2, lista))
            for i in range(len(variable)):
                print(variable[i][1] + "| Calificacion: " + variable[i][0] + "| Decada: " + decada)


    elif genRomance >= max(genSuspenso, genAnime, genAccion, genTerror, genComedia):
        session = graphdp.session()
        result = session.run("MATCH (Genero {name: 'Romance'})--(Pelicula)--(Decada {name:'"+decada+"'})"
                             "RETURN Pelicula.Nombre")
        result2 = session.run("MATCH (Genero {name: 'Romance'})--(Pelicula)--(Decada {name:'"+decada+"'})"
                              "RETURN Pelicula.Puntuacion")
        lista = result.value()
        lista2 = result2.value()
        if not lista:
            print("No se encontraron peliculas con estos parametros.")
        else:
            print("Se le recomendaran algunas canciones basadas en el genero de su eleccion")
            variable = heapq.nlargest(5, zip(lista2, lista))
            for i in range(len(variable)):
                print(variable[i][1] + "| Calificacion: " + variable[i][0] + "| Decada: " + decada)

    elif genAnime >= max(genSuspenso, genRomance, genAccion, genTerror, genComedia):
        session = graphdp.session()
        result = session.run("MATCH (Genero {name: 'Anime'})--(Pelicula)--(Decada {name:'"+decada+"'})"
                             "RETURN Pelicula.Nombre")
        result2 = session.run("MATCH (Genero {name: 'Anime'})--(Pelicula)--(Decada {name:'"+decada+"'})"
                              "RETURN Pelicula.Puntuacion")
        lista = result.value()
        lista2 = result2.value()
        if not lista:
            print("No se encontraron peliculas con estos parametros.")
        else:
            print("Se le recomendaran algunas canciones basadas en el genero de su eleccion")
            variable = heapq.nlargest(5, zip(lista2, lista))
            for i in range(len(variable)):
                print(variable[i][1] + "| Calificacion: " + variable[i][0] + "| Decada: " + decada)

    elif genTerror >= max(genSuspenso, genAnime, genAccion, genRomance, genComedia):
        session = graphdp.session()
        result = session.run("MATCH (Genero {name: 'Terror'})--(Pelicula)--(Decada {name:'"+decada+"'})"
                             "RETURN Pelicula.Nombre")
        result2 = session.run("MATCH (Genero {name: 'Terror'})--(Pelicula)--(Decada {name:'"+decada+"'})"
                              "RETURN Pelicula.Puntuacion")
        lista = result.value()
        lista2 = result2.value()
        if not lista:
            print("No se encontraron peliculas con estos parametros.")
        else:
            print("Se le recomendaran algunas canciones basadas en el genero de su eleccion")
            variable = heapq.nlargest(5, zip(lista2, lista))
            for i in range(len(variable)):
                print(variable[i][1] + "| Calificacion: " + variable[i][0] + "| Decada: " + decada)

    elif genComedia >= max(genSuspenso, genAnime, genAccion, genTerror, genRomance):
        session = graphdp.session()
        result = session.run("MATCH (Genero {name: 'Comedia'})--(Pelicula)--(Decada {name:'"+decada+"'})"
                             "RETURN Pelicula.Nombre")
        result2 = session.run("MATCH (Genero {name: 'Comedia'})--(Pelicula)--(Decada {name:'"+decada+"'})"
                              "RETURN Pelicula.Puntuacion")
        lista = result.value()
        lista2 = result2.value()
        if not lista:
            print("No se encontraron peliculas con estos parametros.")
        else:
            print("Se le recomendaran algunas canciones basadas en el genero de su eleccion")
            variable = heapq.nlargest(5, zip(lista2, lista))
            for i in range(len(variable)):
                print(variable[i][1] + "| Calificacion: " + variable[i][0] + "| Decada: " + decada)


def rating():
    ratingBool = True

    while (ratingBool):
        try:
            userRatingMovie = input("De que pelicula quiere evaluar?\n")
            userRating = input("Que valor de 0 a 10 le daria a esta pelicula?\n")
            movieBase = session.run("MATCH (n {Nombre:'" + userRatingMovie + "'})--(Pelicula)"
                                                                              "RETURN n.Puntuacion")

            movieBaseList = movieBase.value()



            oldValue = (float)(movieBaseList[0])
            userRating = (float)(userRating)
            newValue = (userRating + oldValue) / 2
            newValue = (str)(newValue)



            session.run("MATCH (n {Nombre:'" + userRatingMovie + "'})" "SET n.Puntuacion = toString('"+ newValue+"')" "RETURN n.Nombre, n.Puntuacion")

            ratingBool = False

            print("Gracias por su retroalimentacion.\n")

        except:
            print("Ha ingresado un nombre invalido")


begin()
access(option)

while (option == "R"):
    begin()
    access(option)

if (granted):
    print("Bienvenido al programa")
    menu()
    while num != 5:
        if (num == 1):  # Encuesta
            encuesta()
            menu()
        elif (num == 2):  # Agregar pelicula
            menu_genero()
            while num_genero != 7:
                if (num_genero == 1):  # Suspenso
                    movieName = input("Ingrese el nombre de la pelicula de suspenso que desea agregar:\n")
                    moiveRating = input("Ingrese el rating de 0 a 10 que le daria usted a esa pelicula: ")
                    Decada = input("Ingrese la decada (1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020): ")
                    movieGenre = "Suspenso"

                    session.run(
                        "CREATE (p:Pelicula {Nombre:'" + movieName + "',Genero: '" + movieGenre + "',Puntuacion: '" + moiveRating + "',Decada:'" + Decada + "'})")

                    session.run("MATCH (p:Pelicula {Nombre: '" + movieName + "'})" 
                                " MATCH (m:Genero {name: '"+ movieGenre +"'})"
                                " CALL apoc.create.relationship(p, 'Es del genero', {roles:['Suspenso']}, m)"
                                " YIELD rel"
                                " RETURN rel")
                    session.run("MATCH (p:Pelicula {Nombre: '" + movieName + "'})" 
                                " MATCH (m:Decada {name: '"+ Decada +"'})"
                                " CALL apoc.create.relationship(p, 'Es de la epoca', {roles:['"+ Decada +"']}, m)"
                                " YIELD rel"
                                " RETURN rel")
                    break

                elif (num_genero == 2):  # Terror
                    movieName = input("Ingrese el nombre de la pelicula de terror que desea agregar:\n")
                    moiveRating = input("Ingrese el rating de 0 a 10 que le daria usted a esa pelicula: ")
                    movieGenre = "Terror"
                    Decada = input("Ingrese la decada (1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020): ")

                    session.run(
                        "CREATE (p:Pelicula {Nombre:'" + movieName + "',Genero: '" + movieGenre + "',Puntuacion: '" + moiveRating + "',Decada:'" + Decada + "'})")

                    session.run("MATCH (p:Pelicula {Nombre: '" + movieName + "'})" 
                                " MATCH (m:Genero {name: '"+ movieGenre +"'})"
                                " CALL apoc.create.relationship(p, 'Es del genero', {roles:['Suspenso']}, m)"
                                " YIELD rel"
                                " RETURN rel")
                    session.run("MATCH (p:Pelicula {Nombre: '" + movieName + "'})" 
                                " MATCH (m:Decada {name: '"+ Decada +"'})"
                                " CALL apoc.create.relationship(p, 'Es de la epoca', {roles:['"+ Decada +"']}, m)"
                                " YIELD rel"
                                " RETURN rel")
                    break

                elif (num_genero == 3):  # Anime
                    movieName = input("Ingrese el nombre de la pelicula anime que desea agregar:\n")
                    moiveRating = input("Ingrese el rating de 0 a 10 que le daria usted a esa pelicula: ")
                    movieGenre = "Anime"
                    Decada = input("Ingrese la decada (1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020): ")

                    session.run(
                        "CREATE (p:Pelicula {Nombre:'" + movieName + "',Genero: '" + movieGenre + "',Puntuacion: '" + moiveRating + "',Decada:'" + Decada + "'})")

                    session.run("MATCH (p:Pelicula {Nombre: '" + movieName + "'})" 
                                " MATCH (m:Genero {name: '"+ movieGenre +"'})"
                                " CALL apoc.create.relationship(p, 'Es del genero', {roles:['Suspenso']}, m)"
                                " YIELD rel"
                                " RETURN rel")
                    session.run("MATCH (p:Pelicula {Nombre: '" + movieName + "'})" 
                                " MATCH (m:Decada {name: '"+ Decada +"'})"
                                " CALL apoc.create.relationship(p, 'Es de la epoca', {roles:['"+ Decada +"']}, m)"
                                " YIELD rel"
                                " RETURN rel")
                    break

                elif (num_genero == 4):  # Comedia
                    movieName = input("Ingrese el nombre de la pelicula de comedia que desea agregar:\n")
                    moiveRating = input("Ingrese el rating de 0 a 10 que le daria usted a esa pelicula: ")
                    movieGenre = "Comedia"
                    Decada = input("Ingrese la decada (1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020): ")

                    session.run(
                        "CREATE (p:Pelicula {Nombre:'" + movieName + "',Genero: '" + movieGenre + "',Puntuacion: '" + moiveRating + "',Decada:'" + Decada + "'})")

                    session.run("MATCH (p:Pelicula {Nombre: '" + movieName + "'})" 
                                " MATCH (m:Genero {name: '"+ movieGenre +"'})"
                                " CALL apoc.create.relationship(p, 'Es del genero', {roles:['Suspenso']}, m)"
                                " YIELD rel"
                                " RETURN rel")
                    session.run("MATCH (p:Pelicula {Nombre: '" + movieName + "'})" 
                                " MATCH (m:Decada {name: '"+ Decada +"'})"
                                " CALL apoc.create.relationship(p, 'Es de la epoca', {roles:['"+ Decada +"']}, m)"
                                " YIELD rel"
                                " RETURN rel")
                    break

                elif (num_genero == 5):  # Accion
                    movieName = input("Ingrese el nombre de la pelicula de accion que desea agregar:\n")
                    moiveRating = input("Ingrese el rating de 0 a 10 que le daria usted a esa pelicula: ")
                    movieGenre = "Accion"
                    Decada = input("Ingrese la decada (1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020): ")

                    session.run(
                        "CREATE (p:Pelicula {Nombre:'" + movieName + "',Genero: '" + movieGenre + "',Puntuacion: '" + moiveRating + "',Decada:'" + Decada + "'})")

                    session.run("MATCH (p:Pelicula {Nombre: '" + movieName + "'})" 
                                " MATCH (m:Genero {name: '"+ movieGenre +"'})"
                                " CALL apoc.create.relationship(p, 'Es del genero', {roles:['Suspenso']}, m)"
                                " YIELD rel"
                                " RETURN rel")
                    session.run("MATCH (p:Pelicula {Nombre: '" + movieName + "'})" 
                                " MATCH (m:Decada {name: '"+ Decada +"'})"
                                " CALL apoc.create.relationship(p, 'Es de la epoca', {roles:['"+ Decada +"']}, m)"
                                " YIELD rel"
                                " RETURN rel")
                    break

                elif (num_genero == 6):  # Romance
                    movieName = input("Ingrese el nombre de la pelicula de romance que desea agregar:\n")
                    moiveRating = input("Ingrese el rating de 0 a 10 que le daria usted a esa pelicula: ")
                    movieGenre = "Romance"
                    Decada = input("Ingrese la decada (1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020): ")

                    session.run(
                        "CREATE (p:Pelicula {Nombre:'" + movieName + "',Genero: '" + movieGenre + "',Puntuacion: '" + moiveRating + "',Decada:'" + Decada + "'})")

                    session.run("MATCH (p:Pelicula {Nombre: '" + movieName + "'})" 
                                " MATCH (m:Genero {name: '"+ movieGenre +"'})"
                                " CALL apoc.create.relationship(p, 'Es del genero', {roles:['Suspenso']}, m)"
                                " YIELD rel"
                                " RETURN rel")
                    session.run("MATCH (p:Pelicula {Nombre: '" + movieName + "'})" 
                                " MATCH (m:Decada {name: '"+ Decada +"'})"
                                " CALL apoc.create.relationship(p, 'Es de la epoca', {roles:['"+ Decada +"']}, m)"
                                " YIELD rel"
                                " RETURN rel")
                    break

            menu()

        elif (num == 3):  # Eliminar
            delete()
            menu()
        elif (num == 4):  # Puntuacion
            rating()
            menu()
    print("Gracias por utilizar el programa, vuelva pronto")

if (option == "S"):
    print("Gracias por utilizar nuestro programa")
