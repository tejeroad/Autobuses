#!/usr/bin/python
# -*- coding: utf-8 -*-

from lxml import etree
from suds.client import Client
import cgi
import cgitb
cgitb.enable()
form = cgi.FieldStorage()

# # Realizamos una petición y transformamos la salida a XML 

cliente = Client("http://www.infobustussam.com:9001/services/estructura.asmx?wsdl")
cliente.set_options(retxml=True)

# Usamos el método GetRutasSublinea enviando el codigo de la linea  para obetener sus paradas

variable2 = cliente.service.GetRutasSublinea("%s" % form["paradas"].value,1)

# Creamos un fichero XML  y escribimos en él la informacion que nos devuelve el método

index = open ("/tmp/peticion2.xml","w")
index.write(variable2)
index.close()

# Creamos un HTML y realizamos un busqueda Xpath para obtener el nombre de las paradas y su codigo

arbol = etree.parse("/tmp/peticion2.xml")
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

# Enviamos a infor2.py el codigo de linea y el codigo de parada

select = etree.SubElement(form2,"select", attrib={"name":"paradas2"})
valor = etree.SubElement(form2,"input",attrib={"type":"hidden","name":"valor1","value":"%s" % form["paradas"].value})

# Bucle para crear los option de cada parada

for cont in xrange(len(paradas)):
	p.text = "Elige una parada: "
    	option = etree.SubElement(select,"option",attrib={"value":"%s" % nodos[cont]}).text = nodos[cont] + " - " + "%s" % paradas[cont]

enviar = etree.SubElement(form2,"input", attrib={"type":"submit","value":"Enviar"})

# Definimos la cabecera y mostramos por pantalla el arbol completo HTML

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers
print etree.tostring(arbol2,pretty_print=True)

