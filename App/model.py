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
        "energy": None
    }
    categories = ['instrumentalness', 'liveness','speechiness', 'danceability', 'valence','loudness', 'acousticness','energy']
    for category in categories:
        catalog[category] = om.newMap(omaptype='RBT',comparefunction = compare )
    catalog['events'] = lt.newList('ARRAY_LIST', compareIds)
    catalog['artists'] = mp.newMap(10000,maptype='PROBING',loadfactor=0.5, comparefunction = compareMap)
    catalog['tracks'] = mp.newMap(10000,maptype='PROBING',loadfactor=0.5, comparefunction = compareMap)

    return catalog
# Funciones para agregar informacion al catalogo
def addEvent(catalog, event):
    categories = ['instrumentalness', 'liveness','speechiness', 'danceability', 'valence','loudness', 'acousticness','energy']
    lt.addLast(catalog['events'], event)
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
    for c in categories:
        if c != category:
            event[c] = om.newMap('RBT',compare)
    return event

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
