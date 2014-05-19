#!/usr/local/bin/python3.4
# -*-coding:utf-8 -*
import sys
import re
from lxml import etree as ET
basestring = (str,bytes)
if len(sys.argv) < 2:
    print("Saisissez le chemin vers web.xml ou persistence.xml")
    sys.exit(1)
def newXml(element):
    child=list(element)
    if(not child):
        element.tag=element.tag.replace("http://jboss.com/products/seam/","http://jboss.org/schema/seam/")

    else:
        for el in child:
            newXml(el)    
        element.tag=element.tag.replace("http://jboss.com/products/seam/","http://jboss.org/schema/seam/")
def convert(namespace):
    if re.match("http://jboss.com/products/seam/*", namespace):       
        return namespace.replace("http://jboss.com/products/seam/","http://jboss.org/schema/seam/")
    elif("http://www.w3.org/2001/XMLSchema-instance"==namespace):
        return namespace
    else:
        print("erreur namespace")
def changeDefSeam(page):
    COMPONENT_NAMESPACE = "http://jboss.org/schema/seam/"+page
    COMPONENT = "{%s}" % COMPONENT_NAMESPACE
    NSMAP = {None : COMPONENT_NAMESPACE} 
    for key in root.nsmap.keys():
        NSMAP[key]=convert(root.nsmap[key])
    newRoot = ET.Element(COMPONENT + "components", nsmap=NSMAP)
    newRoot.set('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation',root.get('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation').replace("http://jboss.com/products/seam/","http://jboss.org/schema/seam/").replace("2.2","2.3"))
    newXml(root)
    newRoot.text=root.text
    for element in root:
        newRoot.append(element)
    tree._setroot(newRoot)
parser = ET.XMLParser(remove_blank_text=True)
tree = ET.parse(sys.argv[1],parser)
root = tree.getroot()
if( "{http://java.sun.com/xml/ns/javaee}web-app" == root.tag  ):
    root.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation","http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_3_0.xsd")
    root.set("version","3.0")
elif ( "{http://jboss.com/products/seam/components}components" == root.tag ):
    changeDefSeam("components")
elif (  root.tag=="{http://jboss.com/products/seam/pages}pages" ):
    changeDefSeam("pages")
elif ( "{http://java.sun.com/xml/ns/persistence}persistence" == root.tag  ):
    root.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation","http://java.sun.com/xml/ns/persistence http://java.sun.com/xml/ns/persistence/persistence_2_0.xsd")
    root.set("version","2.0")
elif ( "{http://java.sun.com/xml/ns/javaee}faces-config" == root.tag  ):
    root.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation","http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-facesconfig_2_1.xsd")
    root.set("version","2.1")
tree.write(sys.argv[1],pretty_print=True,encoding='utf-8')
