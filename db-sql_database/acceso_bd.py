#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
acceso_bd.py

Ejercicio de acceso a la base de datos empresa de masterbio utilizando las
clases empleado y empleadoDao.

Autor: Francisco Martínez Picó
Versión: 1.0
Fecha: 21/03/2020
"""
import sys
from db.database import Database
from db.empresa import Departamento, DepartamentoDao, Empleado, EmpleadoDao
##########################################################
##                                                      ##
##                Acceso a Base de Datos                ##
##                                                      ##
##########################################################
if __name__ == '__main__':

    ## Datos de conexión a la base de datos
    host   = 'masterbio.uv.es'
    user   = 'bioinfo'
    passwd = 'bioinfo'
    dtbase = 'empresa'

    try:
        database = Database(host, user, passwd, dtbase)

    except:
        sys.exit(1)

    edao = EmpleadoDao(database)

    # Crea empleado y lo escribe en la base de datos
    empleado = Empleado({'nombre':'Pepito', 'apellidos':'Perez Palacios',
                         'departamento':'3', 'fechaContrato':'2020-05-20',
                         'puesto':'SLS', 'nivelEducacion':'5', 'sueldo':'25000',
                         'complemento':'500'})
    print('\nSe ha creado el empleado "Pepito Perez Palacios"')
    edao.save(empleado)

    # Busca un empleado por código
    print('\nBuscando el empleado de código 50...')
    emple = edao.findbyid(50)
    if (emple):
        print('                ID: %s' % emple.idEmpleado)
        print('            Nombre: %s' % emple.nombre)
        print('         Apellidos: %s' % emple.apellidos)
        print('      Departamento: %s' % emple.departamento)
        print(' Fecha de Contrato: %s' % emple.fechaContrato)
        print('            Puesto: %s' % emple.puesto)
        print('Nivel de Educación: %s' % emple.nivelEducacion)
        print('            Sueldo: %s' % emple.sueldo)
        print('       Complemento: %s' % emple.complemento)
    else:
        print('  No se encontra un empleado con código 50')

    # Busca un empleado por nombre
    emple = edao.findbyname('Pepito')
    print('\nHay %d empleado(s) con nombre "Pepito"' % len(emple))
    for e in emple:
        print('            ID: %s' % e.idEmpleado)
        print('        Nombre: \033[91m%s\033[0m' % e.nombre)
        print('     Apellidos: %s' % e.apellidos)

    # Guarda el código del empleado para usarlo después
    id = emple[0].idEmpleado

    # Busca un empleado por (LIKE) nombre
    emple = edao.findlikename('Fran')
    print('\nHay %d empleados(s) con "Fran"' % len(emple))
    for e in emple:
        print('            ID: %s' % e.idEmpleado)
        print('        Nombre: \033[91m%s\033[0m' % e.nombre)
        print('     Apellidos: %s' % e.apellidos)

    # Actualiza los datos de un empleado
    print('\nModificado el nombre del empleado %d' % id, end='')
    print(' de "Pepito" ==> "Jose"')
    empleado = edao.findbyid(id)
    empleado.nombre = 'Jose'
    edao.update(empleado)

    # Busca el empleado por nombre
    emple = edao.findbyname('Jose')
    print('\nHay %d empleado(s) que se llamen "Jose"' % len(emple))
    for e in emple:
        print('            ID: %s' % e.idEmpleado)
        print('        Nombre: \033[91m%s\033[0m' % e.nombre)
        print('     Apellidos: %s' % e.apellidos)

    # Borra el empleado
    if len(emple) != 0:
        print('\nBorrado el empleado %s' % emple[0].nombre)
        edao.delete(emple[0].idEmpleado)
    else:
        print('No se puede borrar un empleado con ese nombre')
