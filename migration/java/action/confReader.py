#!/opt/python3/bin/python3 
# -*-coding:utf-8 -*
import os
import migration.java.model.replacement
from lxml import etree as ET

class ConfigurationReader:
    """docstring for ConfigurationReader"""
    def readAnnotation(cls,tag):
        mapping=[]
        for it in tag:
            if (it.tag=="mapping"):
                mapping.append((it.get("old"),it.get("new")))
            else:
                print ("error: children of annotation has not the tag mapping")
        return migration.java.model.replacement.AnnotationReplacement(tag.get("regex"),tag.get("replacement"),mapping)
    readAnnotation= classmethod(readAnnotation)

    def readClass(cls,tag):
        method=[]
        mapping=[]
        for it in tag:
            if (it.tag=="method"):
                method.append(it.get("regex"))
            elif(it.tag=="mapping"):
                mapping.append((it.get("old"),it.get("new")))
            else:
                print ("error: children of class has not the tag method or mapping")
        return migration.java.model.replacement.ClassReplacement(tag.get("regex"),tag.get("replacement"),method,mapping)
    readClass= classmethod(readClass)    

    def readMethod(cls,tag):
        return migration.java.model.replacement.MethodReplacement(tag.get("regex"),tag.get("replacement"),False,[])
    readMethod= classmethod(readMethod) 
    def readTag(cls,tag):
        if(tag.tag=="annotation"):
            return ConfigurationReader.readAnnotation(tag)
        elif(tag.tag=="class"):
            return ConfigurationReader.readClass(tag)
        elif(tag.tag=="method"):
            return ConfigurationReader.readMethod(tag)
    readTag= classmethod(readTag)
    def initList(cls):
        script_dir = os.path.dirname(__file__)
        replacementList=[]
        basestring = (str,bytes)
        parser = ET.XMLParser(remove_blank_text=True)
        tree = ET.parse(script_dir+"/changement_java.xml",parser)
        root = tree.getroot()
        for element in root:
            if isinstance(element.tag, basestring):
                replacementList.append(ConfigurationReader.readTag(element))
        return replacementList
    initList = classmethod(initList)
