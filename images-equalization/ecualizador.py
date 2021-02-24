#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
I02_ecualizador.py

Este programa normaliza el histograma de colores de una imagen en formato .ppm
mediante la siguiente fórmula:

val_norm = int((val_ori – min) / (max – min) * 255)

Es decir, para cada color, se calculan los valores máximos y mínimos y se aplica
una normalización para cada uno de los valores RGB. De esta forma se consigue
una mejora visual de la imagen. Se utiliza concurrencia (procesos).

Versión: 1.0
Autor: Francisco Martínez Picó

Fecha: 25/10/2020
"""
from multiprocessing import Process, Queue, Array
from time import time
import traceback

class MaxMin(Process):
    """
    Clase que hereda del objeto Process (módulo multiprocessing).
    """
    def __init__ (self, array_rojo, array_verde, array_azul, inicio, final,
                  cola_roja, cola_verde, cola_azul):
        """
        Inicializa el objeto.
        """
        Process.__init__(self) # Hereda atributos de Process.
        self.rojo = array_rojo
        self.verde = array_verde
        self.azul = array_azul
        self.inicio = inicio # Índice del primer valor RGB.
        self.final = final # Índice del último valor RGB.
        self.cola_roja = cola_roja # Cola donde se añadirán máximos y mínimos.
        self.cola_verde = cola_verde # Cola donde se añadirán máximos y mínimos.
        self.cola_azul = cola_azul # Cola donde se añadirán máximos y mínimos.

    def run(self):
        """
        Código que se ejecuta al lanzar el proceso. Se añaden máximos y mínimos
        a la cola del color correspondiente. Por cada proceso, se añadirán dos
        valores (uno máximo y otro mínimo) a estas colas.
        """
        # Rojo:
        max_val = self.rojo[0]
        min_val = self.rojo[0]

        for j in range(self.inicio, self.final):

            if self.rojo[j] > max_val:
                max_val = self.rojo[j]

            elif self.rojo[j] < min_val:
                min_val = self.rojo[j]

        self.cola_roja.put(max_val)
        self.cola_roja.put(min_val)

        # Verde:
        max_val = self.verde[0]
        min_val = self.verde[0]

        for j in range(self.inicio, self.final):

            if self.verde[j] > max_val:
                max_val = self.verde[j]

            elif self.verde[j] < min_val:
                min_val = self.verde[j]

        self.cola_verde.put(max_val)
        self.cola_verde.put(min_val)

        # Azul:
        max_val = self.azul[0]
        min_val = self.azul[0]

        for j in range(self.inicio, self.final):

            if self.azul[j] > max_val:
                max_val = self.azul[j]

            elif self.azul[j] < min_val:
                min_val = self.azul[j]

        self.cola_azul.put(max_val)
        self.cola_azul.put(min_val)

class Ecualizar(Process):
    """
    Clase que hereda del objeto Process (módulo multiprocessing).
    """
    def __init__ (self, array_rojo, array_verde, array_azul,
                  inicio, final, colores):
        """
        Inicializa el objeto.
        """
        Process.__init__(self) # Hereda atributos de Process.
        self.rojo = array_rojo
        self.verde = array_verde
        self.azul = array_azul
        self.inicio = inicio # Índice del primer píxel.
        self.final = final # Índice del último píxel.
        self.colores = colores # Diccionario con los max/min por color.

    def run (self):
        """
        Código que se ejecuta al lanzar el proceso. En este caso, la
        normalización de los píxeles teniendo en cuenta los máximos y mínimos
        mediante la siguiente fórmula:
        val_norm = int((val_ori – min) / (max – min) * 255)
        """
        # Rojo:
        max_rojo = self.colores["rojos"][0]
        min_rojo = self.colores["rojos"][1]
        rango_rojo = max_rojo - min_rojo
        for j in range(self.inicio, self.final):
            self.rojo[j] = int((self.rojo[j] - min_rojo) /
                               (rango_rojo) * 255)

        # Verde:
        max_verde = self.colores["verdes"][0]
        min_verde = self.colores["verdes"][1]
        rango_verde = max_verde - min_verde
        for j in range(self.inicio, self.final):
            self.verde[j] = int((self.verde[j] - min_verde) /
                                (rango_verde) * 255)

        # Azul:
        max_azul = self.colores["azules"][0]
        min_azul = self.colores["azules"][1]
        rango_azul = max_azul - min_azul
        for j in range(self.inicio, self.final):
            self.azul[j] = int((self.azul[j] - min_azul) /
                               (rango_azul) * 255)

def leer_fichero(nombre):
    """
    Función encargada de leer el fichero. Se comprueba el número mágico P3 para
    verificar que es un archivo en el formato correcto. Seguidamente, se obtiene
    información de las dimensiones y se va leyendo el archivo guardando la
    información de los colores RGB para cada píxel en tres arrays (uno para cada
    color R, G y B). Esto lo consigue utilizando la función guardar_rgb().
    Guardamos la información en arrays ya que utilizaremos concurrencia/procesos
    en la ejecución del programa.
    ARGS:
        - nombre (str): nombre del archivo a abrir.
    RETURNS:
        - fil (int): número de filas en la matriz de valores original.
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
            dimension = in_file.readline() # Dimensión = nº filas x nº columnas.
            dimension = dimension.rstrip()
            a, b = dimension.split()
            fil = int(a)
            col = int(b)

            in_file.readline() # Valor máximo dentro de los RGB.

            rojo, verde, azul = guardar_arrays(fil, col, in_file)

            return fil, col, rojo, verde, azul

        else:
            print("Error, el fichero introducido no tiene el formato adecuado")

        in_file.close()

def guardar_arrays(fil, col, in_file):
    """
    Se guardan, para cada pixel, sus valores correspondientes al rojo, verde y
    azul en un array (un array para cada color). Se utiliza este objeto para
    usar procesos, ya que los arrays permiten compartir memoria entre procesos.
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

    i = 0 # Contador.

    while i < (fil * col):
        linea = in_file.readline()
        linea = linea.rstrip()
        lista = linea.split()

        while lista:
            array_rojo[i] = int(lista.pop(0))
            array_verde[i] = int(lista.pop(0))
            array_azul[i] = int(lista.pop(0))

            i += 1

    return array_rojo, array_verde, array_azul

def max_min_colores(cola_roja, cola_verde, cola_azul):
    """
    Esta función complementa a la clase MaxMin en el objetivo de averiguar los
    valores máximos y mínimos para cada color. Con la clase MaxMin, obtenemos
    colas (una por color) donde cada proceso ha añadido los valores máximos y
    mínimos que ha encontrado en los valores que se le asignan (es decir, unos
    máximos y mínimos relativos). Esta función recorre esos valores para
    averiguar los máximos y mínimos absolutos de todos los valores de cada color
    y los guarda en un diccionario, ya que serán necesarios para la
    normalización.
    ARGS:
        - cola_roja (Queue): cola con los valores máximos y mínimos que ha
        encontrado cada proceso.
        - cola_verde (Queue): cola con los valores máximos y mínimos que ha
        encontrado cada proceso.
        - cola_azul (Queue): cola con los valores máximos y mínimos que ha
        encontrado cada proceso.
    RETURNS:
        - colores (diccionario): las claves corresponden con los colores. Los
        valores son, en orden, el valor máximo para ese color y, el segundo, el
        valor mínimo.
    """
    colores = {"rojos" : [0, 10000],
               "verdes" : [0, 10000],
               "azules" : [0, 10000]}

    # Rojo:
    while not cola_roja.empty():
        nuevo = cola_roja.get()
        colores["rojos"][0] = max(colores["rojos"][0], nuevo)
        colores["rojos"][1] = min(colores["rojos"][1], nuevo)

    # Verde:
    while not cola_verde.empty():
        nuevo = cola_verde.get()
        colores["verdes"][0] = max(colores["verdes"][0], nuevo)
        colores["verdes"][1] = min(colores["verdes"][1], nuevo)

    # Azul:
    while not cola_azul.empty():
        nuevo = cola_azul.get()
        colores["azules"][0] = max(colores["azules"][0], nuevo)
        colores["azules"][1] = min(colores["azules"][1], nuevo)

    return colores

def generar_imagen(fil, col, rojo, verde, azul, fich):
    """
    Escribe los valores RGB correspondientes a cada píxel en el nuevo archivo
    para generar la imagen ecualizada con el histagrama de colores ampliado.
    ARGS:
        - fil (int): número de filas.
        - col (int): número de columnas.
        - rojo (array): array con los valores de rojo. Cada posición
        corresponde a un píxel. Se guardan en orden (1ª posición = 1º píxel...).
        - verde (array): array con los valores de verde. Cada posición
        corresponde a un píxel. Se guardan en orden (1ª posición = 1º píxel...).
        - azul (array): array con los valores de azul. Cada posición
        corresponde a un píxel. Se guardan en orden (1ª posición = 1º píxel...).
        - fich (str): nombre inicial del archivo. Se modificará para escribir el
        archivo de salida.
    """
    # Busca el último punto del nombre del fichero (.ppm).
    index = fich.rfind('.')
    # El nombre del fichero será desde el principio hasta ese último punto.
    nombre = fich[0:index]

    # El nuevo nombre añadirá "_ecual", de (imagen ecualizada)
    nombre = nombre + '_ecual.ppm'
    fout = open(nombre, "w", encoding = 'ascii')
    fout.write("P3\n")

    dimension = str(fil) + " " + str(col) + "\n"
    fout.write(dimension)

    max_val = max(max(rojo), max(verde), max(azul))
    max_val = str(max_val) + "\n"
    fout.write(max_val)

    contador = 0

    # Vamos escribiendo los valores de gris desplazándonos con un contador:
    for i in range(fil):
        for j in range(col):
            fout.write(str(rojo[contador]))
            fout.write(" ")
            fout.write(str(verde[contador]))
            fout.write(" ")
            fout.write(str(azul[contador]))

            contador += 1

            # Si no es el último valor, introducimos un espacio.
            if j != col - 1:
                fout.write(" ")

        fout.write("\n")

    fout.write("\n")

    fout.close()

def main():
    # Tomamos el tiempo inicial.
    tiempo_inicio = time()

    # 1) Pedimos nombre del fichero y el nº de procesos a utilizar:
    fich = input("Introduzca el nombre del fichero: ")

    p = int(input("Introduzca el numero de procesos: "))

    # 2) Leemos la imagen, comprobamos que es un fichero ‘ppm’ tipo ‘ascii’.
    # Comprobamos el número mágico ("P3") y se guarda en memoria.
    fil, col, rojo, verde, azul = leer_fichero(fich)

    # 3) Paralelizamos el problema en varios procesos:
    lista_procesos = []

    # Declaramos las colas utilizadas para hayar valores máximos y mínimos de
    # cada color.
    cola_roja = Queue()
    cola_verde = Queue()
    cola_azul = Queue()

    dim = fil * col # Nº de valores RGB en la imagen (cada píxel tendrá 3).
    n = dim // p # Cuantos valores RGB calculará 1 proceso.
    resto  = dim % p # Guardamos por si la división no es exacta y sobran.

    inicio = 0

    for i in range(p):
        final = inicio + n

        # Puede que al dividir entre procesos, el reparto de valores RGB no sea
        # exacto (y tenga un resto). Por ello, se reparten estos píxeles entre
        # procesos.
        if resto != 0:
            final += 1
            resto -= 1

        # 4) Calculamos máximos y mínimos de cada color utilizando procesos.
        # Realmente se obtienen colas con los valores máximos y mínimos de cada
        # porción paralelizada.
        lista_procesos.append(MaxMin(rojo, verde, azul, inicio, final,
                                     cola_roja, cola_verde, cola_azul))
        lista_procesos[i].start()

        # El inicio del nuevo proceso será el final del anterior.
        inicio = final

    # Comprobamos que los procesos han acabado.
    for i in range(p):
        lista_procesos[i].join()

    # Función auxiliar para guardar los máximos y mínimos en un diccionario por
    # colores.
    colores = max_min_colores(cola_roja, cola_verde, cola_azul)

    # 5) De nuevo, paralelizamos el problema en varios procesos para la
    # normalización de los valores RGB de la imagen:
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

        lista_procesos.append(Ecualizar(rojo, verde, azul,
                                        inicio, final, colores))
        lista_procesos[i].start()

        # El inicio del nuevo proceso será el final del anterior.
        inicio = final

    # Comprobamos que los procesos han acabado.
    for i in range(p):
        lista_procesos[i].join()

    # 6) En último lugar, se genera la nueva imagen ecualizada (con el
    # histograma de colores ampliado/más uniforme).
    generar_imagen(fil, col, rojo, verde, azul, fich)

    # Tomamos tiempo final.
    tiempo_final = time()

    print("La ejecución del programa con %i procesos ha tardado:" %p)
    print(tiempo_final - tiempo_inicio)

if __name__ == '__main__':
    main ()
