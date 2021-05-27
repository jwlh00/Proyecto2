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


#Variable granted de la seccion de login
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
    #Funcion para login
    success = False
    file = open("userInfo.txt", "r")
    for i in file:
        #Confirmar que lo que ingreso el usuario es igual a lo del archivo
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
        print("Usuario o contraseña incorrecta\n")
        begin()
        access(option)


def register(name, password):
    #Funcion para guardar el usuario y contraseña que el usuario ingreso
    file = open("userInfo.txt", "a")
    file.write("\n" + name + "," + password)


def access(option):
    #Funcion para verificar si el usuario eligio la opcion de Login o Registrar
    if (option == "L"):
        print("Login")
        print("-----")
        name = input("Ingrese su usuario: ")
        password = input("Ingrese su contraseña: ")
        login(name, password)
    elif (option == "R"):
        print("Registrar")
        print("---------")
        name = input("Ingrese su usuario: ")
        password = input("Ingrese su contraseña: ")
        register(name, password)


def begin():
    #Funcion de mostrar el menu de inicio
    global option
    option = input(
        "Ingrese una de las siguientes opciones \n(L) para log in: \n(R) para registrar:\n(S) para salir:\n ")
    if (option != "L" and option != "R" and option != "S"):
        begin()


def delete():
    #Funcion para eliminar peliculas del base de datos
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
    #Funcion para realizar encuestas al usuarios para crearles recomendaciones.
    pregunta1 = True
    
    #Variables de chequeo de respuestas
    genSuspenso = 0
    genTerror = 0
    genAnime = 0
    genComedia = 0
    genAccion = 0
    genRomance = 0
    while (pregunta1): #Pregunta 1
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
    while (pregunta2): #Pregunta 2
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
    while (pregunta3): #Pregunta 3
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
    
    #Si el genero preferido es suspenso
    if genSuspenso >= max(genAccion, genAnime, genRomance, genTerror, genComedia):
        session = graphdp.session()
        result = session.run("MATCH (Genero {name: 'Suspenso'})--(Pelicula)"
                             "RETURN Pelicula.Nombre")
        result2 = session.run("MATCH (Genero {name: 'Suspenso'})--(Pelicula)"
                              "RETURN Pelicula.Puntuacion")
        lista = result.value()
        lista2 = result2.value()
        print("Se le recomendaran algunas canciones basadas en el genero de su eleccion")
        variable = heapq.nlargest(5, zip(lista2, lista))
        for i in range(len(variable)):
            print(variable[i][1] + "| Calificacion: " + variable[i][0])
    
    #Si el genero preferido es accion
    elif genAccion >= max(genSuspenso, genAnime, genRomance, genTerror, genComedia):
        session = graphdp.session()
        result = session.run("MATCH (Genero {name: 'Accion'})--(Pelicula)"
                             "RETURN Pelicula.Nombre")
        result2 = session.run("MATCH (Genero {name: 'Accion'})--(Pelicula)"
                              "RETURN Pelicula.Puntuacion")
        lista = result.value()
        lista2 = result2.value()
        print("Se le recomendaran algunas canciones basadas en el genero de su eleccion")
        variable = heapq.nlargest(5, zip(lista2, lista))
        for i in range(len(variable)):
            print(variable[i][1] + "| Calificacion: " + variable[i][0])
    
    #Si el genero preferido es Romance
    elif genRomance >= max(genSuspenso, genAnime, genAccion, genTerror, genComedia):
        session = graphdp.session()
        result = session.run("MATCH (Genero {name: 'Romance'})--(Pelicula)"
                             "RETURN Pelicula.Nombre")
        result2 = session.run("MATCH (Genero {name: 'Romance'})--(Pelicula)"
                              "RETURN Pelicula.Puntuacion")
        lista = result.value()
        lista2 = result2.value()
        print("Se le recomendaran algunas canciones basadas en el genero de su eleccion")
        variable = heapq.nlargest(5, zip(lista2, lista))
        for i in range(len(variable)):
            print(variable[i][1] + "| Calificacion: " + variable[i][0])
    
    #Si el genero preferido es Anime
    elif genAnime >= max(genSuspenso, genRomance, genAccion, genTerror, genComedia):
        session = graphdp.session()
        result = session.run("MATCH (Genero {name: 'Anime'})--(Pelicula)"
                             "RETURN Pelicula.Nombre")
        result2 = session.run("MATCH (Genero {name: 'Anime'})--(Pelicula)"
                              "RETURN Pelicula.Puntuacion")
        lista = result.value()
        lista2 = result2.value()
        print("Se le recomendaran algunas canciones basadas en el genero de su eleccion")
        variable = heapq.nlargest(5, zip(lista2, lista))
        for i in range(len(variable)):
            print(variable[i][1] + "| Calificacion: " + variable[i][0])
    
    #Si el genero preferido es terror
    elif genTerror >= max(genSuspenso, genAnime, genAccion, genRomance, genComedia):
        session = graphdp.session()
        result = session.run("MATCH (Genero {name: 'Terror'})--(Pelicula)"
                             "RETURN Pelicula.Nombre")
        result2 = session.run("MATCH (Genero {name: 'Terror'})--(Pelicula)"
                              "RETURN Pelicula.Puntuacion")
        lista = result.value()
        lista2 = result2.value()
        print("Se le recomendaran algunas canciones basadas en el genero de su eleccion")
        variable = heapq.nlargest(5, zip(lista2, lista))
        for i in range(len(variable)):
            print(variable[i][1] + "| Calificacion: " + variable[i][0])
    
    #Si el genero preferido es comedia
    elif genComedia >= max(genSuspenso, genAnime, genAccion, genTerror, genRomance):
        session = graphdp.session()
        result = session.run("MATCH (Genero {name: 'Comedia'})--(Pelicula)"
                             "RETURN Pelicula.Nombre")
        result2 = session.run("MATCH (Genero {name: 'Comedia'})--(Pelicula)"
                              "RETURN Pelicula.Puntuacion")
        lista = result.value()
        lista2 = result2.value()
        print("Se le recomendaran algunas canciones basadas en el genero de su eleccion")
        variable = heapq.nlargest(5, zip(lista2, lista))
        for i in range(len(variable)):
            print(variable[i][1] + "| Calificacion: " + variable[i][0])


def rating():
    #Funcion para cambiar la puntuacion de las peliculas que el usuario quiera.
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


begin() #Llamar al menu principal
access(option)

while (option == "R"):
    begin()
    access(option)

if (granted): #Pasa cuando el usuario logra hacer log in
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
                    movieGenre = "Suspenso"

                    session.run(
                        "CREATE (p:Pelicula {Nombre:'" + movieName + "',Genero: '" + movieGenre + "',Puntuacion: '" + moiveRating + "'})")

                    session.run("MATCH (p:Pelicula {Nombre: '" + movieName + "'})" 
                                " MATCH (m:Genero {name: 'Suspenso'})"
                                " CALL apoc.create.relationship(p, 'Es del genero', {roles:['Suspenso']}, m)"
                                " YIELD rel"
                                " RETURN rel")
                    break

                elif (num_genero == 2):  # Terror
                    movieName = input("Ingrese el nombre de la pelicula de terror que desea agregar:\n")
                    moiveRating = input("Ingrese el rating de 0 a 10 que le daria usted a esa pelicula: ")
                    movieGenre = "Terror"

                    session.run(
                        "CREATE (p:Pelicula {Nombre:'" + movieName + "',Genero: '" + movieGenre + "',Puntuacion: '" + moiveRating + "'})")

                    session.run("MATCH (p:Pelicula {Nombre: '" + movieName + "'})" 
                                " MATCH (m:Genero {name: 'Terror'})"
                                " CALL apoc.create.relationship(p, 'Es del genero', {roles:['Terror']}, m)"
                                " YIELD rel"
                                " RETURN rel")
                    break

                elif (num_genero == 3):  # Anime
                    movieName = input("Ingrese el nombre de la pelicula anime que desea agregar:\n")
                    moiveRating = input("Ingrese el rating de 0 a 10 que le daria usted a esa pelicula: ")
                    movieGenre = "Anime"

                    session.run(
                        "CREATE (p:Pelicula {Nombre:'" + movieName + "',Genero: '" + movieGenre + "',Puntuacion: '" + moiveRating + "'})")

                    session.run("MATCH (p:Pelicula {Nombre: '" + movieName + "'})" 
                                " MATCH (m:Genero {name: 'Anime'})"
                                " CALL apoc.create.relationship(p, 'Es del genero', {roles:['Anime']}, m)"
                                " YIELD rel"
                                " RETURN rel")
                    break

                elif (num_genero == 4):  # Comedia
                    movieName = input("Ingrese el nombre de la pelicula de comedia que desea agregar:\n")
                    moiveRating = input("Ingrese el rating de 0 a 10 que le daria usted a esa pelicula: ")
                    movieGenre = "Comedia"

                    session.run(
                        "CREATE (p:Pelicula {Nombre:'" + movieName + "',Genero: '" + movieGenre + "',Puntuacion: '" + moiveRating + "'})")

                    session.run("MATCH (p:Pelicula {Nombre: '" + movieName + "'})" 
                                " MATCH (m:Genero {name: 'Comedia'})"
                                " CALL apoc.create.relationship(p, 'Es del genero', {roles:['Comedia']}, m)"
                                " YIELD rel"
                                " RETURN rel")
                    break

                elif (num_genero == 5):  # Accion
                    movieName = input("Ingrese el nombre de la pelicula de accion que desea agregar:\n")
                    moiveRating = input("Ingrese el rating de 0 a 10 que le daria usted a esa pelicula: ")
                    movieGenre = "Accion"

                    session.run(
                        "CREATE (p:Pelicula {Nombre:'" + movieName + "',Genero: '" + movieGenre + "',Puntuacion: '" + moiveRating + "'})")

                    session.run("MATCH (p:Pelicula {Nombre: '" + movieName + "'})" 
                                " MATCH (m:Genero {name: 'Accion'})"
                                " CALL apoc.create.relationship(p, 'Es del genero', {roles:['Accion']}, m)"
                                " YIELD rel"
                                " RETURN rel")
                    break

                elif (num_genero == 6):  # Romance
                    movieName = input("Ingrese el nombre de la pelicula de romance que desea agregar:\n")
                    moiveRating = input("Ingrese el rating de 0 a 10 que le daria usted a esa pelicula: ")
                    movieGenre = "Romance"

                    session.run(
                        "CREATE (p:Pelicula {Nombre:'" + movieName + "',Genero: '" + movieGenre + "',Puntuacion: '" + moiveRating + "'})")

                    session.run("MATCH (p:Pelicula {Nombre: '" + movieName + "'})" 
                                " MATCH (m:Genero {name: 'Romance'})"
                                " CALL apoc.create.relationship(p, 'Es del genero', {roles:['Romance']}, m)"
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
