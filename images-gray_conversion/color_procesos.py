#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
G02_color_procesos.py

Este programa recibe como entrada una imagen en formato ppm (ascii) y elimina su
información del color que contiene, devolviendo la misma imagen pero en una
escala de grises en formato pgm (ascii).

Este programa corresponde con la versión paralelizada con el uso de procesos.

Versión: 2.1
Autor: Francisco Martínez Picó

Fecha: 25/10/2020
"""
from multiprocessing import Process, Array
from time import time
import traceback

class EliminarColor(Process):
    """
    Clase que hereda del objeto Process (módulo multiprocessing).
    """
    def __init__ (self, array_rojo, array_verde, array_azul, inicio, final):
        """
        Inicializa el objeto.
        """
        Process.__init__(self) # Hereda atributos de Process.
        self.rojo = array_rojo
        self.verde = array_verde
        self.azul = array_azul
        self.inicio = inicio # Índice del primer pixel.
        self.final = final # Índice del último pixel.

    def run (self):
        """
        Para lanzar el proceso.
        """
        for j in range(self.inicio,(self.final)):
            suma = ((self.rojo[j] + self.verde[j] + self.azul[j]) // 3)

            # Arbitrariamente, se guardan los nuevos valores de gris en el array
            # que contenía los valores para el rojo.
            self.rojo[j] = suma

def leer_fichero(nombre):
    """
    Función encargada de leer el fichero. Se comprueba el número mágico para
    verificar que es un archivo en el formato correcto. Seguidamente, se obtiene
    información de las dimensiones y se va leyendo el archivo guardando la
    información de los colores RGB para cada píxel en tres listas (una para cada
    color R, G y B). Esto lo consigue utilizando la función guardar_rgb().
    ARGS:
        - nombre (str): nombre del archivo a abrir.
    RETURNS:
        - fila (int): número de filas en la matriz de valores original.
        - col (int): número de columnas en la matriz de valores original.
        - rojo (array): array con los valores del color rojo. Cada posición
        corresponde a un píxel. Se guardan en orden (1ª posición = 1º píxel...).
        - verde (array): array con los valores del color verde. Cada posición
        corresponde a un píxel. Se guardan en orden (1ª posición = 1º píxel...).
        - azul (array): array con los valores del color azul. Cada posición
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
            dimension = dimension.rstrip() # Dimensión.
            a, b = dimension.split()
            fil = int(a)
            col = int(b)

            in_file.readline() # Valor máximo.

            rojo, verde, azul = guardar_arrays(fil, col, in_file) # RGB.

            return fil, col, rojo, verde, azul

        else:
            print("Error, el fichero introducido no tiene el formato adecuado")

        in_file.close()

def guardar_arrays(fil, col, in_file):
    """
    Se guardan, para cada pixel, sus valores correspondientes al rojo, verde y
    azul en un array (un array para cada color). Se utiliza este objeto para
    utilizar procesos, ya que los arrays suponen memoria compartida.
    ARGS:
        - fil (int): número de filas.
        - col (int): número de columnas.
        - in_file (file): fichero abierto.
    RETURNS:
        - rojo (array): array con valores correspondientes al color rojo.
        - verde (array): array con valores correspondientes al color verde.
        - azul (array): array con valores correspondientes al color azul.
    """
    array_rojo = Array('i', fil * col, lock = False)
    array_verde = Array('i', fil * col, lock = False)
    array_azul = Array('i', fil * col, lock = False)

    i = 0

    while i < (fil * col):
        linea = in_file.readline()
        linea = linea.rstrip()
        lista = linea.split()

        n = 0

        for j in range(col):
            array_rojo[i] = int(lista[n])
            array_verde[i]= int(lista[n + 1])
            array_azul[i] = int(lista[n + 2])

            i += 1
            n += 3

    return array_rojo, array_verde, array_azul

def generar_imagen(fil, col, gris, fich):
    """
    Escribe los valores de gris correspondientes a cada píxel en el nuevo
    archivo para generar la imagen en escala de grises.
    ARGS:
        - fil (int): número de filas.
        - col (int): número de columnas.
        - gris (array): array con los valores de gris. Cada posición
        corresponde a un píxel. Se guardan en orden (1ª posición = 1º píxel...).
        Proviene del array_rojo original con los valores sustituidos por los
        procesos.
        - fich (str): nombre inicial del archivo. Se modificará para escribir el
        archivo de salida.
    """
    # Busca el último punto (.ppm)
    index = fich.rfind('.')
    # El nombre del fichero será desde el principio hasta el último punto.
    nombre = fich[0:index]

    nombre = nombre + '_gray.pgm'
    fout = open(nombre, "w", encoding = 'ascii')
    fout.write("P2\n")

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
            if j != col - 1:
                fout.write(" ")

        fout.write("\n")

    fout.write("\n")

    fout.close()

def main():
    # 1) Pedimos nombre del fichero y el nº de procesos a utilizar:
    fich = input("Introduzca el nombre del fichero: ")

    p = int(input("Introduzca el numero de procesos: "))

    # Medimos el tiempo inicial.
    tiempo_inicio = time()

    # 2) Leemos la imagen, comprobamos que es un fichero ‘ppm’ tipo ‘ascii’. Se
    # guarda.
    fil, col, rojo, verde, azul = leer_fichero(fich)
    tiempo_lectura = time()

    # 3) Paralelizamos el problema en varios procesos:
    tiempo_inicio_paralel = time()

    lista_procesos = []

    dim = fil * col
    n = dim // p
    resto  = dim % p
    inicio = 0
    for i in range(p):
        final = inicio + n
        if resto != 0:
            final += 1
            resto -= 1
        lista_procesos.append(EliminarColor(rojo, verde, azul, inicio, final))
        lista_procesos[i].start()
        inicio = final

        # Comprobamos que los procesos han acabado.
    for i in range(p):
        lista_procesos[i].join()

    tiempo_fin_paralel = time()

    # 4) Se guarda la nueva imagen añadiendo al nombre que tenía ‘_gray’ y la
    # extensión "".pgm".
    tiempo_inicio_imagen = time()

    generar_imagen(fil, col, rojo, fich)

    tiempo_fin_imagen = time()

    # Medimos los diferentes tiempos de ejecucion y cremos un fichero de
    # resultados.
    tiempo_final = time()

    # Escribemos un fichero de salida con información respecto a los tiempos que
    # de cada parte.
    tiempo_ejec_total = tiempo_final - tiempo_inicio
    tiempo_ejec_lectura = tiempo_lectura - tiempo_inicio
    tiempo_ejec_paralel = (tiempo_fin_paralel - tiempo_inicio_paralel)
    tiempo_salvar_imagen = (tiempo_fin_imagen - tiempo_inicio_imagen)

    out = 'tiempo_' + str(p) + 'procesos.out'

    resultados = open(out, 'w')
    resultados.write('\nEjecutando el problema con %d proceso(s)...' %p)
    resultados.write('\nEl tiempo de ejecución total es de %5.4f segundos'
                     %tiempo_ejec_total)
    resultados.write('\nEl tiempo de lectura del fichero es de %5.4f segundos'
                     %tiempo_ejec_lectura)
    resultados.write('\nEl tiempo que se tarda en generar la imagen en gris es')
    resultados.write(' de %5.4f segundos' %tiempo_ejec_paralel)
    resultados.write('\nEl tiempo que se tarda en guardar la imagen es')
    resultados.write(' de %5.4f segundos' %tiempo_salvar_imagen)

    resultados.close()

if __name__ == '__main__':
    main()
