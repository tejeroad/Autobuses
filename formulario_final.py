#!/usr/bin/python
# -*- coding: utf-8 -*-

from lxml import etree
from suds.client import Client
import cgi
import cgitb
cgitb.enable()

form = cgi.FieldStorage()

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers
if "paradas" not in form:
    print "<H1>Error</H1>"
    print "Debes elegir una parada"
else:
    print "<p>Parada:", form["paradas"].value

cliente = Client("http://www.infobustussam.com:9001/services/estructura.asmx?wsdl")
cliente.set_options(retxml=True)

asd = cliente.service.GetRutasSublinea("%s" % form["paradas"].value,1)

index = open ("asd2.xml","w")
index.write(asd)
index.close()

arbol = etree.parse("asd2.xml")
raiz = arbol.getroot()

paradas = arbol.xpath("//soap:Envelope/soap:Body/ns:GetRutasSublineaResponse/ns:GetRutasSublineaResult/ns:InfoRuta/ns:secciones/ns:InfoSeccion/ns:nodos/ns:InfoNodoSeccion/ns:nombre/text()",namespaces={'soap':'http://schemas.xmlsoap.org/soap/envelope/','ns':'http://tempuri.org/'})

html = etree.Element("html",attrib={"xmlns":"http://www.w3.org/1999/xhtml"})
arbol2 = etree.ElementTree(html)
head = etree.SubElement(html,"head")
title = etree.SubElement(head,"title")
title.text = "Formulario Tussam"
meta = etree.SubElement(head,"meta", attrib={"http-equiv":"Content-Type", "content":"text/html", "charset":"utf-8"})
body = etree.SubElement(html,"body")
form = etree.SubElement(body,"form", attrib={"action":"", "method":"post"})
select = etree.SubElement(body,"select", attrib={"name":"paradas"})

for linea in paradas:
    option = etree.SubElement(select,"option").text = "%s" % linea

salida = open("paradas.html","w")
salida.write(etree.tostring(arbol2,pretty_print=True))

enviar = etree.SubElement(body,"input", attrib={"type":"submit","value":"Enviar"})