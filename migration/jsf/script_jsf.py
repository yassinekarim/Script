#!/opt/python3/bin/python3 
# -*-coding:utf-8 -*
from lxml import etree as ET
class XhtmlTransformation:
    """docstring for XhtmlTransformation"""
    def newXhtml(element):
        child=list(element)
        if(not child):
            element.tag=element.tag.replace("http://richfaces.ajax4jsf.org/rich","http://richfaces.org/rich")
        else:
            for el in child:
                newXml(el)    
            element.tag=element.tag.replace("http://richfaces.ajax4jsf.org/rich","http://richfaces.org/rich")
    def isRich(tag):
        if ("http://richfaces.org/rich" in tag):
            return True
        else:
            return False
    def isA4J(tag):
        if ("http://richfaces.org/a4j" in tag):
            return True
        else:
            return False
    def commonAttributeChange(element):
        for key, value in element.attrib.items():
            if (key=="reRender")):
                element.set("render",value)
                element.attrib.pop("reRender")
            elif(key=="ajaxSingle")):
                if(value=="true"):
                    element.set("execute","@this")
                element.attrib.pop("ajaxSingle")
            elif (key=="limitToList")):
                element.set("limitRender",value)
                element.attrib.pop("limitToList")
            elif(key in ["ignoreDupResponse","requestDelay","timeout"):
                child = ET.Element("{http://richfaces.org/a4j}attachQueue")
                child.set(key,value)
                element.append(child)
            elif(key=="process"):
                element.set("execute",value)
                element.attrib.pop("process")

    def changeNsmap(tree,key):
        root=tree.getroot()
        NSMAP=root.nsmap
        NSMAP[key]="http://richfaces.org/rich"
        newRoot = ET.Element(root.tag, nsmap=NSMAP)
        newRoot.attrib=root.attrib
        newXml(root)
        newRoot.text=root.text
        for element in root:
            newRoot.append(element)
        tree._setroot(newRoot)

    def upgrade(cls, tree):
        root=tree.getroot()
        inv_nsmap = {root.nsmap[k] : k for k in root.nsmap}
        if(inv_nsmap.get("http://richfaces.ajax4jsf.org/rich")!=None ):
            tree=changeNsmap(tree,inv_nsmap.get("http://richfaces.ajax4jsf.org/rich"))
            root=tree.getroot
        for element in root.iter():
            if(element.tag=="{http://www.w3.org/1999/xhtml}body"):
                element.tag="{http://java.sun.com/jsf/html}body"  #change <body> to <h:body> 
            elif(element.tag=="{http://www.w3.org/1999/xhtml}head"):
                element.tag="{http://java.sun.com/jsf/html}head"
            elif(isRich(element.tag)):
                commonAttributeChange(element)
                componantChange(element)
            elif(isA4J(element.tag)):
                commonAttributeChange(element)
                componantChange(element)
        return tree
    upgrade=classmethod(upgrade)
        
