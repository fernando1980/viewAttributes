View Attributes

Plugin developed to show the attributes of a expropiated field stored in a shapefile.

This plugin has beeen created to show in a form, information about a field. The information is showed in a form. The information shows order's number, Cadastral Reference, Proprietary name, Phone's proprietary, Cadastral surface and expropiated surface. Also, it shows some pictures of the field.

To work properly, it is needed that the information will be stored in a shapefile with these fields:

FIELD NAME 	Description
REFCAT 		Cadastral Reference of the field
AREA 		Field surface
S_EXPRO 	Expropiated surface
N_ORDEN 	Number of the expropiated field
TIT_NOMBRE 	Propietary's name
TIT_TLF 	Propietary's telephone number
FOTON(*) 	Picture of the field (N is the number of the picture, for example FOTO1)

(*) This field stores the relative path of the image. The image must be stored in the same folder as the project file (.qgs)

BEGIN: 01/01/2017

AUTHOR: FERNANDO REQUENA

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

