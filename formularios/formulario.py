#!/usr/bin/python
# -*- coding: utf-8 -*-

from lxml import etree
from suds.client import Client
import cgi
import cgitb
cgitb.enable()

cliente = Client("http://www.infobustussam.com:9001/services/estructura.asmx?wsdl")
cliente.set_options(retxml=True)

asd = cliente.service.GetLineas()

index = open ("/tmp/prueba.xml","w")
index.write(asd)
index.close()

arbol = etree.parse("/tmp/prueba.xml")
raiz = arbol.getroot()

lineas_nombre = arbol.xpath("/soap:Envelope/soap:Body/ns:GetLineasResponse/ns:GetLineasResult/ns:InfoLinea/ns:nombre/text()",namespaces={'soap':'http://schemas.xmlsoap.org/soap/envelope/','ns':'http://tempuri.org/'})
lineas_value = arbol.xpath("/soap:Envelope/soap:Body/ns:GetLineasResponse/ns:GetLineasResult/ns:InfoLinea/ns:label/text()",namespaces={'soap':'http://schemas.xmlsoap.org/soap/envelope/','ns':'http://tempuri.org/'})

html = etree.Element("html",attrib={"xmlns":"http://www.w3.org/1999/xhtml"})
arbol2 = etree.ElementTree(html)
head = etree.SubElement(html,"head")
title = etree.SubElement(head,"title")
title.text = "Formulario Tussam"
meta = etree.SubElement(head,"meta", attrib={"http-equiv":"Content-Type", "content":"text/html", "charset":"utf-8"})
body = etree.SubElement(html,"body")
p = etree.SubElement(body,"p")
form = etree.SubElement(body,"form", attrib={"action":"formulario_final.py", "method":"post"})
select = etree.SubElement(body,"select", attrib={"name":"paradas"})

for cont in xrange(len(lineas_nombre)):
    p.text = "Elige una Linea: "
    option2 = etree.SubElement(select,"option",attrib={"value":"%s" % lineas_value[cont]}).text = lineas_value[cont] + " - " + '%s' % lineas_nombre[cont]

enviar = etree.SubElement(body,"input", attrib={"type":"submit","value":"Enviar"})
    
#salida = open("formularioParadas.html","w")
#salida.write(etree.tostring(arbol2,pretty_print=True))

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers
print etree.tostring(arbol2,pretty_print=True)

####Formulario.py y formulario_final.py hay que meterlo dentro de /usr/lib/cgi-bin/
