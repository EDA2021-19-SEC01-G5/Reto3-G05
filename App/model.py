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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import sys
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
import random

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def initCatalog():
    catalog = {
        'instrumentalness': None,
        'liveness': None,
        'speechiness': None,
        'danceability': None,
        'valence': None,
        'artists': None,
        'tracks':None,
        'events': None,
        "loudness":None,
        "acousticness":None,
        "energy": None,
        'tempo': None
    }
    categories = ['instrumentalness', 'liveness','speechiness', 'danceability', 'valence','loudness', 'acousticness','energy']
    for category in categories:
        catalog[category] = om.newMap(omaptype='RBT',comparefunction = compare )
    catalog['artists'] = mp.newMap(maptype='PROBING',loadfactor=0.5)
    catalog['tracks'] = mp.newMap(maptype='PROBING',loadfactor=0.5)
    catalog['events'] = lt.newList('ARRAY_LIST', compareIds)
    catalog['tempo'] = om.newMap(omaptype='RBT', comparefunction = compare )

    return catalog
# Funciones para agregar informacion al catalogo
def addEvent(catalog, event):
    categories = ['instrumentalness', 'liveness','speechiness', 'danceability', 'valence','loudness', 'acousticness','energy']
    lt.addLast(catalog['events'], event)
    addToTempoMap(catalog,event)
    for category in categories:
        addToRBT(catalog, event,category)
    addArtists(catalog, event)
    addTrack(catalog, event)


    
def addTrack(catalog, event):
    track = mp.get(catalog['tracks'], event['track_id'])
    if (track is None):
        track_entry = lt.newList('ARRAY_LIST')  
        mp.put(catalog['tracks'],event['track_id'],track_entry)
    else:
        track_entry = me.getValue(track)
    lt.addLast(track_entry,event)


def addArtists(catalog, event):
    artist = mp.get(catalog['artists'], event['artist_id'])
    if (artist is None):
        artist_entry = lt.newList('ARRAY_LIST')  
        mp.put(catalog['artists'],event['artist_id'],artist_entry)
    else:
        artist_entry = me.getValue(artist)
    lt.addLast(artist_entry,event)



# Funciones para creacion de datos
def addToRBT(catalog, event, category):
    map = catalog[category]
    #se esta volviendo float
    key = float(event[category])
    value = om.get(map,key)
    if (value is None):
        entry = newEvent(category)
        om.put(map,key,entry)
    else:
        entry = me.getValue(value)
    lt.addLast(entry['list'],event)
    addToTempoList(entry,event)
    categories = ['instrumentalness', 'liveness','speechiness', 'danceability', 'valence','loudness', 'acousticness','energy']
    for c in categories:
        if c != category:
            valor_c = om.get(entry[c],float(event[c]))
            if valor_c is None:
                entry_c = lt.newList('ARRAY_LIST')
                om.put(entry[c],float(event[c]),entry_c)
            else:
                entry_c = me.getValue(valor_c)
            lt.addLast(entry_c,event)



def newEvent(category):
    event = {
        'list': None
    }
    event['list'] = lt.newList('ARRAY_LIST',compareIds )
    categories = ['instrumentalness', 'liveness','speechiness', 'danceability', 'valence','loudness', 'acousticness','energy']
    event["tempo"] = om.newMap('RBT',compare)
    for c in categories:
        if c != category:
            event[c] = om.newMap('RBT',compare)
    return event


def addToTempoList(entry,event):
    in_tempo = om.get(entry["tempo"],float(event["tempo"]))
    if (in_tempo is None):
        entry_tempo = lt.newList('ARRAY_LIST')
        om.put(entry["tempo"],float(event["tempo"]),entry_tempo)
    else:
        entry_tempo = me.getValue(in_tempo)
    lt.addLast(entry_tempo,event)

def addToTempoMap(catalog,event):
    map = catalog['tempo']
    entry = om.get(map,float(event['tempo']))
    if (entry is None):
        value = lt.newList('ARRAY_LIST')
        om.put(map, float(event['tempo']), value)
    else:
        value = me.getValue(entry)
    lt.addLast(value,event)
# Funciones de consulta


#requerimiento 1

def requerimiento1(catalog,caracteristica1, min1, max1, caracteristica2, min2, max2):
    eventos_totales = lt.newList('ARRAY_LIST')
    events_car1 = om.keys(catalog[caracteristica1],min1, max1)
    cant_events1 = lt.size(events_car1)
    for i in range(1, cant_events1+1):
        key = lt.getElement(events_car1,i)
        entry = om.get(catalog[caracteristica1],key)
        elemento = me.getValue(entry)
        events_car2 = om.keys(elemento[caracteristica2],min2,max2)
        cant_car2 = lt.size(events_car2)
        for j in range(1, cant_car2+1):
            key2 = lt.getElement(events_car2, j)
            entry2 = om.get(elemento[caracteristica2],key2)
            elemento2 = me.getValue(entry2)
            len_lista = lt.size(elemento2)
            for e in range(1,len_lista+1):
                evento = lt.getElement(elemento2,e)
                lt.addLast(eventos_totales,evento)
    total_eventos = lt.size(eventos_totales)
    total_artistas = num_artistas(eventos_totales)
    altura_arbol = om.height(catalog[caracteristica1])
    return total_eventos, total_artistas, altura_arbol

def num_artistas(lista):
    artistas = mp.newMap(10000,maptype='PROBING',loadfactor=0.5)
    longitud = lt.size(lista)
    for i in range(1,longitud+1):
        evento = lt.getElement(lista, i)
        mp.put(artistas, evento['artist_id'],evento)
    return mp.size(artistas)



# requerimiento 2

    
def dar_pistas(lista):
    map_pistas = om.newMap(omaptype='RBT',comparefunction = compare )
    longitud = lt.size(lista)
    for i in range(1,longitud+1):
        evento = lt.getElement(lista, i)
        om.put(map_pistas, evento["track_id"],evento)
    return map_pistas


def requerimiento2(catalog, min_liv , max_liv, min_spe, max_spe):
    eventos_totales = lt.newList('ARRAY_LIST')
    eventos_liv = om.keys(catalog['liveness'],min_liv, max_liv)
    cantidad_eventos_liv = lt.size(eventos_liv)
    for i in range(1, cantidad_eventos_liv+1):
        key = lt.getElement(eventos_liv, i)
        entry = om.get(catalog['liveness'],key)
        eventos_spe = me.getValue(entry)
        events_car2 = om.keys(eventos_spe['speechiness'],min_spe,max_spe)
        cant_car2 = lt.size(events_car2)
        for j in range(1, cant_car2+1):
            key2 = lt.getElement(events_car2, j)
            entry2 = om.get(eventos_spe['speechiness'], key2)
            lista_eventos = me.getValue(entry2)
            cantidad_eventos = lt.size(lista_eventos)
            for e in range(1, cantidad_eventos+1):
                evento = lt.getElement(lista_eventos, e)
                lt.addLast(eventos_totales, evento)           
    arbol_pistas = dar_pistas(eventos_totales)
    total_pistas = om.size(arbol_pistas)
    posiciones = random.sample(range(total_pistas), 8)
    pistas = lt.newList('ARRAY_LIST')
    for i in posiciones:
        key_pista = om.select(arbol_pistas, i)
        entry3 = om.get(arbol_pistas, key_pista)
        pista = me.getValue(entry3)
        lt.addLast(pistas, pista)
    return total_pistas, pistas

# Requerimiento 3

def requerimiento3(catalog, min_valence, max_valence,min_tempo,max_tempo):
    final_list = lt.newList("ARRAY_LIST")
    map = catalog["valence"]
    list = om.values(map,min_valence,max_valence)
    size = lt.size(list)
    for i in range(1, size + 1):
        sub_element = lt.getElement(list,i)
        sub_map = sub_element['tempo'] 
        sub_list = om.values(sub_map,min_tempo,max_tempo)
        size_j = lt.size(sub_list)
        for j in range(1, size_j +1):
            element = lt.getElement(sub_list,j)
            size_k = lt.size(element)
            for k in range(1, size_k + 1):
                final_element = lt.getElement(element,k)
                lt.addLast(final_list, final_element)
    arbol_pistas = dar_pistas(final_list)
    total_pistas = om.size(arbol_pistas)
    posiciones = random.sample(range(total_pistas), 8)
    pistas = lt.newList('ARRAY_LIST')
    for i in posiciones:
        key_pista = om.select(arbol_pistas, i)
        entry3 = om.get(arbol_pistas, key_pista)
        pista = me.getValue(entry3)
        lt.addLast(pistas, pista)
    
    return pistas, total_pistas 

# Requerimiento 4

def tablaGeneros():
    tabla = {
        'reggeae': [60,90],
        'down-tempo': [70,100],
        'chill-out': [90,120],
        'hip-hop':[85,115],
        'jazz-funk':[120,125],
        'pop': [100,130],
        'ryb': [60,80],
        'rock': [110,140],
        'metal':[100,160]
    }
    return tabla


def requerimiento4(catalog: dict,lista_generos: str, nuevoGenero: bool,nuevo: str, min: float,max: float):
    #Preparar la nueva información
    data = {}
    map = catalog['tempo']
    tabla = tablaGeneros()
    nuevo = nuevo.strip().lower()
    generos = lista_generos.split(",")
    mapa_pistas = om.newMap('RBT',comparefunction= compare) 
    if nuevoGenero:
        tabla[nuevo] = [min,max]
        generos.append(nuevo)
    # Consolidar la lista con los eventos para cada uno de los generos
    for genero in generos:
        genero = genero.strip().lower()
        data[genero] = lt.newList('ARRAY_LIST')
        listas = om.values(map,tabla[genero][0],tabla[genero][1])
        num_listas = lt.size(listas)
        for i in range(1, num_listas + 1):
            lista = lt.getElement(listas,i)
            num_elementos = lt.size(lista)
            for j in range(1, num_elementos + 1 ):
                elemento = lt.getElement(lista, j)
                lt.addLast(data[genero],elemento)
                om.put(mapa_pistas,elemento['id'],elemento)
        data[genero] = (data[genero], lt.size(data[genero]),num_artistas(data[genero])) 
    data['numero_pistas_individual'] = om.size(mapa_pistas)
    
    return data, tabla

# Funciones utilizadas para comparar elementos dentro de una lista
def compare(i1, i2):
    if i1 == i2:
        return 0
    if i1 < i2:
        return -1
    else:
        return 1

def compareIds(event1, event2):
    i1 = int(event1['id'])
    i2 = int(event2['id'])
    if i1 == i2:
        return 0
    if i1 < i2:
        return -1
    else:
        return 1

def compareMap(id, entry):
    cat_entry = me.getKey(entry)
    if (id.lower().strip() == cat_entry.strip().lower()):
        return 0



# Funciones de ordenamiento
