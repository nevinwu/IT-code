#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
database.py

Contiene la clase Database utilizada para el acceso a Bases de Datos
relacionales. Tomado de los apuntes del profesor Wladimiro Díaz.

Autor: Francisco Martínez Picó
Versión: 1.0
Fecha: 21/03/2020
"""
import MySQLdb
import logging

##########################################################
##                                                      ##
##                   class Database                     ##
##                                                      ##
##########################################################
class Database(object):
    """ Conector a la base de datos """
    # Inicializa el logger
    logger = logging.getLogger('Database')
    # Logger es un singleton, así que sólo le vamos a añadir un handler
    if not len(logger.handlers):
        logger.setLevel(logging.DEBUG)
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # add formatter to ch
        ch.setFormatter(formatter)
        # add ch to logger
        logger.addHandler(ch)

    def __init__(self, host, user, passwd, db, autocommit = True):
        try:
            self.autocommit = autocommit
            self.connection = MySQLdb.connect(
                host = host,
                user = user,
                passwd = passwd,
                db = db,
                charset = "utf8",
                use_unicode = True
                )

        except MySQLdb.Error as e:
            error = 'Mysql connection error %5d: %s' % (e.args)
            self.logger.error(error)
            raise

    def query(self, query, data = None):
        try:
            cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query, data)

        except MySQLdb.Error as e:
            error = 'Mysql query error %5d: %s' % (e.args)
            self.logger.error(error)
            self.connection.rollback()
            result = None

        else:
            result = cursor.fetchall()
            if self.autocommit:
                self.connection.commit()
        finally:
            cursor.close()
            return result

    def docommit(self):
        if not self.autocommit:
            self.connection.commit()

    def __del__(self):
        if 'connection' in locals():
            self.connection.close()
