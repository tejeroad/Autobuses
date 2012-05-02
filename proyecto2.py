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

paradas = arbol.xpath("/soap:Envelope/soap:Body/ns:GetLineasResponse/ns:GetLineasResult/ns:InfoLinea/ns:nombre",namespaces={'soap':'http://schemas.xmlsoap.org/soap/envelope/','ns':'http://tempuri.org/'})

for i in paradas:
    print i.text



