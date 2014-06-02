#!/opt/python3/bin/python3 
# -*-coding:utf-8 -*
import os
import glob
import sys
from migration.java.action.confReader import ConfigurationReader
from migration.java.action.script_java import JavaTransformation 
from migration.jsf.script_jsf import XhtmlTransformation
from migration.persistence.script_persistence import PersistenceMigration
from migration.web.script_web import WebMigration
from migration.components.action.script_component import ComponentsMigration
from migration.pom.action.script_pom import PomMigration
from lxml import etree as ET
from migration.utils.change_definition import ChangeDefinition

   
size = len(sys.argv)
if size == 1 or size > 2:
    print ("Usage: script_java.py project_folder")
    sys.exit(1)
inputPath = sys.argv[1]
if not os.path.exists(inputPath):
    print (inputPath+" does not exist on disk")
    sys.exit(1)
if not os.path.isdir(inputPath):
    print (inputPath+" isn't a dir")
    sys.exit(1)


def changeDefinition(filePath):
    parser = ET.XMLParser(remove_blank_text=True)
    tree = ET.parse(filePath,parser)
    tree=ChangeDefinition.changedefinition(tree)
    root = tree.getroot()
    tree.write(filePath,pretty_print=True,encoding='utf-8')

JavaTransformation.replacementList=ConfigurationReader.initList()
for path, dirs, files in os.walk(inputPath):
    for filepath in [ os.path.join(path, f) for f in files]:
        if not "target" in filepath:
            if(filepath.endswith(".java") ):
               JavaTransformation.parseJava(filepath)
            elif(filepath.endswith(".xhtml")):
                XhtmlTransformation.upgrade(filepath)
            elif(filepath.endswith("persistence.xml")):
                PersistenceMigration.parseXml(filepath)
            elif(filepath.endswith("components.xml")):
                ComponentsMigration.parseXml(filepath)
            elif(filepath.endswith("web.xml")):
                WebMigration.parseXml(filepath)
            elif(filepath.endswith("pom.xml")):
                PomMigration.parseXml(filepath) 
            elif(filepath.endswith("faces-config.xml")):
                changeDefinition(filepath)
            elif(filepath.endswith("pages.xml")):
                changeDefinition(filepath)
ComponentsMigration.addComponents(inputPath)