#!/opt/python3/bin/python3 
# -*-coding:utf-8 -*
import os
from migration.java.action.script_java import JavaTransformation 
from migration.jsf.script_jsf import XhtmlTransformation
from migration.persistence.script_persistence import PersistenceMigration
from migration.web.script_web import WebMigration
from migration.components.action.script_component import ComponentsMigration
from migration.pom.action.script_pom import PomMigration
from lxml import etree as ET
from migration.utils.change_definition import ChangeDefinition

   

class Main:
    """docstring for Main"""

        
    def changeDefinition(cls,filePath):
        parser = ET.XMLParser(remove_blank_text=True)
        tree = ET.parse(filePath,parser)
        tree=ChangeDefinition.changedefinition(tree)
        root = tree.getroot()
        tree.write(filePath,pretty_print=True,encoding='utf-8')
    changeDefinition=classmethod(changeDefinition)

    def walk(cls,inputPath):
        isEar=False
        for path, dirs, files in os.walk(inputPath):
            for filepath in [ os.path.join(path, f) for f in files]:
                if not "target" in filepath:
                    if not "GazelleTag" in filepath:
                        # if(filepath.endswith(".java") ):
                        #     JavaTransformation.parseJava(filepath)
                        # el
                        if(filepath.endswith(".xhtml")):
                            XhtmlTransformation.upgrade(filepath)
                        # elif(filepath.endswith("persistence.xml")):
                        #     PersistenceMigration.parseXml(filepath)
                        # elif(filepath.endswith("components.xml")):
                        #     ComponentsMigration.parseXml(filepath)
                        # elif(filepath.endswith("web.xml")):
                        #     WebMigration.parseXml(filepath)
                        # elif(filepath.endswith("pom.xml")):
                        #     tmp=PomMigration.parseXml(filepath)
                        #     isEar=isEar or tmp 
                        # elif(filepath.endswith("faces-config.xml")):
                        #     Main.changeDefinition(filepath)
                        # elif(filepath.endswith("pages.xml")):
                        #     Main.changeDefinition(filepath)
        if(isEar):
            ComponentsMigration.addComponents(inputPath)
    walk=classmethod(walk)