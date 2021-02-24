#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
color_secuencial.py

Este programa recibe como entrada una imagen en formato ppm (ascii) y elimina su
información del color que contiene, devolviendo la misma imagen pero en una
escala de grises en formato pgm (ascii).

Este programa corresponde con la versión secuencial.

Versión: 1.0
Autor: Francisco Martínez Picó

Fecha: 25/10/2020
"""
from time import time
import traceback

def leer_fichero(nombre):
    """
    Función encargada de leer el fichero. Se comprueba el número mágico para
    verificar que es un archivo en el formato correcto. Seguidamente, se obtiene
    información de las dimensiones y se va leyendo el archivo guardando la
    información de los colores RGB para cada píxel en tres listas (una para cada
    color R, G y B). Esto lo consigue utilizando la función guardar_listas().
    ARGS:
        - nombre (str): nombre del archivo a abrir.
    RETURNS:
        - fila (int): número de filas en la matriz de valores original.
        - col (int): número de columnas en la matriz de valores original.
        - rojo (list): lista con los valores del color rojo. Cada posición
        corresponde a un píxel. Se guardan en orden (1ª posición = 1º píxel...).
        - verde (list): lista con los valores del color verde. Cada posición
        corresponde a un píxel. Se guardan en orden (1ª posición = 1º píxel...).
        - azul (list): lista con los valores del color azul. Cada posición
        corresponde a un píxel. Se guardan en orden (1ª posición = 1º píxel...).
    """
    try:
        in_file = open(nombre, 'r')

    except:
        print("No se ha podido abrir el fichero")
        print(traceback.print_exc()) # Devuelve el error (si se produce).

    else:
        cabecera = in_file.readline()
        cabecera = cabecera.rstrip()

        if (cabecera == 'P3'): # Comprobamos número mágico.
            dimension = in_file.readline()
            dimension = dimension.rstrip()
            a, b = dimension.split() # Dimensión.
            fil = int(a)
            col = int(b)

            in_file.readline() # Valor máximo.

            rojo, verde, azul = guardar_listas(fil, col, in_file) # RGB.

            return fil, col, rojo, verde, azul

        else:
            print("Error, el fichero introducido no tiene el formato adecuado")

        in_file.close()

def guardar_listas(fil, col, in_file):
    """
    Se guardan, para cada pixel, sus valores correspondientes al rojo, verde y
    azul en una lista (una lista para cada color).
    ARGS:
        - fil (int): número de filas.
        - col (int): número de columnas.
        - in_file (file): fichero abierto.

    RETURNS:
        - rojo (list): lista con pixeles correspondientes al color rojo.
        - verde (list): lista con pixeles correspondientes al color verde.
        - azul (list): lista con pixeles correspondientes al color azul.
    """
    # Inicializamos las listas.
    rojo = [int] * (fil * col)
    verde = [int] * (fil * col)
    azul = [int] * (fil * col)

    pos = 0 # Posición, contador para crear las listas en orden.

    for i in range(fil):
        linea = in_file.readline()
        linea = linea.rstrip()
        linea = linea.split()

        for j in range(0, col * 3, 3):
            rojo[pos] = int(linea[j])
            verde[pos] = int(linea[j + 1])
            azul[pos] = int(linea[j + 2])
            pos += 1

    return rojo, verde, azul

def eliminar_color(fil, col, rojo, verde, azul):
    """
    Esta función se encarga de convertir los valores de RGB a la escala de
    grises. Recibe las listas con los valores de rojo, verde y azul (así como el
    número de filas y columnas que tiene la matriz de valores). Para calcular el
    valor de gris correspondiente a cada pixel hace una media aritmética entre
    los valores RGB (es decir, gris = (rojo + verde + azul) / 3). Los nuevos
    valores de gris se devuelven en forma de lista.
    ARGS:
        - fil (int): número de filas.
        - col (int): número de columnas.
        - rojo (list): lista con los valores del color rojo. Cada posición
        corresponde a un píxel. Se guardan en orden (1ª posición = 1º píxel...).
        - verde (list): lista con los valores del color verde. Cada posición
        corresponde a un píxel. Se guardan en orden (1ª posición = 1º píxel...).
        - azul (list): lista con los valores del color azul. Cada posición
        corresponde a un píxel. Se guardan en orden (1ª posición = 1º píxel...).
    RETURNS:
        - gris (list): lista con los valores de gris. Cada posición
        corresponde a un píxel. Se guardan en orden (1ª posición = 1º píxel...).
    """
    gris = []

    for x, y, z in zip(rojo, verde, azul):
        nuevo_valor = (x + y + z)//3
        gris.append(nuevo_valor)

    # Eliminamos las listas con los colores anteriores para liberar memoria.
    rojo.clear()
    verde.clear()
    azul.clear()

    return gris

def generar_imagen(fil, col, gris, fich):
    """
    Escribe los valores de gris correspondientes a cada píxel en el nuevo
    archivo para generar la imagen en escala de grises.
    ARGS:
        - fil (int): número de filas.
        - col (int): número de columnas.
        - gris (list): lista con los valores de gris. Cada posición
        corresponde a un píxel. Se guardan en orden (1ª posición = 1º píxel...).
        - fich (str): nombre inicial del archivo. Se modificará para escribir el
        archivo de salida.
    """
    # Busca el último punto (.ppm).
    index = fich.rfind('.')
    # El nombre del fichero será desde el principio hasta el último punto.
    nombre = fich[0:index]
    # El nombre del archivo de salida cuenta con esta extensión.
    nombre = nombre + '_gray.pgm'

    fout = open(nombre, "w", encoding='ascii')
    fout.write("P2\n") # Cambiamos el número mágico al del adecuado al formato.

    dimension = str(fil) + " " + str(col) + "\n"
    fout.write(dimension)

    maxi = max(gris)
    maxi = str(maxi) + "\n"
    fout.write(maxi)

    contador = 0

    # Vamos escribiendo los valores de gris desplazándonos con un contador:
    for i in range(fil):
        for j in range(col):
            fout.write(str(gris[contador]))
            contador += 1
            # Si no es el último valor, introducimos un espacio.
            if j != col-1:
                fout.write(" ")

        fout.write("\n")

    fout.write("\n")

    fout.close()

def main():
    # 1) Pedimos el nombre del fichero. Debe estar en el directorio actual:
    fich = input("Introduzca el nombre del fichero: ")

    # 2) Leemos la imagen, comprobamos que es un fichero ‘ppm’ tipo ‘ascii’ y
    # se guarda en una matriz.
    fil, col, rojo, verde, azul = leer_fichero(fich)

    # 3) Generamos la nueva imagen cambiando el color a escala de grises.
    gris = eliminar_color(fil,col,rojo,verde,azul)

    # 4) Se guarda la nueva imagen cambiando el nombre al que tenía mas
    # ‘_gray’ y el formato a '.pgm'.
    generar_imagen(fil,col,gris,fich)

if __name__ == '__main__':
    main()
