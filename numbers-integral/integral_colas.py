#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
integral_procesos.py

Este programa halla el área bajo la curva de la función f(x) = x^2 + 2x + 1
utilizando una aproximación por rectángulos (el lado izquierdo concretamente).
Se toma como input los puntos inicial y final del intervalo en el que queremos
realizar la integral definida así como el número de divisiones (rectángulos) que
queremos utilizar. Además, se mide el tiempo de ejecución del programa.

Esta es la versión paralelizada del programa mediante la utilización de
procesos. De esta forma, la integral se divide en tantas subintegrales como
procesos se lancen. Cada subintegral se calculará en un proceso.

En esta versión se ha añadido el uso de colas para calcular correctamente el
resultado

Versión: 2.0
Autor: Francisco Martínez Picó
Fecha: 22/10/2020
"""
from time import time
from multiprocessing import Process, Queue

class ProcesoIntegral(Process):
    """
    Esta clase hereda los atributos de la clase Process, del módulo threading.
    Además, se le añade el atributo self.res inicializado a 0. Este atributo
    hace referencia al valor del área de la subintegral calculada por ese
    proceso. Al ejecutar cada proceso, se cálcula una subintegral definida.

    Se le añade el sistema de colas.
    """
    def __init__(self, ini, fin, paso, cola):
        """
        Inicialización del objeto.
        """
        Process.__init__(self)
        self.ini = ini
        self.fin = fin
        self.paso = paso
        self.cola = cola
        self.res = 0

    def run(self):
        """
        Para comenzar con el cálculo del proceso.
        """
        self.res = integral_definida(self.ini, self.fin, self.paso)
        self.cola.put(self.res)

def lado_izquierdo(ini, fin, paso):
    """
    Esta función se utiliza para calcular los puntos de la curva que tocan los
    lados izquierdos de nuestros rectángulos. Devuelve estos puntos en forma de
    lista.

    INPUTS:
        - ini: tipo float. Punto desde el que se comienza a calcular la integral
        definida.
        - fin: tipo float. Punto hasta el que se va a calcular la integral
        definida.
        - paso: tipo float. Ancho de los cuadrados utilizados.

    OUTPUTS:
        - puntos: tipo lista. Contiene estos puntos necesarios para la
        sustitución de valores en la integral y así hallar la altura de los
        réctangulos y, posteriromente, el área.
    """
    puntos = list([ini])

    while ini < (fin - paso):
        ini += paso
        puntos.append(ini)

    return puntos

def calcular_area(puntos, paso):
    """
    Esta función se utiliza para calcular el área bajo la curva (integral
    definida) siguiendo con la aproximación con rectángulos. Recibe los puntos
    del eje de abscisas donde están los lados izquierdos de los rectángulos, los
    sustituye en la integral para hallar su valor (que es la altura del lado), y
    finalmente, halla el área total.

    INPUTS:
        - puntos: tipo lista. Contiene estos puntos necesarios para la
        sustitución de valores en la integral y así hallar la altura de los
        réctangulos y, posteriromente, el área.
        - paso: tipo float. Ancho de los cuadrados utilizados.

    OUTPUTS:
        - area: tipo float. Valor del área bajo la curva en los intervalos
        definidos. Este valor se devuelve como variable y también se imprime por
        pantalla
    """
    alturas = list()

    while puntos:
        valor = puntos.pop()
        h = valor ** 2 + 2 * valor + 1
        alturas.append(h)

    # Finalmente calculamos el área bajo la curva aproximando con el área de
    # nuestros rectángulos.
    area = paso * (sum(alturas))

    return area

def integral_definida(ini, fin, paso):
    """
    Esta función es una recapitulación del proceso del programa secuencial. Es
    decir, se crea esta función para que únicamente utilizando ésta y las
    variables de ini, fin y paso se calcule la integral. Esto facilita el
    proceso de paralelización, ya que es este proceso de cálculo que realiza
    esta función lo que se va a paralelizar (la integral se divide en
    subintegrales que se calculan en paralelo).

    INPUTS:
        - ini: tipo float. Punto desde el que se comienza a calcular la integral
        definida.
        - fin: tipo float. Punto hasta el que se va a calcular la integral
        definida.
        - paso: tipo float. Ancho de los cuadrados utilizados.
    """
    # Calcularemos los valores de abscisas donde el lado izquierdo de nuestro
    # rectángulo toca la curva para sustituirlos en f(x).
    puntos = lado_izquierdo(ini, fin, paso)

    # Calculamos el valor de la altura de los rectángulos para esos puntos.
    area = calcular_area(puntos, paso)

    return area

def main():
    print(__doc__)

    # Inputs.
    ini = float(input('Introduce el punto INICIAL del intervalo: '))
    fin = float(input('Introduce el punto FINAL del intervalo: '))
    nrect = int(input('Introduce el NÚMERO DE RECTÁNGULOS a utilizar: '))
    nprocesos = int(input('Introduce el NÚMERO DE PROCESOS a utilizar: '))

    # Comenzamos a medir el tiempo.
    tiempo_inicial = time()

    # Llamamos tramo a la longitud del intervalo dado.
    tramo = fin - ini

    # Se calcula el ancho de los cuadrados (paso).
    paso = tramo / nrect

    # Calculamos el tramo que hará cada subintegral en cada proceso.
    subtramo = tramo / nprocesos

    # Los objetos de la clase ProcesoIntegral que hereda de proceso se añadirán
    # a una lista
    lista_procesos = list()

    q = Queue()

    # A diferencia de la versión anterior, ahora pasamos a cada proceso la cola
    # donde pondrá el resultado de la subintegral.
    for i in range(nprocesos):
        # Creamos el proceso.
        t = ProcesoIntegral(ini + subtramo * i,
                         fin/nprocesos + subtramo * i,
                         paso, q)

        # Lo ponemos en la lista.
        lista_procesos.append(t)

        # Lo iniciamos.
        lista_procesos[i].start()

    for proceso in lista_procesos:
        # Esperamos a que haya acabado.
        proceso.join()

    # Pondremos los resultados de las subintegrales en esta lista para sumarlos.
    resultados = list()
    while not q.empty():
        valor = q.get()
        resultados.append(valor)

    print('\nEl ÁREA TOTAL bajo la curva es: ', sum(resultados))

    tiempo_final = time()

    tiempo_ejecucion = tiempo_final - tiempo_inicial
    print('El tiempo de ejecución fue: ', tiempo_ejecucion)

if __name__ == '__main__':
    main()
