#!/usr/bin/python
# -*- coding: utf-8 -*-

from lxml import etree
from suds.client import Client
import cgi
import cgitb
cgitb.enable()

form = cgi.FieldStorage()

cliente = Client("http://www.infobustussam.com:9001/services/estructura.asmx?wsdl")
cliente.set_options(retxml=True)

asd = cliente.service.GetRutasSublinea("%s" % form["paradas"].value,1)

index = open ("/tmp/asd2.xml","w")
index.write(asd)
index.close()

arbol = etree.parse("/tmp/asd2.xml")
raiz = arbol.getroot()

paradas = arbol.xpath("//soap:Envelope/soap:Body/ns:GetRutasSublineaResponse/ns:GetRutasSublineaResult/ns:InfoRuta/ns:secciones/ns:InfoSeccion/ns:nodos/ns:InfoNodoSeccion/ns:nombre/text()",namespaces={'soap':'http://schemas.xmlsoap.org/soap/envelope/','ns':'http://tempuri.org/'})

nodos = arbol.xpath("//soap:Envelope/soap:Body/ns:GetRutasSublineaResponse/ns:GetRutasSublineaResult/ns:InfoRuta/ns:secciones/ns:InfoSeccion/ns:nodos/ns:InfoNodoSeccion/ns:nodo/text()",namespaces={'soap':'http://schemas.xmlsoap.org/soap/envelope/','ns':'http://tempuri.org/'})

html = etree.Element("html",attrib={"xmlns":"http://www.w3.org/1999/xhtml"})
arbol2 = etree.ElementTree(html)
head = etree.SubElement(html,"head")
title = etree.SubElement(head,"title")
title.text = "Formulario Tussam"
meta = etree.SubElement(head,"meta", attrib={"http-equiv":"Content-Type", "content":"text/html", "charset":"utf-8"})
body = etree.SubElement(html,"body")
p = etree.SubElement(body,"p")
form2 = etree.SubElement(body,"form", attrib={"action":"infor2.py", "method":"post"})
select = etree.SubElement(form2,"select", attrib={"name":"paradas2"})
valor = etree.SubElement(form2,"input",attrib={"type":"hidden","name":"valor1","value":"%s" % form["paradas"].value})
cont_paradas = 1
for cont in xrange(len(paradas)):
	p.text = "Elige una parada: "
    	option = etree.SubElement(select,"option",attrib={"value":"%s,%d" % (nodos[cont],cont_paradas)}).text = nodos[cont] + " - " + "%s" % paradas[cont]
	cont_paradas = cont_paradas + 1
#salida = open("/tmp/paradas.html","w")
#salida.write(etree.tostring(arbol2,pretty_print=True))

enviar = etree.SubElement(form2,"input", attrib={"type":"submit","value":"Enviar"})

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers
print etree.tostring(arbol2,pretty_print=True)

