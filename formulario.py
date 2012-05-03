# -*- coding: utf-8 -*-
from lxml import etree
from suds.client import Client

cliente = Client("http://www.infobustussam.com:9001/services/estructura.asmx?wsdl")
cliente.set_options(retxml=True)

asd = cliente.service.GetLineas()

index = open ("prueba.xml","w")
index.write(asd)
index.close()

arbol = etree.parse("prueba.xml")
raiz = arbol.getroot()

paradas = arbol.xpath("/soap:Envelope/soap:Body/ns:GetLineasResponse/ns:GetLineasResult/ns:InfoLinea/ns:nombre/text()",namespaces={'soap':'http://schemas.xmlsoap.org/soap/envelope/','ns':'http://tempuri.org/'})
codigo = arbol.xpath("/soap:Envelope/soap:Body/ns:GetLineasResponse/ns:GetLineasResult/ns:InfoLinea/ns:label/text()",namespaces={'soap':'http://schemas.xmlsoap.org/soap/envelope/','ns':'http://tempuri.org/'})

#!/usr/bin/python
import cgi
import cgitb
cgitb.enable()

html = etree.Element("html",attrib={"xmlns":"http://www.w3.org/1999/xhtml"})
arbol2 = etree.ElementTree(html)
head = etree.SubElement(html,"head")
title = etree.SubElement(head,"title")
title.text = "Formulario Tussam"
meta = etree.SubElement(head,"meta", attrib={"http-equiv":"Content-Type", "content":"text/html", "charset":"utf-8"})
body = etree.SubElement(html,"body")
form = etree.SubElement(body,"form", attrib={"action":"", "method":"post"})
select = etree.SubElement(body,"select", attrib={"name":"paradas"})
    
for label in codigo:
    option = etree.SubElement(select,"option", attrib={"value":"%s" % label})

for lineas in paradas:
    option.text = lineas
    
salida = open("formularioParadas.html","w")
salida.write(etree.tostring(arbol2,pretty_print=True))
