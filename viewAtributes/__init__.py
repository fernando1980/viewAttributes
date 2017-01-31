# -*- coding: utf-8 -*-
"""
/***************************************************************************
 viewAtributes
                                 A QGIS plugin
 Ver atributos de una seleccion
                             -------------------
        begin                : 2017-01-01
        copyright            : (C) 2017 by Fernando Requena
        email                : fernandorequena1980@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load viewAtributes class from file viewAtributes.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .view_Atributes import viewAtributes
    return viewAtributes(iface)
