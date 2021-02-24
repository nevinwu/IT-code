#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""divisibilidad_procesos.py

Un número primo es aquel cuyos únicos divisores son la unidad (1) y él mismo.
Para comprobar si un número es primo, este programa itera desde 1 hasta el mismo
número introducido realizando divisiones. Se lleva la cuenta del número de
divisores existentes. Cuando termina la iteración. Si el número de divisores es
mayor que 2, el número introducido no se considera primo.

Esta es la versión concurrente mediante procesos del programa.

Versión: 1.0
Autor: Francisco Martínez Picó

Fecha: 12/11/2020
"""
from multiprocessing import Process, Array
from time import time

class AveriguaPrimo(Process):
    def __init__(self, i, num, referencia, divisores):
        """
        Se inicializa la instancia de clase. Esta clase hereda de Process.
        INPUTS:
        - i: indice del proceso
        - num
        - referencia
        - divisores
        """
        Process.__init__(self)
        self.i = i
        self.num = num
        self.referencia = referencia
        self.divisores = divisores

    def run(self):
        """
        Al lanzar el proceso se comprueba si el rango de números que ha recibido
        son divisores del número introducido. Si lo son, se añaden a la cola.
        """
        for j in self.referencia:
            if self.num % j == 0:
                self.divisores[self.i] += 1

def main():
    num = int(input('Introduce un número entero: '))

    p = int(input('Introduzca el número de procesos: '))

    # Lista de posibles divisores a comprobar.
    posibles = list(range(1, num + 1))

    # Tomamos el tiempo en el que comienza la búsqueda.
    tiempo_inicio = time()

    lista_procesos = []
    divisores = Array('i', p, lock = False)

    trozo = len(posibles) // p
    resto = len(posibles) % p
    inicio = 0

    for i in range(p):
        if resto != 0:
            trozo_final = trozo + 1
        else:
            trozo_final = trozo

        fin = inicio + trozo_final
        referencia = posibles[inicio:fin]
        lista_procesos.append(AveriguaPrimo(i, num, referencia, divisores))
        lista_procesos[i].start()
        inicio = fin

    for i in range(p):
        lista_procesos[i].join()


    # Tomamos el tiempo en el que finaliza la búsqueda.
    tiempo_fin = time()

    tiempo_busqueda = tiempo_fin - tiempo_inicio

    if sum(divisores) > 2:
        print('El número %d NO es primo.' % num)
    else:
        print('El número %d SÍ es primo' % num)

    print('El programa ha tardado %5.4f segundos.' % tiempo_busqueda)

if __name__ == '__main__':
    main()
