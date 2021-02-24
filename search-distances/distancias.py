#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
distancias.py

Este programa realiza la búsqueda por distancias (distancia de Hamming) de una
secuencia patrón en otra secuencia de referencia.

Versión: 1.0
Autor: Francisco Martínez Picó

Fecha: 12/11/2020
"""
from multiprocessing import Process, Queue
from time import time

class CalculaDistancias(Process):

    def __init__(self, referencia, patron, inicio, similitud, q):
        """
        Se inicializa la instancia de clase. Esta clase hereda de Process.

        INPUTS:
            - secuencia (tipo string): cadena sobre la que se va a buscar
            el patrón.
            - patron (tipo string): subcadena que estás buscando en la cadena de
            referencia.
            - inicio (tipo integer): posición absoluta de la secuencia en la que
            cada proceso empezará a buscar.
            - similitud (tipo integer): número de coincidencias mínimo que tiene
            que haber entre la secuencia patrón y la de referencia para
            considerar una similitud mayor al 90%.
            - q (tipo Queue): cola para comunicarse entre los procesos.
        """
        Process.__init__(self)
        self.patron = patron
        self.referencia = referencia
        self.inicio = inicio
        self.similitud = similitud
        self.q = q

    def run(self):
        """
        Al lanzar el proceso se hace una búsqueda del patrón en la secuencia de
        referencia utilizando las distancias de Hamming.
        """
        coincidencias = distancias_Hamming(self.referencia, self.patron,
                                           self.similitud)
        for c in coincidencias:
            self.q.put(c + self.inicio)

def leer_fasta(file):
    """
    Esta función recibe el nombre del fichero que contiene la secuencia, lo
    abre, lee la secuencia de referencia y la guarda en memoria. Esta secuencia
    de referencia será sobre la que se realizará la búsqueda del patrón.

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
    cad_patron = ""

    while not cad_patron:
        cad_patron = str(input("Introduce la secuencia patrón: "))

        cad_patron = cad_patron.upper ()

        if (cad_patron.count("G") + cad_patron.count("C") +
        cad_patron.count("T") + cad_patron.count("A") +
        cad_patron.count("U") == len(cad_patron)):
            break

        else:
            print ("\nNo se ha introducido una secuencia de ADN/ARN.\n")

    return cad_patron

def distancias_Hamming(referencia, patron, similitud):
    """
    Función utilizada para realizar una búsqueda por distancias de un patrón
    sobre una secuencia de referencia. Concretamente, se utilizan las distancias
    de Hamming. Esta distancia se define como el número de caracteres que tienen
    que cambiarse para transformar una palabra en otra de igual dimensión. La
    cadena de referencia se recorre mediante fuerza bruta.
    INPUTS:
        - referencia (tipo string): cadena sobre la que se va a buscar
        el patrón.
        - patron (tipo string): subcadena que estás buscando en la cadena de
        referencia.
        - similitud (tipo integer): número de coincidencias mínimo que tiene
        que haber entre la secuencia patrón y la de referencia para
        considerar una similitud mayor al 90%.
    RETURNS:
        - coincidencias (tipo lista): es una lista donde cada elemento es el
        inicio de un match (relativo al trozo de secuencia de referencia que se
        le ha pasado). Por ello, la posición de match absoluta será esa posición
        relativa más el punto de la secuencia donde ha comenzado a buscar.
    """
    coincidencias = []

    # Iteramos tantas veces como nucleótidos hay en la secuencia de referencia
    # menos el número de nucleótidos en el patrón.
    for i in range((len(referencia) - len(patron))):
        match = 0

        for x, y in zip(list(referencia[i:]), list(patron)):
            if x == y:
                match += 1

        if match >= similitud:
            coincidencias.append(i)

    return coincidencias

def main():
    """
    Programa principal.
    """
    # Pedimos el nombre del archivo.
    fich = input("Introduzca el nombre del fichero: ")

    # Leemos el fichero fasta para obtener secuencia de referencia.
    sec = leer_fasta(fich)

    # Guardamos la longitud de la secuencia de referencia.
    long_sec = len(sec)

    # Pedimos el patron y comprobamos que es una secuencia de nucleótidos.
    patron = introducir_cadena()

    # Guardamos la longitud de la secuencia patrón a buscar sobre la referencia.
    long_patron = len(patron)

    # ¿Cuántas coincidencias para un % de identidad mayor al 90%? Como se pide
    # identidad > 90%, si la división no es exacta, se exigirá una coincidencia
    # más.
    similitud = int((90 * long_patron) / 100)

    if ((90 * long_patron) % 100) != 0:
        similitud += 1

    # Introducimos cuántos procesos queremos utilizar.
    p = int(input("Introduzca el número de procesos: "))

    # Tomamos el tiempo en el que comienza la búsqueda.
    tiempo_inicio = time()

    lista_procesos = []
    q = Queue()

    tamaño = long_sec // p
    resto = long_sec % p
    inicio = 0

    for i in range(p):
        if resto != 0:
            tamaño_final = tamaño + 1
        else:
            tamaño_final = tamaño

        # Como se va a dividir la secuencia de referencia y puede haber
        # coincidencias que no aparecieran a raíz de esto, a cada procesos se le
        # pasa un trozo de secuencia adicional equivalente a la longitud del
        # patrón.
        fin = inicio + tamaño_final + long_patron
        referencia = sec[inicio:fin]
        lista_procesos.append(CalculaDistancias(referencia, patron, inicio,
                                                similitud, q))
        lista_procesos[i].start()
        inicio = fin - long_patron

    # Unimos los procesos
    for i in range(p):
        lista_procesos[i].join()

    posiciones = []

    while not q.empty():
        posiciones.append(q.get())

    # Tomamos el tiempo en el que finaliza la búsqueda.
    tiempo_fin = time()

    print("\nBuscando una similitud mayor al 90 por ciento (es decir,")
    print("más de %d matches entre el patrón y la referencia)..." % similitud)
    if posiciones:
        print()
        print("Se han encontrado coincidencias en las posiciones: ", posiciones)
    else:
        print("\nNo se han encontrado coincidencias.")

    tiempo_busqueda = tiempo_fin - tiempo_inicio

    print("\nLa búsqueda ha tardado %5.4f segundos." %tiempo_busqueda)

if __name__ == '__main__':
    main()
