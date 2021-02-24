#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
divisibilidad_secuencial.py

Este programa determina si un número introducido por teclado es primo o no. Un
número primo es aquel cuyos únicos divisores son la unidad (1) y él mismo.

Esta es la versión secuencial del programa.

Versión: 1.0
Autor: Francisco Martínez Picó
Fecha: 12/11/2020
"""
from time import time

def primo(num):
    """
    Determina si un número es primo o no. Para ello, itera desde 1 hasta el
    mismo número introducido realizando divisiones. Se lleva la cuenta del
    número de divisores existentes (numeros por los cual se puede dividir
    obteniendo resto 0). Cuando termina la iteración, si el número de divisores
    es mayor que 2, el número introducido no se considera primo.
    INPUT:
    - num (tipo entero): número entero introducido por teclado que se quiere
    averiguar si es primo o no.
    """
    divisores = 0

    for i in range(num + 1):
        if num % (i + 1) == 0:
            divisores += 1

    if divisores > 2:
        print('El número %d NO es primo.' % num)
    else:
        print('El número %d SÍ es primo' % num)

def main():
    num = int(input('Introduce un número entero: '))

    # Tomamos el tiempo en el que comienza la búsqueda.
    tiempo_inicio = time()

    primo(num)

    # Tomamos el tiempo en el que finaliza la búsqueda.
    tiempo_fin = time()

    tiempo_busqueda = tiempo_fin - tiempo_inicio

    print("El programa ha tardado %5.4f segundos." % tiempo_busqueda)

if __name__ == '__main__':
    main()
