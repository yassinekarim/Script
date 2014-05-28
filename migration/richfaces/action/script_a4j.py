#!/opt/python3/bin/python3 
# -*-coding:utf-8 -*
from lxml import etree as ET


class A4jElement:
    """"upgrade a4j tag"""
    a4jNs="{http://richfaces.org/a4j}"
    hNs="{http://java.sun.com/jsf/html}"
    def parseSrc(cls,src):
        listStr=src=split('/')
        name=listStr.pop() #  remove and return the last elemen of the list
        last=listStr.pop()
        library=""
        for it in listStr:
            library+=it+"/"
        library+=last
        return library,name
    parseSrc=classmethod(parseSrc)
    def ressourceUpdate(cls,element):
        """move the ressources to the right location and upate element"""
        src=element.get("src")
        library,name=A4jElement.parseSrc(src)
        element.attrib.pop("src")
        element.set("library",library)
        element.set("name",name)
    ressourceUpdate=classmethod(ressourceUpdate)
    def componantChange(cls,element):
        """migrate a4j tag"""
        if (element.tag== cls.a4jNs+"actionparam"):
            element.tag=cls.a4jNs+"param"
        elif (element.tag== cls.a4jNs+"form"):
            element.tag=cls.hNs+"form"
        elif (element.tag== cls.a4jNs+"region"):
            print ("selfRendered, renderRegionOnly, ajaxListener and immediate attribute are removed/not implemented")
        elif (element.tag== cls.a4jNs+"AjaxListener"):
            print ("a4j:AjaxListener removed didn't replaced yet")
        elif (element.tag== cls.a4jNs+"support"):
            element.tag=cls.a4jNs+"ajax"
        elif (element.tag== cls.a4jNs+"push"):
            print ("a4j:push not supported yet")
        elif (element.tag== cls.a4jNs+"status"):
            print ("a4j:staus upgrade not yet implemented")
        elif (element.tag== cls.a4jNs+"log"):
            if(element.get("popup")):
                element.set("mode","popup")
                element.attrib.pop("popup")
                print ("popup attribute renamed to mode")
        elif (element.tag== cls.a4jNs+"outputPanel"):
            if(element.get("layout")=="none"):
                element.attrib.pop(layout)
                element.set("rendered","false")
        elif(element.tag== cls.a4jNs+"loadStyle" ):
            element.tag=hNs+"outputStylesheet"
            A4jElement.ressourceUpdate(element)
        elif(element.tag== cls.a4jNs+"loadScript"):
            element.tag=hNs+"outputScript"
            A4jElement.ressourceUpdate(element)
        return element
    componantChange=classmethod(componantChange)