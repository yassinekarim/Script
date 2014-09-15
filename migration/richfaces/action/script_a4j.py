"""module for a4j componant migration"""
#!/usr/bin/python3
# -*-coding:utf-8 -*
from lxml import etree as ET
import os
import subprocess
class A4jElement:
    """"upgrade a4j tag"""
    a4jNs = "{http://richfaces.org/a4j}"
    hNs = "{http://java.sun.com/jsf/html}"
    uiNs = "{http://java.sun.com/jsf/facelets}"
    subviewId = 0
    def parse_src(cls, src):
        """parse the src atribute of outputStylesheet/Scipt and dived it to library and name"""
        list_str = src.split('/')
        name = list_str.pop()
        #  remove and return the last elemen of the list
        last = list_str.pop()
        library = ""
        for iterator in list_str:
            if iterator != "":
                library += iterator+"/"
        library += last
        return library, name
    parse_src = classmethod(parse_src)
    def get_web_app_path(cls, file_path):
        list_path = file_path.split("webapp/")
        relativepath = list_path[1]
        relativepath = relativepath[:relativepath.rfind("/")]
        return list_path[0]+"webapp", relativepath
    get_web_app_path = classmethod(get_web_app_path)
    def ressource_update(cls, element, file_path):
        """move the ressources to the right location and upate element"""
        src = element.get("src")
        if src.startswith("resource:///"):
            src = src.replace("resource:///", "/")
        library, name = A4jElement.parse_src(src)
        element.attrib.pop("src")
        web_app_path, relativepath = cls.get_web_app_path(file_path)
        old_path = os.getcwd()
        os.chdir(web_app_path)
        if src.startswith("/"):
            subprocess.call(["mkdir", "-p", "./resources/"+library])
            subprocess.call(["mv", "."+src, "./resources"+src])
        else:
            subprocess.call(["mkdir", "-p", "./resources/"+relativepath+"/"+library])
            subprocess.call(["mv", "./"+relativepath+"/"+src, "./resources/"+relativepath+"/"+src])
        os.chdir(old_path)
        element.set("library", library)
        name.replace(".xcss", ".ecss")
        element.set("name", name)
    ressource_update = classmethod(ressource_update)
    def componant_change(cls, element, file_path):
        """migrate a4j tag"""
        if element.tag == cls.a4jNs+"actionparam":
            element.tag = cls.a4jNs+"param"
        elif element.tag == cls.a4jNs+"form":
            element.tag = cls.hNs+"form"
        elif element.tag == cls.a4jNs+"region":
            print("self_rendered, renderRegionOnly, ajaxListener and immediate attribute are removed/not implemented")
        elif element.tag == cls.a4jNs+"AjaxListener":
            print("a4j:AjaxListener removed didn't replaced yet")
        elif element.tag == cls.a4jNs+"support":
            element.tag = cls.a4jNs+"ajax"
            onrowmouseover = element.get("onRowMouseOver")
            onclick = element.get("onclick")
            Id = element.get("id")
            if onrowmouseover or onclick or Id is not None:
                element.tag = cls.a4jNs+"commandLink"
                parent = element.getparent()
                gparent = parent.getparent()
                gparent.insert(gparent.index(parent), element)
                element.append(parent)
                element.attrib.pop("event")
            else:
                action = element.get("action") or element.get("actionListener")
                if element.get("action"):
                    element.set("listener", action)
                    element.attrib.pop("action")
                elif action:
                    element.set("listener", action)
                    element.attrib.pop("actionListener")
                onsubmit = element.get("onsubmit")
                if onsubmit is not None:
                    element.set("onbegin", onsubmit)
                    element.attrib.pop("onsubmit")
                for child in element:
                    if child.tag == "{http://java.sun.com/jsf/core}setPropertyActionListener":
                        child.tag = cls.a4jNs+"param"
                        target = child.get("target")
                        if target is not None:
                            child.set("assignTo", target)
                            child.attrib.pop("target")
        elif element.tag == cls.a4jNs+"include":
            subview = ET.Element("{http://java.sun.com/jsf/core}subview")
            subview.set("id", "subview_"+str(cls.subviewId))
            cls.subviewId += 1
            element.tag = cls.uiNs+"include"
            src = element.get("viewId")
            if src:
                element.set("src", src)
                element.attrib.pop("viewId")
            parent = element.getparent()
            parent.insert(parent.index(element), subview)
            subview.append(element)
            # parent.remove(element)
        elif element.tag == cls.a4jNs+"push":
            return
        elif element.tag == cls.a4jNs+"status":
            return
        elif element.tag == cls.a4jNs+"log":
            if element.get("popup"):
                element.set("mode", "popup")
                element.attrib.pop("popup")
        elif element.tag == cls.a4jNs+"outputPanel":
            if element.get("layout") == "none":
                element.attrib.pop("layout")
                element.set("rendered", "false")
        elif element.tag == cls.a4jNs+"loadStyle" :
            element.tag = cls.hNs+"outputStylesheet"
            A4jElement.ressource_update(element, file_path)
        elif element.tag == cls.a4jNs+"loadScript":
            element.tag = cls.hNs+"outputScript"
            A4jElement.ressource_update(element, file_path)
    componant_change = classmethod(componant_change)
