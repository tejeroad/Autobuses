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

    