#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
fuerzab_secuencial.py

Programa de búsqueda de una secuencia patrón en una secuencia problema obtenida
de un fichero FASTA. Se implementa un algoritmo de fuerza bruta: se navega
sobre la cadena problema (genoma) desde el primer carater de la secuencia patrón.
Se irá desplazando sobre la secuencia problema hasta obtener una coincidencia
total.

Esta es la versión secuencial del programa.

Versión: 1.0
Autor: Francisco Martínez Picó

Fecha: 12/11/2020
"""
from time import time

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
        cad_patron = str(input("Introduce la secuencia patron: "))

        # Pasar a mayúsculas para evitar errores.
        cad_patron = cad_patron.upper ()

        # Comprobamos que todo lo introducido son nucleótidos (G, C, T, A o U).
        if (cad_patron.count ("G") + cad_patron.count ("C") +
           cad_patron.count("T") + cad_patron.count ("A") +
           cad_patron.count ("U")) == len(cad_patron):
            break
        else:
            print ("\nNo has introducido una secuencia de ADN/ARN.\n")

    return cad_patron

def alineamiento(patron, sec):
    """
    Esta función alinea dos cadenas sin gaps (espacios). No corrije si es ADN o
    ARN. Es decir, se considera que T no es equivalente a U. Las dos secuencias
    a comparar pueden tener longitudes diferentes.

    INPUTS:
        - patron (tipo cadena): es la cadena que se va a buscar sobre la
        secuencia de referencia.
        - sec (tipo cadena): es la secuencia de referencia (en este caso, el
        genoma). No contiene la cabecera.

    RETURNS:
        - coincidencias (tipo lista): contiene las posiciones de la secuencia de
        referencia (genoma) en las que se ha producido coincidencia completa de
        la secuencia patrón. Es decir, las posiciones del match.
	"""
    coincidencias = []
    longS = len(sec)
    longP = len(patron)

    i = 0

    # Con este bucle buscamos coincidencias de la cad_patron, partir del
    # índice i, en la sec empezando por el índice 0 (j) sólo hasta un rango.
    for i in range(longS - longP):

        j = 0

        # Desde el índice 0 avanzamos mientras este sea menor que la longP.
        while (j < longP):

            if (sec[i + j] != patron[j]):
                # Índice i y j de la sec es diferente al índice j del patrón
                # rompo la búsqueda y avanzo una posición en el bucle while,
                # así hasta que recorra la secuencia.
                break

            j += 1

        if (j == longP):
            i += 1
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

    # Pedimos el patrón y comprobamos que es una secuencia de nucleótidos.
    cad_patron = introducir_cadena()

    # Tomamos el tiempo en el que comienza la búsqueda.
    tiempo_inicio = time()

    # Se realiza la búsqueda.
    coincidencias = alineamiento(cad_patron, sec)
    print("\nExiste una coincidencia a partir del indice:", coincidencias)

    # Tomamos el tiempo en el que finaliza la búsqueda.
    tiempo_fin = time()

    tiempo_busqueda = tiempo_fin - tiempo_inicio

    print("\nLa búsqueda ha tardado %5.4f segundos." %tiempo_busqueda)

if __name__ == '__main__':
    main ()
