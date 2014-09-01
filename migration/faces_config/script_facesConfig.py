#!/usr/bin/python3 
# -*-coding:utf-8 -*
from lxml import etree as ET
from migration.utils.change_definition import ChangeDefinition
class FaceConfigMigration:
    
    def parseXml(cls,filePath):
        """parse the web.xml update definition and richfaces context-param"""
        parser = ET.XMLParser(remove_blank_text=True,load_dtd=True)
        tree = ET.parse(filePath,parser)
        tree=ChangeDefinition.changedefinition(tree)
        root = tree.getroot()
        for element in root:
            if(element.tag=="{http://java.sun.com/xml/ns/javaee}application"):
                view=element.find("{http://java.sun.com/xml/ns/javaee}view-handler")
                if(view is not None):
                    element.remove(view)
        tree.write(filePath,pretty_print=True,encoding='utf-8', xml_declaration=True)
    parseXml=classmethod(parseXml)
