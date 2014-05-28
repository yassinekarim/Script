#!/opt/python3/bin/python3 
# -*-coding:utf-8 -*
from lxml import etree as ET


class A4jElement:
    """docstring for A4jElement"""
    a4jNs="{http://richfaces.org/a4j}"
    hNs="{http://java.sun.com/jsf/html}"
    def componantChange(cls,element):
        if (element.tag== cls.a4jNs+"actionparam"):
            element.tag=cls.a4jNs+"param"
        elif (element.tag== cls.a4jNs+"form"):
            element.tag==cls.hNs+"form"
        elif (element.tag== cls.a4jNs+"region"):
            print ("selfRendered, renderRegionOnly, ajaxLsitener and immediate attribute are removed/not implemented")
        elif (element.tag== cls.a4jNs+"AjaxListener"):
            print ("a4j:AjaxListener removed didn't replaced yet")
        elif (element.tag== cls.a4jNs+"support"):
            element.tag==cls.hNs+"ajax"
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
    componantChange=classmethod(componantChange)