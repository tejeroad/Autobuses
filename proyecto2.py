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

paradas = arbol.xpath("//soap:Envelope/soap:Body/ns:GetLineasResponse/ns:GetLineasResult/ns:InfoLinea/ns:nombre")

for i in paradas:
    print i.text



