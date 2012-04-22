from suds.client import Client

cliente = Client("http://www.infobustussam.com:9001/services/estructura.asmx?wsdl")

asd = cliente.service.GetLineas()
index = open ("prueba.xml","w")
index.write("%s" % asd)
index.close()

f = open("prueba.xml","r")

for i in f:
    if i.find("nombre") >= 0:
        nuevo = i.replace(" ","")
        print nuevo[8:-2]

