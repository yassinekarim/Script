#!/opt/python3/bin/python3 
# -*-coding:utf-8 -*
import os
import subprocess
from migration.java.action.script_java import JavaTransformation 
from migration.jsf.script_jsf import XhtmlTransformation
from migration.persistence.script_persistence import PersistenceMigration
from migration.web.script_web import WebMigration
from migration.faces_config.script_facesConfig import FaceConfigMigration
from migration.components.action.script_component import ComponentsMigration
from migration.pom.action.script_pom import PomMigration
from lxml import etree as ET
from migration.utils.change_definition import ChangeDefinition
from migration.datasource.script_ds import DataSourceMigration
   

class Main:
    """docstring for Main"""
    def changeDefinition(cls,filePath):
        parser = ET.XMLParser(remove_blank_text=True)
        tree = ET.parse(filePath,parser)
        tree=ChangeDefinition.changedefinition(tree)
        root = tree.getroot()
        tree.write(filePath,pretty_print=True,encoding='utf-8')
    changeDefinition=classmethod(changeDefinition)
    def addDeploymentStructure(cls):
        script_dir = os.path.dirname(__file__)
        source=script_dir+"/jboss-deployment-structure.xml"
        earPath=input('please enter the path to the src/main/application directory of the ear project : ')
        subprocess.call(["mkdir","-p",earPath+"/META-INF"])
        subprocess.call(["cp",source,earPath+"/META-INF"])
    addDeploymentStructure=classmethod(addDeploymentStructure)
    def removeFile(cls,filePath):
        subprocess.call(["rm",filePath])
    removeFile=classmethod(removeFile)
    def walk(cls,inputPath):
        isEar=True
        for path, dirs, files in os.walk(inputPath):
            for filepath in [ os.path.join(path, f) for f in files]:
                if not "target" in filepath:
                    if(filepath.endswith(".xhtml") and filepath.__contains__("webapp")):
                        XhtmlTransformation.upgrade(filepath)
                    elif(filepath.endswith(".java") ):
                        JavaTransformation.parseJava(filepath)
                    elif(filepath.endswith("/persistence.xml")):
                        PersistenceMigration.parseXml(filepath)
                    elif(filepath.endswith("/components.xml")):
                        ComponentsMigration.parseXml(filepath)
                    elif(filepath.endswith("/web.xml")):
                        WebMigration.parseXml(filepath)
                    elif(filepath.endswith("pom.xml")):
                        tmp=PomMigration.parseXml(filepath)
                        isEar=isEar or tmp 
                    elif(filepath.endswith("/faces-config.xml")):
                       FaceConfigMigration.parseXml(filepath)
                    elif(filepath.endswith("/pages.xml")):
                        cls.changeDefinition(filepath)
                    elif(filepath.endswith("-ds.xml")):
                        DataSourceMigration.parseXml(filepath)
                    elif(filepath.endswith("/jboss-web.xml")):
                        cls.removeFile(filepath)
        if(isEar):
            cls.addDeploymentStructure()
            ComponentsMigration.addComponents(inputPath)
    walk=classmethod(walk)