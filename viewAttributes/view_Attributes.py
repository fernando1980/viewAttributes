# -*- coding: utf-8 -*-
"""
/***************************************************************************
 viewAttributes
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
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from PIL import Image
import PIL.Image
import ImageQt
import ImageEnhance
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from view_Attributes_dialog import viewAttributesDialog
import os.path
from qgis.utils import reloadPlugin


class viewAttributes:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'viewAttributes_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&View Attributes')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'viewAttributes')
        self.toolbar.setObjectName(u'viewAttributes')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('viewAttributes', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = viewAttributesDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/viewAttributes/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Ver atributos de una seleccion'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&View Attributes'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        self.dlg.pB_exit.clicked.connect(self.exit)
        # Access to the next and previous photo buttons
        self.dlg.pB_sig.clicked.connect(self.fotoSig)
        self.dlg.pB_ant.clicked.connect(self.fotoAnt)
        # Access to the entity select button
        self.dlg.bt_selectParcel.clicked.connect(self.selectParcel)
        layers = self.iface.legendInterface().layers()
        layer_list = []
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == 2:
                layer_list.append(layer.name())
        self.dlg.cb_listLayers.addItems(layer_list)
        elem = len(layer_list)
        if (elem == 0):
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Debes cargar una capa poligonal para su uso.")
            msgBox.exec_()
        else:
            self.dlg.bt_selectParcel.setEnabled(True)
            # show the dialog
            self.dlg.show()
            # Run the dialog event loop
            result = self.dlg.exec_()
            # See if OK was pressed
            if result:
                # Do something useful here - delete the line containing pass and
                # substitute with your code.
                pass
    
    @QtCore.pyqtSlot() # signal with no arguments
    def selectParcel(self):
        # Selected layer name
        selectedLayer = self.dlg.cb_listLayers.currentText()
        # Access to the selected layer
        sLayer = QgsMapLayerRegistry.instance().mapLayersByName(selectedLayer)[0]
        self.iface.setActiveLayer(sLayer)
        activeLayer = self.iface.activeLayer()
        self.iface.mapCanvas().selectionChanged.connect(self.actuaLiza)
        # Change cursor appearance
        # cursor = QCursor()
        # cursor.setShape(Qt.WhatsThisCursor)
        # qgis.utils.iface.mapCanvas().setCursor(cursor)
        # QApplication.instance().setOverrideCursor(cursor)
        self.iface.actionSelect().trigger()

    def actuaLiza(self):
        try:
            layer = self.iface.activeLayer()
            selected_feature = layer.selectedFeatures()[0]
            refCat = selected_feature["REFCAT"]
            self.dlg.tb_refCat.setText(refCat)
            supParce = str(selected_feature["AREA"])
            self.dlg.tb_supPar.setText(supParce)
            supExpro = str(selected_feature["S_EXPRO"])
            self.dlg.tb_supExpro.setText(supExpro)
            norden = str(selected_feature["N_ORDEN"])
            self.dlg.tb_norden.setText(norden)
            tit_nombre = str(selected_feature["TIT_NOMBRE"].encode('ISO-8859-1'))
            self.dlg.tb_titnombre.setText(tit_nombre)
            tit_tlf = str(selected_feature["TIT_TLF"])
            self.dlg.tb_tittlf.setText(tit_tlf)
            fotoField = self.dlg.fotoField
            fotoField.setScaledContents(True)
            myfilepath = self.iface.activeLayer().dataProvider().dataSourceUri()
            myprojectpath = QgsProject.instance().homePath()
            (dirPath, nameFile) = os.path.split(myfilepath)
            foto = str(selected_feature["FOTO1"])
            foto_str = foto[1:]
            #fotoPath = dirPath + foto
            fotoPath = myprojectpath + foto_str
            # Load the image
            fotoField.setPixmap(QPixmap(fotoPath))
            global nFoto
            nFoto = 1
            global Foto
            Foto = "FOTO" + str(nFoto)
            if foto != "NULL":
                self.dlg.pB_sig.setEnabled(True)
                self.dlg.pB_ant.setEnabled(True)
                self.dlg.tb_foTo.setText(Foto)
            else:
                self.dlg.pB_sig.setEnabled(False)
                self.dlg.pB_ant.setEnabled(False)
                self.dlg.tb_foTo.setText("")
        except:
            #reloadPlugin('viewAtributes')
            global nFoto
            nFoto = 1
            #msgBox = QtGui.QMessageBox()
            #msgBox.setText("Debes seleccionar una parcela.")
            #msgBox.exec_()
    
    def fotoSig(self):
        global nFoto
        nFoto = nFoto + 1
        #global Foto
        Foto = "FOTO" + str(nFoto)
        layer = self.iface.activeLayer()
        selected_feature = layer.selectedFeatures()[0]
        myfilepath= self.iface.activeLayer().dataProvider().dataSourceUri()
        myprojectpath = QgsProject.instance().homePath()
        (dirPath,nameFile) = os.path.split(myfilepath)
        foto = str(selected_feature[Foto])
        foto_str = foto[1:]
        if foto != "NULL":
            self.dlg.tb_foTo.setText(Foto)
            fotoPath = myprojectpath + foto_str
            fotoField = self.dlg.fotoField
            fotoField.setScaledContents(True)
            # Load the image
            fotoField.setPixmap(QPixmap(fotoPath))
        else:
            nFoto = nFoto - 1
    
    @QtCore.pyqtSlot() # signal with no arguments
    def fotoAnt(self):
        global nFoto
        if (nFoto > 1):
            nFoto = nFoto - 1
            #global Foto
            Foto = "FOTO" + str(nFoto)
            self.dlg.tb_foTo.setText(Foto)

            layer = self.iface.activeLayer()
            selected_feature = layer.selectedFeatures()[0]
            myfilepath= self.iface.activeLayer().dataProvider().dataSourceUri()
            myprojectpath = QgsProject.instance().homePath()
            (dirPath,nameFile) = os.path.split(myfilepath)

            fotoField = self.dlg.fotoField
            fotoField.setScaledContents(True)
            foto = str(selected_feature[Foto])
            foto_str = foto[1:]
            fotoPath = myprojectpath + foto_str
            # Load the image
            fotoField.setPixmap(QPixmap(fotoPath))

    def exit(self):
        try:
            #         global nFoto
            #         nFoto = 1
            #         self.dlg.fotoField.setPixmap(QPixmap(""))
            #         self.dlg.tb_refCat.setText("")
            #         self.dlg.tb_supPar.setText("")
            #         self.dlg.tb_supExpro.setText("")
            #         self.dlg.tb_foTo.setText("")
            #         self.dlg.cb_listLayers.clear()
            mc = self.iface.mapCanvas()
            layer = self.iface.activeLayer()
            layer.removeSelection()
            mc.refresh()
            reloadPlugin('viewAttributes')
            self.dlg.close()
        except:
            reloadPlugin('viewAttributes')
            self.dlg.close()
