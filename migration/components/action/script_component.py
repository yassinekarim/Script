#!/opt/python3/bin/python3
# -*-coding:utf-8 -*
from lxml import etree as ET
from migration.utils.change_definition import ChangeDefinition
from migration.utils.jndiMigration import JndiMigration
from migration.components.action.script_ejb import Search4Ejb
from migration.web.script_web import WebMigration
import os
import subprocess
class ComponentsMigration:
    """component.xml migration """
    def parseXml(cls,filePath):
        cls.componentsFilePath.append(filePath)
        parser = ET.XMLParser(remove_blank_text=True)
        tree = ET.parse(filePath,parser)
        tree=ChangeDefinition.changedefinition(tree)
        root = tree.getroot()
        for element in root:
            if(element.tag=="{http://jboss.org/schema/seam/components}component"):
                if(element.get("name")=="org.jboss.seam.core.init"):
                    init=ET.Element('{http://jboss.org/schema/seam/core}init')
                    for prop in element:
                        if(prop.get("name")=="jndi-pattern"):
                            prop.text=JndiMigration.changeJndi(prop.text.strip(),"app")
                        init.set(prop.get("name"),prop.text)
                    root.remove(element)
                    root.insert(2, init)
            elif(element.tag=="{http://jboss.org/schema/seam/persistence}managed-persistence-context"):
                jndi=element.get("persistence-unit-jndi-name")
                if jndi is not None:
                    element.set("persistence-unit-jndi-name",JndiMigration.changeJndi(jndi,"jboss"))
        tree.write(filePath,pretty_print=True,encoding='utf-8')
    parseXml=classmethod(parseXml)
    componentsFilePath=list()
    def addComponents(cls,projectPath):
        """build and deploy project and give the log to Search4Ejb"""
        oldPath = os.getcwd()
        absoluteProjectPath=os.path.abspath(projectPath)
        os.chdir(projectPath)
        # print ("begin mvn clean package"+absoluteProjectPath)
        # subprocess.call(["mvn","clean","package"], shell=True)
        # print ("end mvn clean package")
        print ("Veuillez deployer l'ear")
        log = input("Saisissez le chemin vers le fichier de log : ")
        f=open(log,"r")
        content = f.read()
        f.close()
        os.chdir(oldPath)
        for path in cls.componentsFilePath:
            Search4Ejb.parseLog(content,path)
            WebMigration.updateJndi()
    addComponents=classmethod(addComponents)