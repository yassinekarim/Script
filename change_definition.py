#!/usr/local/bin/python3.4
# -*-coding:utf-8 -*
import sys
from lxml import etree as ET
basestring = (str,bytes)
if len(sys.argv) < 2:
    print("Saisissez le chemin vers web.xml ou persistence.xml")
    sys.exit(1)
tree = ET.parse(sys.argv[1])
root = tree.getroot()
print(root.tag)
if( "{http://java.sun.com/xml/ns/javaee}web-app" == root.tag  ):
    root.atribs.pop("key")
    root.set("{http://java.sun.com/xml/ns/javaee}xsi","http://www.w3.org/2001/XMLSchema-instance")
    root.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation","http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_3_0.xsd")
    root.set("version","3.0")
tree.write(sys.argv[1],pretty_print=True,encoding='utf-8')