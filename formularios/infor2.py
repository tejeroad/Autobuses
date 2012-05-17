#!/usr/bin/python
# -*- coding: utf-8 -*-

from lxml import etree
from suds.client import Client
import cgi
import cgitb
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

html = etree.Element("html",attrib={"xmlns":"http://www.w3.org/1999/xhtml"})
arbol2 = etree.ElementTree(html)
head = etree.SubElement(html,"head")
title = etree.SubElement(head,"title")
title.text = "Formulario Tussam"
meta = etree.SubElement(head,"meta", attrib={"http-equiv":"Content-Type", "content":"text/html", "charset":"utf-8"})
body = etree.SubElement(html,"body")
p = etree.SubElement(body,"p").text = "minutos: " + "%s" % minutos
p = etree.SubElement(body,"p").text = "distancia: " + "%s" % metros



#salida = open("paradas.html","w")
#salida.write(etree.tostring(arbol2,pretty_print=True))


print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers
print etree.tostring(arbol2,pretty_print=True)

