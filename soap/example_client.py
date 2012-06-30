# http://graphical.weather.gov/xml/ about a quarter down the page for funcs
# http://soappy.ooz.ie/p/client_27.html

import SOAPpy
service_url ='http://graphical.weather.gov/xml/SOAP_server/ndfdXMLserver.php'
namespace = 'http://graphical.weather.gov/xml/DWMLgen/wsdl/ndfdXML.wsdl#NDFDgenByDay'
client = SOAPpy.SOAPProxy(service_url, namespace)
client.LatLonListLine(39 -77 39 -77)
#this returns some XML. Use xml.etree to parse it from there
#into your 'weather' object and save that into the DB 
