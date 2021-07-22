"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


event_file = 'context_content_features-small.csv'

# ___________________________________________________
#  Menu principal
# ___________________________________________________

def printMenu():
    print("Bienvenido")
    print("1- Inicializar el catálogo") 
    print("2- Cargar información en el catálogo")
    print("3- Consultar el número de reproducciones en la intersección de dos caracteristicas de contenido en un rango")
    print("4- Encontrar música para festejar")
    print("5- Encontrar música para estudiar")
    print("6- Estudiar los géneros musicales") 

def initCatalog():
    return controller.initCatalog()

def loadData(catalog,event_file):
    controller.loadData(catalog, event_file)
    numero_eventos = lt.size(catalog['events'])
    numero_artistas = mp.size(catalog['artists'])
    numero_pistas = mp.size(catalog['tracks'])
    elementos_iniciales = []
    elementos_finales = []
    for i in range(5):
        inicial = lt.getElement(catalog['events'],i+1)
        final = lt.getElement(catalog['events'],numero_eventos-i)
        elementos_iniciales.append(inicial)
        elementos_finales.append(final)
    print('\n Total de eventos guardados: ', numero_eventos)
    print('\n Total de artistas unicos cargados: ', numero_artistas)
    print('\n Total de pistas de audio unicas guardadas: ', numero_pistas)
    print('\n 5 primeros elementos cargados: ')
    for i in range(5):
        print(elementos_iniciales[i])
    print('\n 5 elementos finales cargados: ')
    for i in range(5):
        print(elementos_finales[i])


#Requerimiento 1
def requerimiento1(catalog,caracteristica1, min1, max1, caracteristica2, min2, max2):
    total_eventos, total_artistas, altura_arbol = controller.requerimiento1(catalog,caracteristica1, min1, max1, caracteristica2, min2, max2)
    print('La cantidad de eventos entre el rango espeficicado es de :',total_eventos)
    print('La cantidad de artistas diferentes es de: ', total_artistas)
    print('La altura del arbol es de ', altura_arbol)




#requerimiento 2
def requerimiento2(catalog, min_liv , max_liv, min_spe, max_spe):
    total_pistas, pistas = controller.requerimiento2(catalog, min_liv , max_liv, min_spe, max_spe)
    print('El total de pistas en el rango especificado es de: ', total_pistas)
    print('Informacion de 8 pistas aleatorias: ')
    for i in range(1,lt.size(pistas)+1):
        print('pista ',i,': \n', lt.getElement(pistas, i), '\n')


#requerimiento 3
def requerimiento3(catalog, min_valence,max_valence, min_tempo,max_tempo):
    pistas, total_pistas = controller.requerimiento3(catalog, min_valence,max_valence, min_tempo,max_tempo)
    print('El total de pistas encontradas para los rangos especificados es de:', total_pistas)
    print(8*"*")
    print("Información de las 8 pistas aleatorias: ")
    print(8*"*")
    for i in range(1, lt.size(pistas) + 1):
        print(8*"*")
        print('Pista ', i,':\n', lt.getElement(pistas,i), '\n')


def requerimiento4(catalog,lista_generos,nuevoGenero,nuevo,min,max):
    data, tabla = controller.requerimiento4(catalog,lista_generos,nuevoGenero,nuevo,min,max)
    print(8*"*") 
    print(8*"*") 
    print("Se encontraron un total de:", data["numero_pistas_individual"], "total de eventos de reproducción")
    for genero in data.keys():
        if genero.lower().strip() in (lista_generos + nuevo):
            genero = genero.lower().strip()
            min = tabla[genero][0]
            max = tabla[genero][1]
            lista = data[genero][0]
            eventos = data[genero][1]
            artistas = data[genero][2]
            print(4*"*", genero.upper(),4*"*")
            print("Para el genero:", genero.title(),"el tempo se encuentra entre",min, "y",max)
            print("Reproducciones en el genero", genero.title(), ":", eventos, "eventos y", artistas, "artistas")
            print(4*"*", "Algunos artistas para", genero.title(), 4*"*")
            for i in range(1,11):
                elemento = lt.getElement(lista,i)
                print("Artista", i, elemento["artist_id"])


catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Inicializando el catalogo....")
        catalog = initCatalog()
        print("Catalogo inicializado\n")

    elif int(inputs[0]) == 2:
        print("Cargando información al catalogo")
        loadData(catalog, event_file)
        print("Información cargada")

    elif int(inputs[0]) == 3:
        caracteristica1 = input('Ingrese la primera categoria deseada: ')
        min1 = float(input('ingrese el valor minimo para esta caracteristica: '))
        max1 = float(input('ingrese el valor maximo para esta caracteristica: '))
        caracteristica2 = input('Ingrese la segunda categoria deseada: ')
        min2 = float(input('ingrese el valor minimo para esta caracteristica: '))
        max2 = float(input('ingrese el valor maximo para esta caracteristica: '))
        requerimiento1(catalog,caracteristica1, min1, max1, caracteristica2, min2, max2)
    elif int(inputs[0]) == 4:
        min_liv = float(input('Ingrese el valor minimo de liveness: '))
        max_liv = float(input('Ingrese el valor maximo de liveness: '))
        min_spe = float(input('Ingrese el valor minimo de speecheless: '))
        max_spe = float(input('Ingrese el valor mmaximo de speecheless: '))
        requerimiento2(catalog, min_liv , max_liv, min_spe, max_spe)
    elif (int(inputs[0])) == 5:
        min_valence = float(input('Ingrese el valor minimo de valence: '))
        max_valence= float(input('Ingrese el valor maximo de valence: '))
        min_tempo = float(input('Ingrese el valor minimo del tempo: '))
        max_tempo = float(input('Ingrese el valor maximo del tempo: '))
        requerimiento3(catalog, min_valence,max_valence, min_tempo,max_tempo)
    elif (int(inputs[0])) == 6:
        min, max, nuevoGenero, nuevo = 0, 0, False, ""
        lista_generos = input("Ingrese la lista de generos que desea consultar: \n")
        nuevoGenero = bool(int(input("¿Desea ingresar un nuevo género (0 para no, 1 para si)?: ")))
        if nuevoGenero:
            min = float(input("Ingrese el valor mínimo de BPM del nuevo genero: "))
            max = float(input("Ingrese el valor maximo de BPM del nuevo genero: "))
            nuevo = input("Ingrese el nombre del nuevo genero: ")
        requerimiento4(catalog,lista_generos, nuevoGenero,nuevo,min,max)
    else:
        sys.exit(0)
sys.exit(0)

