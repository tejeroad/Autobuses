#!/usr/bin/python
# -*- coding: utf-8 -*-

from lxml import etree
from suds.client import Client
import cgi
import cgitb
import pyproj
cgitb.enable()

form = cgi.FieldStorage()

cliente = Client("http://www.infobustussam.com:9001/services/dinamica.asmx?wsdl")
cliente.set_options(retxml=True)

asd2 = cliente.service.GetPasoParada("%s" % form["valor1"].value,"%s" % form["paradas2"].value,1)

index = open ("/tmp/infor.xml","w")
index.write(asd2)
index.close()

arbol = etree.parse("/tmp/infor.xml")
raiz = arbol.getroot()

minutos = arbol.xpath("/soap:Envelope/soap:Body/ns:GetPasoParadaResponse/ns:GetPasoParadaResult/ns:PasoParada/ns:e1/ns:minutos/text()",namespaces={'soap':'http://schemas.xmlsoap.org/soap/envelope/','ns':'http://tempuri.org/'})
metros = arbol.xpath("/soap:Envelope/soap:Body/ns:GetPasoParadaResponse/ns:GetPasoParadaResult/ns:PasoParada/ns:e1/ns:metros/text()",namespaces={'soap':'http://schemas.xmlsoap.org/soap/envelope/','ns':'http://tempuri.org/'})
minutos2 = arbol.xpath("/soap:Envelope/soap:Body/ns:GetPasoParadaResponse/ns:GetPasoParadaResult/ns:PasoParada/ns:e2/ns:minutos/text()",namespaces={'soap':'http://schemas.xmlsoap.org/soap/envelope/','ns':'http://tempuri.org/'})
metros2 = arbol.xpath("/soap:Envelope/soap:Body/ns:GetPasoParadaResponse/ns:GetPasoParadaResult/ns:PasoParada/ns:e2/ns:metros/text()",namespaces={'soap':'http://schemas.xmlsoap.org/soap/envelope/','ns':'http://tempuri.org/'})

x=-92.199881
y=38.56694
p1 = pyproj.Proj(init='epsg:26915')
p2 = pyproj.Proj(init='epsg:26715')
x1, y1 = p1(x,y)
longitud, latitud = pyproj.transform(p1,p2,x1,y1)

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


salida = open("/tmp/tabulado.txt","w")
#salida.write(etree.tostring(arbol2,pretty_print=True))
salida.write("%s\t" % longitud)
salida.write("%s\t" % latitud)
salida.write("%s\t" % minutos)
salida.write("%s\t" % metros)
salida.write("%s\t" % minutos2)
salida.write("%s" % metros2)
salida.close()

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers
print etree.tostring(arbol2,pretty_print=True)

