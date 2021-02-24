#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
integral_secuencial.py

Este programa halla el área bajo la curva de la función f(x) = x^2 + 2x + 1
utilizando una aproximación por rectángulos (el lado izquierdo concretamente).
Se toma como input los puntos inicial y final del intervalo en el que queremos
realizar la integral definida así como el número de divisiones (rectángulos) que
queremos utilizar. Además, se mide el tiempo de ejecución del programa.

Esta es la versión secuencial del programa, sin ningún tipo de paralelización
del proceso.

Versión: 1.0
Autor: Francisco Martínez Picó
Fecha: 15/10/2020
"""
from time import time

def lado_izquierdo(ini, fin, paso):
    """
    Esta función sencilla se utiliza para calcular los puntos de la curva que
    tocan los lados izquierdos de nuestros rectángulos. Devuelve estos puntos en
    forma de lista

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

def main():
    print(__doc__)

    # Inputs.
    ini = float(input('Introduce el punto INICIAL del intervalo: '))
    fin = float(input('Introduce el punto FINAL del intervalo: '))
    nrect = int(input('Introduce el NÚMERO DE RECTÁNGULOS a utilizar: '))

    # Comenzamos a medir el tiempo.
    tiempo_inicial = time()

    # Se calcula el ancho de los cuadrados (el paso).
    paso = (fin - ini) / nrect

    # Calcularemos los valores de abscisas donde el lado izquierdo de nuestro
    # rectángulo toca la curva para sustituirlos en f(x).
    puntos = lado_izquierdo(ini, fin, paso)

    # Calculamos el valor de la altura de los rectángulos para esos puntos.
    area = calcular_area(puntos, paso)

    print('\nEl ÁREA TOTAL bajo la curva es: ', area)

    tiempo_final = time()

    tiempo_ejecucion = tiempo_final - tiempo_inicial
    print('El tiempo de ejecución fue: ', tiempo_ejecucion)

if __name__ == '__main__':
    main()
