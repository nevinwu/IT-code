#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
empresa.py

Contiene la clase Departamento y DepartamentoDao utilizadas para el acceso a la
base de datos empresa de masterbio. Estas dos clases están tomadas del ejemplo
empresa.py del profesor Wladimiro Díaz. Además, cuenta con las clases Empleado y
EmpleadoDao.

MariaDB [empresa]> describe departamentos;
+----------------+-------------+------+-----+---------+----------------+
| Field          | Type        | Null | Key | Default | Extra          |
+----------------+-------------+------+-----+---------+----------------+
| idDepartamento | int(11)     | NO   | PRI | NULL    | auto_increment |
| nombre         | varchar(36) | NO   |     | NULL    |                |
| manager        | int(11)     | YES  | MUL | NULL    |                |
+----------------+-------------+------+-----+---------+----------------+

MariaDB [empresa]> describe empleados;
+----------------+--------------+------+-----+---------+----------------+
| Field          | Type         | Null | Key | Default | Extra          |
+----------------+--------------+------+-----+---------+----------------+
| idEmpleado     | int(11)      | NO   | PRI | NULL    | auto_increment |
| nombre         | varchar(20)  | NO   |     | NULL    |                |
| apellidos      | varchar(50)  | NO   |     | NULL    |                |
| departamento   | int(11)      | NO   | MUL | NULL    |                |
| fechaContrato  | date         | YES  |     | NULL    |                |
| puesto         | char(8)      | YES  |     | NULL    |                |
| nivelEducacion | smallint(6)  | YES  |     | NULL    |                |
| sueldo         | decimal(9,2) | YES  |     | NULL    |                |
| complemento    | decimal(9,2) | YES  |     | NULL    |                |
+----------------+--------------+------+-----+---------+----------------+

Autor: Francisco Martínez Picó
Versión: 1.0
Fecha: 21/03/2020
"""
##########################################################
##                                                      ##
##                  class Departamento                  ##
##                                                      ##
##########################################################
class Departamento(dict):
    """ DTO de la tabla Departamentos """

    # Atributos de la tabla Departamentos
    ATRIBUTOS = ( 'idDepartamento', 'nombre', 'manager')

    def __init__(self, data):
        # Inicializa los valores del objeto
        for key in self.ATRIBUTOS:
            if key in data:
                self[key] = data[key]
            else:
                self[key] = None

    def __getattr__(self, name):
            return self[name]

    def __setattr__(self, name, value):
        self[name] = value

##########################################################
##                                                      ##
##                class DepartamentoDao                 ##
##                                                      ##
##########################################################
class DepartamentoDao(object):
    """ Capa de acceso de la tabla Departamentos """

    # Insercción
    _INSERT = """
       INSERT INTO Departamentos(nombre, manager)
            VALUES (UPPER(%(nombre)s), %(manager)s)
    """

    # Selección por Id
    _FINDBYID = """
       SELECT idDepartamento, nombre, manager
         FROM Departamentos
        WHERE idDepartamento = %(id)s
    """

    # Selección por nombre de departamento
    _FINDBYNAME = """
       SELECT idDepartamento, nombre, manager
         FROM Departamentos
        WHERE UPPER(nombre) = UPPER(%(name)s)
    """

    # Selección por similitud nombre de departamento
    _FINDLIKENAME = """
        SELECT idDepartamento, nombre, manager
          FROM Departamentos
         WHERE UPPER(nombre) LIKE UPPER(%(name)s)
    """

    # Actualización
    _UPDATE = """
        UPDATE Departamentos
           SET nombre = UPPER(%(nombre)s), manager = %(manager)s
         WHERE idDepartamento = %(idDepartamento)s
        """

    # Borrado.
    _DELETE = """
        DELETE FROM Departamentos
              WHERE idDepartamento = %(id)s
       """

    def __init__(self, dbase):
        self.dbase = dbase

    ## MÉTODOS CRUD

    ## Create
    def save(self, departamento):
        """ Añade departamento en la tabla Departamentos """
        self.dbase.query(self._INSERT, departamento)

    ## Read
    def findbyid(self, idd):
        """ Busca el departamento de código idd """
        result = self.dbase.query(self._FINDBYID, {'id':idd})
        if result:
            return Departamento(result[0])
        return None

    def findbyname(self, name):
        """ Busca departamentos con nombre name """
        result = []
        for depto in self.dbase.query(self._FINDBYNAME, {'name':name}):
            result.append(Departamento(depto))
        return result

    def findlikename(self, name):
        """ Busca departamentos con nombre %name% """
        data = '%' + name + '%'
        result = []
        for depto in self.dbase.query(self._FINDLIKENAME, {'name':data}):
            result.append(Departamento(depto))
        return result

    ## Update
    def update(self, departamento):
        """ Actualiza la fila departamento en la tabla """
        self.dbase.query(self._UPDATE, departamento)

    ## Delete
    def delete(self, idd):
        """ Borra una fila de la tabla """
        self.dbase.query(self._DELETE, {'id':idd})

##########################################################
##                                                      ##
##                  class Empleado                      ##
##                                                      ##
##########################################################
class Empleado(dict):
    """ DTO de la tabla Empleados """

    # Atributos de la tabla Empleados
    ATRIBUTOS = ( 'idEmpleado', 'nombre', 'apellidos', 'departamento',
                  'fechaContrato', 'puesto', 'nivelEducacion', 'sueldo',
                  'complemento')

    def __init__(self, data):
        # Inicializa los valores del objeto
        for key in self.ATRIBUTOS:
            if key in data:
                self[key] = data[key]
            else:
                self[key] = None

    def __getattr__(self, name):
            return self[name]

    def __setattr__(self, name, value):
        self[name] = value

##########################################################
##                                                      ##
##                  class EmpleadoDao                   ##
##                                                      ##
##########################################################
class EmpleadoDao(object):
    """ Capa de acceso de la tabla Empleados """

    # Insercción
    _INSERT = """
       INSERT INTO Empleados(nombre, apellidos, departamento, fechaContrato,
       puesto, nivelEducacion, sueldo, complemento)
            VALUES (UPPER(%(nombre)s), UPPER(%(apellidos)s), %(departamento)s,
            %(fechaContrato)s, %(puesto)s, %(nivelEducacion)s, %(sueldo)s,
            %(complemento)s)
    """

    # Selección por Id
    _FINDBYID = """
       SELECT idEmpleado, nombre, apellidos, departamento, fechaContrato,
       puesto, nivelEducacion, sueldo, complemento
         FROM Empleados
        WHERE idEmpleado = %(id)s
    """

    # Selección por nombre de departamento
    _FINDBYNAME = """
       SELECT idEmpleado, nombre, apellidos, departamento, fechaContrato,
       puesto, nivelEducacion, sueldo, complemento
         FROM Empleados
        WHERE UPPER(nombre) = UPPER(%(name)s)
    """

    # Selección por similitud nombre de departamento
    _FINDLIKENAME = """
       SELECT idEmpleado, nombre, apellidos, departamento, fechaContrato,
       puesto, nivelEducacion, sueldo, complemento
         FROM Empleados
         WHERE UPPER(nombre) LIKE UPPER(%(name)s)
    """

    # Actualización
    _UPDATE = """
        UPDATE Empleados
           SET nombre = UPPER(%(nombre)s), apellidos = UPPER(%(apellidos)s),
           departamento = %(departamento)s, fechaContrato = %(fechaContrato)s,
           puesto = %(puesto)s, nivelEducacion = %(nivelEducacion)s,
           sueldo = %(sueldo)s, complemento = %(complemento)s
         WHERE idEmpleado = %(idEmpleado)s
        """

    # Borrado.
    _DELETE = """
        DELETE FROM Empleados
              WHERE idEmpleado = %(id)s
       """

    def __init__(self, dbase):
        self.dbase = dbase

    ## MÉTODOS CRUD

    ## Create
    def save(self, empleado):
        """ Añade empleado en la tabla Empleados """
        self.dbase.query(self._INSERT, empleado)

    ## Read
    def findbyid(self, idd):
        """ Busca el empleado de código idd """
        result = self.dbase.query(self._FINDBYID, {'id':idd})
        if result:
            return Empleado(result[0])
        return None

    def findbyname(self, name):
        """ Busca empleados con nombre name """
        result = []
        for emp in self.dbase.query(self._FINDBYNAME, {'name':name}):
            result.append(Empleado(emp))
        return result

    def findlikename(self, name):
        """ Busca empleados con nombre %name% """
        data = '%' + name + '%'
        result = []
        for emp in self.dbase.query(self._FINDLIKENAME, {'name':data}):
            result.append(Empleado(emp))
        return result

    ## Update
    def update(self, empleado):
        """ Actualiza la fila empleado en la tabla """
        self.dbase.query(self._UPDATE, empleado)

    ## Delete
    def delete(self, idd):
        """ Borra una fila de la tabla """
        self.dbase.query(self._DELETE, {'id':idd})
