#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
G03_boyer_procesos.py

Este programa implementa el algoritmo de Boyer-Moore para llevar a cabo la
búsqueda de una secuencia patrón (introducida por teclado) sobre una secuencia
de referencia (contenida en un fichero, se solicita el nombre de éste). Se
decuelve las posiciones de match entre la secuencia patrón y la de referencia
así como el tiempo que ha tardado en completarse la búsqueda.

Esta es la versión concurrente mediante el uso de procesos.

Versión: 1.0
Autor: Francisco Martínez Picó

Fecha: 12/11/2020
"""
from multiprocessing import Process, Queue
from time import time

class BuscaCoincidencias(Process):

    def __init__(self, dic, patron, secuencia, q, inicio):
        """
        Se inicializa la instancia de clase. Esta clase hereda de Process.

        INPUTS:
            - dic (tipo diccionario): se trata de la tabla de desplazamientos.
            - patron (tipo string): cadena que estás buscando en la cadena de
            referencia.
            - secuencia (tipo string): cadena sobre la que se va a buscar
            el patrón.
            - q (tipo Queue): cola para comunicarse entre los procesos.
            - inicio (tipo integer): posición absoluta de la secuencia en la que
            cada proceso empezará a buscar.
        """
        Process.__init__(self)
        self.dic = dic
        self.patron = patron
        self.secuencia = secuencia
        self.q = q
        self.inicio = inicio

    def run(self):
        coincidencias = boyer_moore(self.dic, self.patron, self.secuencia)

        for n in coincidencias:
            self.q.put(n + self.inicio)

def leer_fasta(file):
    """
    Esta función recibe el nombre del fichero que contiene la secuencia, lo
    abre, lee la secuencia de referencia y la devuelve para guardarla en
    memoria. Esta secuencia de referencia será sobre la que se realizará la
    búsqueda del patrón.

    INPUT:
        - file (tipo string): es una cadena que corresponde con el nombre del
        archivo que contiene la secuencia de referencia.

    RETURN:
        - sec (tipo cadena): es la secuencia de referencia (en este caso, el
        genoma). No contiene la cabecera.
    """
    sec = ""

    file = open(file, "r")

    for line in file:

        if ">" not in line:
            line = line.strip() # Quitamos blancos (saltos de línea).
            sec += line

    file.close()

    return sec

def introducir_cadena():
    """
    Esta función se utiliza para leer la secuencia patrón a buscar sobre la
    secuencia de referencia. Solicita la entrada por teclado de la secuencia
    patrón. Se convierte a mayúsculas y se comprueba que se han introducido
    nucleótidos (DNA o RNA).

    RETURN:
        - cad_patron (tipo cadena): es la cadena que se va a buscar sobre la
        secuencia de referencia.
    """
    while True:
        # Introducción de la cadena patrón a buscar.
        cad_patron = str(input("Introduce la secuencia patrón: "))

        # Pasar a mayuscualas para evitar errores.
        cad_patron = cad_patron.upper ()

        # Comprobamos que todo lo introducido son nucleótidos (G, C, T, A o U).
        if (cad_patron.count("G") + cad_patron.count("C") +
        cad_patron.count("T") + cad_patron.count("A") +
        cad_patron.count("U") == len(cad_patron)):
            break

        else:
            print ("\nNo has introducido una secuencia de ADN/ARN.\n")

    return cad_patron

def tabla_desplazamientos(cad_patron):
    """
    Esta función se utiliza para crear la tabla de desplazamientos empleada en
    la búsqueda mediante la implementación del algoritmo de Boyer-Moore. En la
    búsqueda con este algoritmo, la comparación entre la secuencia patrón y la
    secuencia de referencia se realiza desde el final de la secuencia patrón
    hasta el inicio de la misma. En el momento que encontremos un carácter no
    coincidente, podemos desplazar la cadena un número determinado de espacios.
    Este número de espacios se averigua mediante el preprocesamiento de la
    secuencia patrón para hallar la tabla de desplazamientos. Este
    preprocesamiento es el que realiza esta función.

    INPUT:
        - cad_patron (tipo cadena): es la cadena que se va a buscar sobre la
        secuencia de referencia.

    RETURN:
        - dic (tipo diccionario): es la tabla de desplazamientos mencionada
        anteriormente.
    """
    dic = {}
    desplaza = 1

    for i in range (len(cad_patron)-1,-1,-1):

        if cad_patron[i] not in dic:
            dic[cad_patron[i]] = desplaza
            desplaza += 1

        else:
            desplaza += 1

    for letra in ["A","C","G","T","U","N"]:

        if letra not in dic.keys():
            dic[letra] = len(cad_patron)

    return dic

def boyer_moore(dic, patron, genoma):
    """
    Esta función lleva a cabo la búsqueda mediante la implementación del
    algoritmo de Boyer-Moore. En la búsqueda con este algoritmo, la comparación
    entre la secuencia patrón y la secuencia de referencia se realiza desde el
    final de la secuencia patrón hasta el inicio de la misma. En el momento que
    encontremos un carácter no coincidente, podemos desplazar la cadena un
    número determinado de espacios. Este número de espacios se averigua mediante
    el preprocesamiento de la secuencia patrón para hallar la tabla de
    desplazamientos.

    INPUTS:
        - dic (tipo diccionario): es la tabla de desplazamientos mencionada
        anteriormente.
        - patron (tipo cadena): es la cadena patrón que se va a buscar sobre la
        secuencia de referencia.
        - genoma (tipo cadena): es la secuencia de referencia sobre la que se va
        a llevar a cabo la búsqueda. No contiene la cabecera.

    RETURNS:
        - coincidencias (tipo lista): contiene las posiciones de la secuencia de
        referencia (genoma) en las que se ha producido coincidencia completa de
        la secuencia patrón. Es decir, las posiciones del match.
    """
    coincidencias = []
    i = 0 # inicio de donde se localiza el patron en el genoma
    a = 1 # indice de la letra que se esta leyendo en el patron (sentido derecha-izq)
    longP = len(patron)
    diferencia = len(genoma) - longP
    match = 0

    while i <= diferencia:

        posletraP = longP - a
        letra_gen = genoma[i + posletraP]
        letra_patron = patron[posletraP]

        if letra_gen != letra_patron:
            match = 0
            desplazamiento = max(1,(dic[letra_gen] - a))
            i += desplazamiento
            a = 1

        else:
            match += 1
            a += 1
            if match == longP:
                match = 0
                i += 1
                a = 1
                coincidencias.append(i)

    return coincidencias

def main():
    """
    Función principal.
    """
    # Pedimos el nombre del archivo.
    fich = input("Introduzca el nombre del fichero: ")

    # Leemos el fichero fasta para obtener secuencia de referencia.
    sec = leer_fasta(fich)

    # Pedimos el patron y comprobamos que es una secuencia de nucleótidos.
    patron = introducir_cadena()

    # Introducimos cuántos procesos queremos utilizar.
    p = int(input("Introduzca el número de procesos: "))

    # Obtenemos la tabla de desplazamientos.
    dic = tabla_desplazamientos(patron)

    # print("\nTabla de desplazamientos", dic)

    # Tomamos el tiempo en el que comienza la búsqueda.
    tiempo_inicio = time()

    lista_procesos = []
    q = Queue()

    longitud = len(sec)
    tamaño = longitud // p
    resto = longitud % p
    longPatron = len(patron) - 1
    inicio = 0

    for i in range(p):

        if resto != 0:
            tamañofinal = tamaño + 1

        else:
            tamañofinal = tamaño

        fin = inicio + tamañofinal + longPatron
        secuencia =  sec[inicio:fin]
        lista_procesos.append(BuscaCoincidencias(dic, patron, secuencia, q,
                                                 inicio))
        lista_procesos[i].start()
        inicio = fin - longPatron

    # Unimos los procesos
    for i in range(p):
        lista_procesos[i].join()

    coincidencias = []

    while not q.empty():
        coincidencias.append(q.get())

    # Tomamos el tiempo en el que finaliza la búsqueda.
    tiempo_fin = time()

    print("\nCoincidencias: ", coincidencias)

    tiempo_busqueda = tiempo_fin - tiempo_inicio

    print("\nLa búsqueda ha tardado %5.4f segundos." %tiempo_busqueda)

if __name__ == '__main__':
    main ()
