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

asd = cliente.service.GetPasoParada("01","%s" % form["paradas2"].value,1)


index = open ("asd3.xml","w")
index.write(asd3.xml)
index.close()

arbol = etree.parse("asd3.xml")
raiz = arbol.getroot()

minutos = arbol.xpath("/soap:Envelope/soap:Body/ns:GetPasoParadaResponse/ns:GetPasoParadaResult/ns:PasoParada/ns:e1/ns:minutos/text()",namespaces={'soap':'http://schemas.xmlsoap.org/soap/envelope/','ns':'http://tempuri.org/'})
metros = arbol.xpath("/soap:Envelope/soap:Body/ns:GetPasoParadaResponse/ns:GetPasoParadaResult/ns:PasoParada/ns:e1/ns:metros/text()",namespaces={'soap':'http://schemas.xmlsoap.org/soap/envelope/','ns':'http://tempuri.org/'})


html = etree.Element("html",attrib={"xmlns":"http://www.w3.org/1999/xhtml"})
arbol2 = etree.ElementTree(html)
head = etree.SubElement(html,"head")
title = etree.SubElement(head,"title")
title.text = "Formulario Tussam"
body = etree.SubElement(html,"body")
p = etree.SubElement(body,"p")
