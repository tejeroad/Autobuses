#!/usr/bin/python
# -*- coding: utf-8 -*-

from lxml import etree
from suds.client import Client
import cgi
import cgitb
from pyproj import Proj
cgitb.enable()
form = cgi.FieldStorage()

# Guardamos en paradas2 los codigos de paradas que enviamos en formulario_final.py

paradas2 = form["paradas2"].value

# Realizamos una petición para informacion estática y otra para la dinámica y transformamos la salida de ambas a XML 

cliente = Client("http://www.infobustussam.com:9001/services/dinamica.asmx?wsdl")
cliente2 = Client("http://www.infobustussam.com:9001/services/estructura.asmx?wsdl")
cliente.set_options(retxml=True)
cliente2.set_options(retxml=True)

# Usamos el método GetPasoParada enviando el codigo de la linea, codigo de parada para obetener el tiempo de llegada y los metros a los que se encuentra
# Usamos el método GetTopoSublinea enviando el codigo de la linea para obetener las X,Y de la trayectoria de las lineas

variable3 = cliente.service.GetPasoParada("%s" % form["valor1"].value,"%s" % paradas2,1)
peticion = cliente2.service.GetTopoSublinea("%s" % form["valor1"].value,1)

# Creamos un fichero XML  y escribimos en él la informacion que nos devuelve el método GetPasoParada (minutos y metros de dos lineas)

index = open("/tmp/infor.xml","w")
index.write(variable3)
index.close()
arbol = etree.parse("/tmp/infor.xml")
raiz = arbol.getroot()

# Creamos un fichero XML  y escribimos en él la informacion que nos devuelve el método GetTopoSublinea (X,Y de las rutas de las lineas)

index2 = open("/tmp/infor2.xml","w")
index2.write(peticion)
index2.close()

# Creamos un HTML y realizamos una busqueda Xpath para obtener el tiempo de llegada y la distancia

arbol3 = etree.parse("/tmp/infor2.xml")
raiz2 = arbol3.getroot()

minutos = arbol.xpath("/soap:Envelope/soap:Body/ns:GetPasoParadaResponse/ns:GetPasoParadaResult/ns:PasoParada/ns:e1/ns:minutos/text()",namespaces={'soap':'http://schemas.xmlsoap.org/soap/envelope/','ns':'http://tempuri.org/'})
metros = arbol.xpath("/soap:Envelope/soap:Body/ns:GetPasoParadaResponse/ns:GetPasoParadaResult/ns:PasoParada/ns:e1/ns:metros/text()",namespaces={'soap':'http://schemas.xmlsoap.org/soap/envelope/','ns':'http://tempuri.org/'})
minutos2 = arbol.xpath("/soap:Envelope/soap:Body/ns:GetPasoParadaResponse/ns:GetPasoParadaResult/ns:PasoParada/ns:e2/ns:minutos/text()",namespaces={'soap':'http://schemas.xmlsoap.org/soap/envelope/','ns':'http://tempuri.org/'})
metros2 = arbol.xpath("/soap:Envelope/soap:Body/ns:GetPasoParadaResponse/ns:GetPasoParadaResult/ns:PasoParada/ns:e2/ns:metros/text()",namespaces={'soap':'http://schemas.xmlsoap.org/soap/envelope/','ns':'http://tempuri.org/'})

# Realizamos otra busqueda Xpath para obtener las X,Y de las lineas

xs= arbol3.xpath("/soap:Envelope/soap:Body/ns:GetTopoSublineaResponse/ns:GetTopoSublineaResult/ns:InfoCoord/ns:x/text()",namespaces={'soap':'http://schemas.xmlsoap.org/soap/envelope/','ns':'http://tempuri.org/'})
ys = arbol3.xpath("/soap:Envelope/soap:Body/ns:GetTopoSublineaResponse/ns:GetTopoSublineaResult/ns:InfoCoord/ns:y/text()",namespaces={'soap':'http://schemas.xmlsoap.org/soap/envelope/','ns':'http://tempuri.org/'})
#xs = xs[0]
#ys = ys[0]

# Tranformamos las X,Y a float y las guardamos en una lista

xss=[]
for x in xs:
    xss.append(float(x))
yss=[]
for y in ys:
    yss.append(float(y))

html = etree.Element("html",attrib={"xmlns":"http://www.w3.org/1999/xhtml"})
arbol2 = etree.ElementTree(html)
head = etree.SubElement(html,"head")
title = etree.SubElement(head,"title")
title.text = "Formulario Tussam"
meta = etree.SubElement(head,"meta", attrib={"http-equiv":"Content-Type", "content":"text/html", "charset":"utf-8"})
body = etree.SubElement(html,"body")
p = etree.SubElement(body,"h1").text = "Primer Autobus"
p = etree.SubElement(body,"p").text = "minutos: " + "%s" % minutos
p = etree.SubElement(body,"p").text = "distancia: " + "%s" % metros
p = etree.SubElement(body,"h1").text = "Segundo Autobus"
p = etree.SubElement(body,"p").text = "minutos: " + "%s" % minutos2
p = etree.SubElement(body,"p").text = "distancia: " + "%s" % metros2
form = etree.SubElement(body,"form", attrib={"action":"maparadas.html", "method":"post"})

# Definimos la zona utm para sevilla y las transformamos a latitud y longitud

p = Proj(proj='utm',zone=30,ellps='WGS84')
valorx,valory = p(xss,yss,inverse=True)

# Creamos un fichero TXT con la información adicional para mostrar los puntos en el mapa

salida = open("/usr/lib/cgi-bin/paradas.txt","w")
salida.write("lat\tlon\ttitle\tdescription\ticonSize\tincoOffset\ticon\n")
for cont in xrange(len(valorx)):
    salida.write("%s\t" % valory[cont]) 
    salida.write("%s\t" % valorx[cont])
    salida.write("Prueba\t")
    salida.write("Punto %d\t"% cont)
    salida.write("%s\t" % "21,25")
    salida.write("%s\t" % "-10,-25")
    salida.write("autobus.gif\n")
salida.close()

mapa = etree.SubElement(form,"input", attrib={"type":"submit","value":"Mapa"})

# Definimos la cabecera y mostramos por pantalla el arbol completo HTML
# Ademas dispone de un botón "Mapa" que mostrará el recorrido de la linea seleccionada

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers
print etree.tostring(arbol2,pretty_print=True)
