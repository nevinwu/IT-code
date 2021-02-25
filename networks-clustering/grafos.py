#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
grafos.py

Programa que realiza diferentes tareas con grafos.

Versión: 1.0
Autor: Francisco Martínez Picó
Fecha: 03/03/2020
"""
import networkx as nx
import matplotlib.pyplot as plt
import random

def draw_net(graph):
    """
    Utilizaremos esta función para crear y mostrar el gráfico con la red que
    representa nuestro grafo.

    ARGS:
        - graph: tipo grafo. Se trata de un objeto grafo del paquete networkx
        creado con la función 'nx.read_adjlist()'.
    """
    nx.draw_networkx(graph) # Dibujamos el grafo (red).

    plt.show() # Mostramos el gráfico de la red.

def show_matrix(matrix):
    """
    Función muy básica para mostrar la matriz por filas.

    ARGS:
        - matrix: tipo matriz (lista de listas). Se trata de la matriz que
        queremos mostrar por pantalla.
    """
    for row in matrix:
        print(row)

def get_adj(G):
    """
    Esta función se utiliza para obetener la matriz de adyacencias tal y como se
    pide en el ejercicio: distancia 1 entre los nodos conectados, infinito entre
    los no conectados (representando infinito como 200), y 0 para la relación de
    los nodos consigo mismos.

    ARGS:
        - G: tipo grafo (networkx). Objeto grafo creado con el paquete networkx.

    RETURNS:
        - final_matrix: tipo matriz (lista de listas). Básicamente, es una
        matriz de adyacencia para el grafo proporcionado.
    """
    A = nx.adjacency_matrix(G)

    A = A.toarray() # Para visualizar como array de adyacencias como 0 y 1.

    matrix = [] # Será la matriz de adyacencias.

    for row in A:
        fila = []

        for element in row:
            fila.append(element)

        matrix.append(fila)

    final_matrix = []

    for i in range(len(matrix)):
        new_row = []

        for j in range(len(matrix[i])):

            if i == j: # Nodo con sí mismo = 0.
                new_element = 0

            elif matrix[i][j] == 0: # Nodos sin relación directa = infinito.
                new_element = 200

            elif matrix[i][j] == 1: # Nodos con relación directa = 1.
                new_element = 1

            new_row.append(new_element)

        final_matrix.append(new_row)

    return final_matrix

def get_min_dist(G):
    """
    Esta función calcula la matriz de distancias mínimas para los nodos de un
    grafo. Se define como distancia mínima al número mínimo de nodos que habrá
    que recorrer para llegar de un nodo a otro. Esta matriz se calcula
    utilizando el algoritmo de Floyd-Warshall, que ya viene implementado en el
    paquete de networkx. Este algoritmo puede escribirse en pseucódigo de la
    siguiente manera:

    procedimiento FloydWarshall ()
    {
    Para k desde 0 hasta n-1
        Para i desde 0 hasta n-1
            Para j desde 0 hasta n-1
            T[i,j]= min(T[i,j], T[i,k] + T[k,j])
            Fin para j
        Fin para i
    Fin para k
    }

    ARGS:
        - G: tipo grafo (networkx). Objeto grafo creado con el paquete networkx.

    RETURNS:
        - min_dist: tipo matriz (lista de lista). Se trata de una matriz que
        contiene las distancias mínimas entre los nodos de un grafo.
    """
    B = nx.floyd_warshall(G) # Devuelve un diccionario de diccionarios.

    min_dist = []

    for key in nx.nodes(G):
        row = []

        for subkey in nx.nodes(G):
            row.append(B[key][subkey])

        min_dist.append(row)

    return min_dist

def get_diameter(G):
    """
    Se entiende como diametro de un grafo al camino más largo de los caminos más
    cortos entre los nodos. Esta función recibe, por tanto, un objeto grafo
    (networkx), halla su matriz de distancias mínimas y, finalmente, nos
    devuelve el diámetro.

    ARGS:
        - G: tipo grafo (networkx). Objeto grafo creado con el paquete networkx.

    RETURNS:
        - max_distance: tipo float. Número con coma flotante que representa el
        diámetro del grafo.
    """
    min_dist = get_min_dist(G)

    max_distance = 0

    for row in min_dist:

        if max(row) > max_distance:
            max_distance = max(row)

    return max_distance

def get_average_dist(G):
    """
    Esta función se encarga de calcular la distancia promedio. Para cada nodo de
    la matriz de distancias mínimas se calcula su distancia promedio al resto de
    los nodos. Finalmente, se hace un promedio de estos promedios.

    ARGS:
        - G: tipo grafo (networkx). Objeto grafo creado con el paquete networkx.

    RETURNS:
        - average_distance: tipo float. Número con coma flotante que representa
        la distancia promedio de los grafos.
    """
    min_dist = get_min_dist(G)

    rows_average = 0

    for row in min_dist:

        average = 0

        for element in row:
            average += element # Distancia de un nodo con sigo mismo es 0.

        average = average / (len(row) - 1) # No se hace de un nodo con él mismo.

        rows_average += average

    average_distance = rows_average / len(min_dist)

    return average_distance

def get_direct_interact(G):
    """
    Devuelve un listado de los nodos de un grafo ordenado de mayor a menor según
    el número de interacciones directas que tienen con otros nodos (es decir,
    según el número de arcos que tengan los nodos).

    ARGS:
        - G: tipo grafo (networkx). Objeto grafo creado con el paquete networkx.

    RETURNS:
        - direct_inter: tipo lista. Lista de nodos del grafo ordenada de mayor a
        menor según el número de arcos o relaciones que tengan.
    """
    adj = get_adj(G)

    lis = []

    for index in range(len(adj)):

        count = 0

        for element in adj[index]:

            if element == 1:
                count += 1

        lis.append(count)

    dic = {}

    for node in nx.nodes(G):
        dic[node] = lis[0]
        del lis[0]

    direct_inter = []

    for w in sorted(dic, key = dic.get, reverse = True):
        direct_inter.append(w)

    return direct_inter

def get_10min_average_dist(G):
    """
    Esta función nos devuelve los 10 nodos que tienen una menor distancia
    promedio al resto de nodos.

    ARGS:
        - G: tipo grafo (networkx). Objeto grafo creado con el paquete networkx.

    RETURNS:
        - sor_aver_dist[0:10]: tipo lista. Se trata de los 10 primeros elementos
        de la lista (de nodos) ordenada de menor a mayor según la distancia al
        resto de nodos.
    """
    min_dist = get_min_dist(G)

    average_dist = {}

    row = 0
    for node in nx.nodes(G):
        average_dist[node] = sum(min_dist[row]) / len(min_dist[row])
        row += 1

    sor_aver_dist = []

    for w in sorted(average_dist, key = average_dist.get):
        sor_aver_dist.append(w)

    return sor_aver_dist[0:10]

class Node:
    """
    Esta clase se utilizará para hacer referencia a cada uno de los nodos de
    nuestro grafo. Se utilizará para, dado una agrupación de nodos, facilitar el
    cálculo de la distancia promedio entre estos (ya que a cada nodo se le
    atribuye su fila de la matriz de distancias).
    """
    def __init__(self):
        """
        Cada instancia de la clase Node tendrá los atributos self.node (nodo que
        representa, caracteres alfanumérico), self.id (número entero asignado de
        manera ordenada a los nodos según su orden en las matrices de adyacencia
        y distancias, es decir, el nodo A, que es la primera fila de estas
        matrices (fila 0), tendrá un id 0), y self.distances (este atributo
        contendrá la fila correspondiente de la matriz de distancias mínimas).
        """
        self.node = str
        self.id = int
        self.distances = list

    def __str__(self):
        """
        Las instancias de la clase nodo se imprimirán como el nodo al que hacen
        referencia.
        """
        return self.node

def get_nodes(G):
    """
    Esta función se utiliza para obtener una lista de los nodos del grafo cuyos
    elementos son instancias de la clase Node. Por tanto, cada nodo tiene su id
    correspondiente y su fila de la matriz de distancias mínimas. Esta lista de
    nodos nos facilitará el clustering inicial.

    ARGS:
        - G: tipo grafo (networkx). Objeto grafo creado con el paquete networkx.

    RETURNS:
        - nodes: tipo lista. Lista con los nodos de un grafo
    """
    nodes = []

    min_dist = get_min_dist(G)

    count_id = 0

    for node in nx.nodes(G):
        new_node = Node()

        new_node.node = node

        new_node.id = count_id

        new_node.distances = min_dist[count_id]

        nodes.append(new_node)

        count_id += 1

    return nodes

def get_initial_clusters(G):
    """
    Esta función recibe un grafo y devuelve un diccionario con los 4 clusters
    iniciales. Los nodos en los clusters se colocan al azar: primero se coloca
    un nodo al azar en el cluster 1, seguidamente otro nodo al azar en el
    cluster 2, seguido del mismo proceso en el cluster 3 y 4. Después, este
    proceso se repite (volviendo a empezar por el cluster 1) hasta que la lista
    de nodos está vacía. Tres de estos clusters tienen 9 elementos, mientras que
    el último tiene 8 (esto para el caso de 'cubos.txt' que tiene 35 nodos)

    ARGS:
        - G: tipo grafo (networkx). Objeto grafo creado con el paquete networkx.

    RETURNS:
        - clusters: tipo diccionario. Cada clave es un cluster (c + número del
        cluster). Cada cluster tiene 9 u 8 nodos asignados al azar (para el caso
        de 'cubos.txt').
    """
    nodes = get_nodes(G)

    clusters = {'c1' : [],
                'c2' : [],
                'c3' : [],
                'c4' : []}

    while nodes:

        number = 1

        for n in range(0,4):
            dictionary_key = 'c' + str(number)

            # Claúsula try: no todos los cluster tendrán el mismo nº de nodos.
            try:
                choice = nodes.pop(random.randrange(len(nodes)))
                clusters[dictionary_key].append(choice)
                number += 1

            except:
                continue

    return clusters

def show_clusters(clusters):
    """
    Función simple que nos muestra los clusters y los nodos que contiene.

    ARGS:
        - clusters: tipo diccionario. Como clave está el nombre del cluster y,
        como valor, una lista con las instancias de la clase Node que lo forman.
    """
    for key in clusters:
        print('Cluster:', key)
        for node in clusters[key]:
            print(node)
        print('')

def get_cluster_score(cluster):
    """
    Esta función devuelve la distancia promedio entre los elementos de un
    cluster. Se define como un cluster mejor aquel cuya distancia promedio entre
    sus elementos (nodos del grafo) sea menor.

    ARGS:
        - cluster: tipo lista de objetos Node. Se trata de una lista de
        instancias de la clase Node (nodos de un grafo).

    RETURNS:
        - cluster_distance: tipo floating. Número decimal que representa la
        distancia promedio entre los elementos del cluster proporcionado.
    """

    """
    Primero miramos los nodos que hay en el cluster mediante su atributo 'id' y
    añadimos el total de nodos (sus id) que hay a una lista 'id_list'. Esta
    lista la utilizaremos para calcular la distancia promedio de un nodo con el
    resto.
    """
    id_list = []
    for e in cluster:
        id_list.append(e.id)

    cluster_distance = 0

    """
    Para cada elemento del cluster, calculamos su distancia promedio al resto y
    la sumamos a la variable 'distance'
    """
    for e in cluster:

        distance = 0

        for i in id_list:
            distance = distance + e.distances[i] # Distancia con uno mismo es 0,
                                                 # (no afecta a la media).

        distance = distance / (len(id_list) - 1) # No contamos el nodo mismo.

        """
        Esa distancia de cada nodo del cluster con el resto se suma a la
        variable 'cluster_distance', que se encarga de acumular el sumatorio de
        estas distancias para, una vez ya se han sumado la de todos los nodos
        del cluster, realizar el promedio.
        """
        cluster_distance = cluster_distance + distance

    # Finalmente, esta es la distancia promedio entre los elementos del cluster:
    cluster_distance = cluster_distance / len(cluster)

    return cluster_distance

def clusters_shuffling(G):
    """
    Función que, proporcionándole un objeto grafo del módulo 'networkx':

        1º. Crea 4 clusters iniciales de manera aleatorio utilizando la función
        'get_initial_clusters(G)'.

        2º. Reordena los nodos que forman estos clusters (mediante un algoritmo
        explicado a continuación) de manera que la distancia promedio entre los
        nodos que los forman es mínima.

    ALGORITMO DE ORDENACIÓN ('SHUFFLING'):

    En primer lugar, se crean 4 clusters. Los nodos de dichos clusters se
    asignan de manera aleatoria. Posteriormente, se comienza la reordenación de
    dichos nodos:

        1º. Se escogen 2 clusters de los 4 disponibles al azar.
        2º. De cada cluster, se coge un nodo al azar.
        3º. Se permutan estos dos nodos.
        4º. Se evalúan los nuevos clusters.
            4º a. Si los nuevos clusters son mejores (la distancia promedio
                entre los nodos es menor o igual para permitir mayor
                exploración), se mantienen.
            4º b. Si no lo son (distancia promedio entre los nodos es
                mayor), se deshacen los cambios volviendo a los clusters
                anteriores.

    Este proceso se repetirá hasta que, tras la permutación, no se encuentre un
    algoritmo mejor después de 10.000.000 de veces. Así aseguramos una
    exploración de las posibilidades más que suficiente y fijamos un tiempo
    finito de finalización del proceso.

    ARGS:
        - G: tipo grafo (networkx). Objeto grafo creado con el paquete networkx.

    RETURNS:
        - clusters: tipo diccionario. Las claves son los nombres de los
        clusters, mientras que los valores son listas de instancias de la clase
        Node (son los nodos que forman dicho cluster).
    """
    # Creamos los 4 clusters iniciales.
    print('Creando los 4 clusters iniciales...')
    clusters = get_initial_clusters(G)
    print('Hecho.\n')

    print('Los clusters INICIALES son:')
    show_clusters(clusters)

    # Primero, creamos una lista con las claves del diccionario.
    clusters_list = []

    for key in clusters:
        clusters_list.append(key)

    iterations_count = 0

    changes_count = 0

    no_change_count = 0

    limit = True # Límite de la reordenación (False a los 10m iter. sin cambio).

    while limit:

        # Escogemos dos clusters al azar, comprobando que no sean el mismo.
        rdc1 = '' # 'Random Cluster 1'
        rdc2 = '' # 'Random Cluster 2'
        while rdc1 == rdc2:
            rdc1 = random.choice(clusters_list)
            rdc2 = random.choice(clusters_list)

        # Calculamos su 'score' (distancia promedio entre sus nodos).
        rdc1_distance = get_cluster_score(clusters[rdc1])
        rdc2_distance = get_cluster_score(clusters[rdc2])

        # Quitamos 1 nodo de cada cluster al azar.
        rdc1_node = clusters[rdc1].pop(random.randrange(len(clusters[rdc1])))
        rdc2_node = clusters[rdc2].pop(random.randrange(len(clusters[rdc2])))

        # Ponemos el nodo que quitamos en un cluster al otro cluster.
        clusters[rdc1].append(rdc2_node)
        clusters[rdc2].append(rdc1_node)

        # Calculamos score (distancia promedio entre nodos) de nuevos clusters.
        new_rdc1_distance = get_cluster_score(clusters[rdc1])
        new_rdc2_distance = get_cluster_score(clusters[rdc2])

        """
        - score = mejor (menor distancia promedio), mantenemos nuevos grupos.
        - score = igual, mantenemos nuevos grupos para explorar.
        - score = peor (mayor distancia promedio), vuelven grupos anteriores.

        Si no hay cambio, se registra. Cuando se lleve 10.000.000 iteraciones
        sin cambio, se detendrá el proceso de reordenación.
        """
        if (new_rdc1_distance > rdc1_distance or
            new_rdc2_distance > rdc2_distance):

            del clusters[rdc1][-1]
            clusters[rdc1].append(rdc1_node)

            del clusters[rdc2][-1]
            clusters[rdc2].append(rdc2_node)

            no_change_count += 1

        else:
            changes_count += 1

            no_change_count = 0

        iterations_count += 1

        if no_change_count == 10000000:
            print('Se han realizado', iterations_count, 'iteraciones.')
            print('Ha habido', changes_count, 'cambios.')
            print('Hace', no_change_count, 'iteraciones que no hay cambios.')
            print('Se detiene el proceso de reordenación.')
            print('')

            limit = False

        elif iterations_count % 1000000 == 0:
            print('Iteración nº:',iterations_count)
            print('Se han realizado', changes_count, 'cambios.')
            print('Iteraciones desde el último cambio:',no_change_count)
            print('')

    print('Tras finalizar el algoritmo, los clusters FINALES son:')
    show_clusters(clusters)

    return clusters

def main():

    file_name = 'cubos20.txt' # Debe estar en el directorio actual.
    other_file_name = 'proteinas20.txt'

    G = nx.read_adjlist(file_name) # Leemos el .txt con el grafo.
    C = nx.read_adjlist(other_file_name) # Leemos el .txt con el grafo.

    # draw_net(G)
    # draw_net(C)
    """
    Creamos la matriz de adyacencias 'adj' a partir del grafo:
    """
    adj = get_adj(G)

    """
    Creamos la matriz de distancias mínimas 'C' con utilizando el algoritmo de
    Floyd-Marshall que ya viene implementado en el módulo networkx. Seguidamente
    resolvemos las 5 primeras cuestiones de la Act1.
    """
    min_dist = get_min_dist(G) # Q2

    diameter = get_diameter(G) # Q1

    average_distance = get_average_dist(G) # Q3

    direct_inter = get_direct_interact(G) # Q4

    min10_average_dist = get_10min_average_dist(G) # Q5

    """
    Creamos los 4 clusters iniciales y los reordenamos mediante un algoritmo
    (explicado en la función 'clusters_shuffling()') de manera que la distancia
    entre los nodos que forman un cluster es mínima.
    """
    clusters = clusters_shuffling(G) # Q6

if __name__ == '__main__':
    main()
