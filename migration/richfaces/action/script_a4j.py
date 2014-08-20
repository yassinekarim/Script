#!/opt/python3/bin/python3
# -*-coding:utf-8 -*
from lxml import etree as ET
import os
import subprocess

class A4jElement:
    """"upgrade a4j tag"""
    a4jNs="{http://richfaces.org/a4j}"
    hNs="{http://java.sun.com/jsf/html}"
    uiNs="{http://java.sun.com/jsf/facelets}"
    subviewId=0

    def parseSrc(cls,src):
        listStr=src.split('/')
        name=listStr.pop() #  remove and return the last elemen of the list
        last=listStr.pop()
        library=""
        for it in listStr:
            if(it!=""):
                library+=it+"/"
        library+=last
        return library,name
    parseSrc=classmethod(parseSrc)
    def getWebAppPath(cls,filePath):
        listPath=filePath.split("webapp/")
        relativePath=listPath[1]
        relativePath=relativePath[:relativePath.rfind("/")]
        return listPath[0]+"webapp",relativePath
    getWebAppPath=classmethod(getWebAppPath)
    def ressourceUpdate(cls,element,filePath):
        """move the ressources to the right location and upate element"""
        src=element.get("src")
        if (src.startswith("resource:///")):
            src=src.replace("resource:///","/")
        library,name=A4jElement.parseSrc(src)
        element.attrib.pop("src")
        webAppPath,relativePath=cls.getWebAppPath(filePath)
        oldPath = os.getcwd()
        os.chdir(webAppPath)
        if(src.startswith("/")):
            subprocess.call(["mkdir","-p","./resources/"+library])
            subprocess.call(["mv","."+src,"./resources"+src])
        else:
            subprocess.call(["mkdir","-p","./resources/"+relativePath+"/"+library])
            subprocess.call(["mv","./"+relativePath+"/"+src,"./resources/"+relativePath+"/"+src])
        os.chdir(oldPath)
        element.set("library",library)
        element.set("name",name)
    ressourceUpdate=classmethod(ressourceUpdate)
    def componantChange(cls,element,filePath):
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
            onRowMouseOver=element.get("onRowMouseOver")
            onclick=element.get("onclick")
            Id=element.get("id")
            if(onRowMouseOver or onclick or Id is not None):
                element.tag=cls.a4jNs+"commandLink"
                parent=element.getparent()
                gparent=parent.getparent()
                gparent.insert(gparent.index(parent),element)
                element.append(parent)
                element.attrib.pop("event")
            else:
                action=element.get("action") or element.get("actionListener")
                if(element.get("action")):
                    element.set("listener",action)
                    element.attrib.pop("action")
                else:
                    element.set("listener",action)
                    element.attrib.pop("actionListener")
                onsubmit=element.get("onsubmit")
                if(onsubmit is not None): 
                    element.set("onbegin",onsubmit)
                    element.attrib.pop("onsubmit")
                for child in element:
                    if(child.tag=="{http://java.sun.com/jsf/core}setPropertyActionListener"):
                        child.tag=cls.a4jNs+"param"
                        target=child.get("target")
                        if(target is not None):
                            element.set("assignTo",target)
                            element.attrib.pop("target") 
        elif (element.tag== cls.a4jNs+"include"):
            subview=ET.Element("{http://java.sun.com/jsf/core}subview")
            subview.set("id","subview_"+str(cls.subviewId))
            cls.subviewId+=1
            element.tag=cls.uiNs+"include"
            src=element.get("viewId")
            if(src):
                element.set("src",src)
                element.attrib.pop("viewId") 
            parent=element.getparent()
            parent.insert(parent.index(element),subview)
            subview.append(element)
            # parent.remove(element)
        elif (element.tag== cls.a4jNs+"push"):
            pass
        elif (element.tag== cls.a4jNs+"status"):
            pass
        elif (element.tag== cls.a4jNs+"log"):
            if(element.get("popup")):
                element.set("mode","popup")
                element.attrib.pop("popup")
        elif (element.tag== cls.a4jNs+"outputPanel"):
            if(element.get("layout")=="none"):
                element.attrib.pop(layout)
                element.set("rendered","false")
        elif(element.tag== cls.a4jNs+"loadStyle" ):
            element.tag=cls.hNs+"outputStylesheet"
            A4jElement.ressourceUpdate(element,filePath)
        elif(element.tag== cls.a4jNs+"loadScript"):
            element.tag=cls.hNs+"outputScript"
            A4jElement.ressourceUpdate(element,filePath)
        return element
    componantChange=classmethod(componantChange)