from SOAPpy import WSDL
WSDLFile = "http://www.infobustussam.com:9001/services/estructura.asmx?wsdl"
proxy = WSDL.Proxy(WSDLFile)
asd = proxy.GetLineas()
print asd

