#!/usr/local/bin/python3.4
# -*-coding:utf-8 -*
import sys
from lxml import etree as ET
basestring = (str,bytes)
if len(sys.argv) < 2:
    print("Saisissez le chemin vers le pom.xml")
    sys.exit(1)
tree = ET.parse(sys.argv[1])
root = tree.getroot()
dependencies=root.findall("xmlns:dependencies/xmlns:dependency", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
for element in dependencies:
    if isinstance(element.tag, basestring):
        if("org.richfaces." in element.find("xmlns:groupId",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text):
            element.remove()
        if("com.sun.facelets" in element.find("xmlns:groupId",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text):

# tree.write(sys.argv[1],pretty_print=True,encoding='utf-8')