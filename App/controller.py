"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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

from math import pi
import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initCatalog():
    return model.initCatalog()

# Funciones para la carga de datos
def loadData(catalog,event_file):
    event_file = cf.data_dir + event_file
    input_file = csv.DictReader(open(event_file,encoding="utf-8"),delimiter = ",")
    for event in input_file:
        model.addEvent(catalog, event)
    return catalog

# Funciones de ordenamiento

def requerimiento1(catalog,caracteristica1, min1, max1, caracteristica2, min2, max2):
    total_eventos, total_artistas, altura_arbol = model.requerimiento1(catalog,caracteristica1, min1, max1, caracteristica2, min2, max2)
    return total_eventos, total_artistas, altura_arbol



def requerimiento2(catalog, min_liv , max_liv, min_spe, max_spe):
    total_pistas, pistas = model.requerimiento2(catalog, min_liv , max_liv, min_spe, max_spe)
    return total_pistas, pistas

# Funciones de consulta sobre el catálogo

def requerimiento3(catalog, min_valence, max_valence,min_tempo,max_tempo):
    return model.requerimiento3(catalog, min_valence,max_valence,min_tempo,max_tempo)