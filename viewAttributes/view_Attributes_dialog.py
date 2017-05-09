# -*- coding: utf-8 -*-
"""
/***************************************************************************
 viewAttributesDialog
                                 A QGIS plugin
 Show attributes of a field selected stored in a shapefile.
                             -------------------
        begin                : 2017-05-08
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Fernando Requena
        email                : fernandorequena1980@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic, QtCore

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'view_Attributes_dialog_base.ui'))


class viewAttributesDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(viewAttributesDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        #stay on top always
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint |QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.CustomizeWindowHint)

