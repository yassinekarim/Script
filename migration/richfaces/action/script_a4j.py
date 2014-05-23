#!/opt/python3/bin/python3 
# -*-coding:utf-8 -*
from lxml import etree as ET

a4jNs="{http://richfaces.org/a4j}"
hNS="{http://java.sun.com/jsf/html}"
def a4jComponantChange(element):
    if (element.tag== a4jNs+"actionparam"):
        element.tag=a4jNs+"param"
    elif (element.tag== a4jNs+"form"):
        element.tag==hNs+"form"
    elif (element.tag== a4jNs+"region"):
        print ("selfRendered, renderRegionOnly, ajaxLsitener and immediate attribute are removed/not implemented")
    elif (element.tag== a4jNs+"AjaxListener"):
        print ("a4j:AjaxListener removed didn't replaced yet")
    elif (element.tag== a4jNs+"support"):
        element.tag==hNs+"ajax"
    elif (element.tag== a4jNs+"push"):
        print ("a4j:push not supported yet")
    elif (element.tag== a4jNs+"status"):
        print ("a4j:staus upgrade not yet implemented")
    elif (element.tag== a4jNs+"log"):
        if(element.get("popup"):
            element.set("mode","popup")
            element.attrib.pop("popup")
            print ("popup attribute renamed to mode")
    elif (element.tag== a4jNs+"outputPanel"):
        if(element.get("layout")=="none"):
            element.attrib.pop(layout)
            element.set("rendered","false")

