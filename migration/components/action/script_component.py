#!/opt/python3/bin/python3
# -*-coding:utf-8 -*
from lxml import etree as ET
from migration.utils.change_definition import ChangeDefinition
from migration.utils.jndiMigration import JndiMigration
from migration.components.action.script_ejb import Search4Ejb
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
                            prop.text=JndiMigration.changeJndi(prop.text,"jboss")
                        init.set(prop.get("name"),prop.text)
                    root.remove(element)
                    root.insert(2, init)
            elif(element.tag=="{http://jboss.org/schema/seam/persistence}managed-persistence-context"):
                element.set("persistence-unit-jndi-name",JndiMigration.changeJndi(element.get("persistence-unit-jndi-name"),"jboss"))
        tree.write(filePath,pretty_print=True,encoding='utf-8')
    parseXml=classmethod(parseXml)
    componentsFilePath=list()
    def addComponents(cls,projectPath):
        """build and deploy project and give the log to Search4Ejb"""
        oldPath = os.getcwd()
        absoluteProjectPath=os.path.abspath(projectPath)
        os.chdir(projectPath)
        print ("begin mvn clean package"+absoluteProjectPath)
        subprocess.call(["mvn","clean","package"], shell=True)
        print ("end mvn clean package")
        earPath = input("Saisissez le chemin vers l'ear ( . = {} ): ".format(absoluteProjectPath))
        jbossHome = input("Saisissez le chemin absolu vers Jboss7 et assurez vous que le serveur est stoppé: ")
        subprocess.call(["cp",earPath,jbossHome+"/standalone/deployments"], shell=True)
        f=open("log.tmp","w")
        subprocess.call(jbossHome+"/bin/standalone.sh",stdout=f)
        f.close()
        f = open("log.tmp","r")
        content = f.read()     
        f.close()
        for path in cls.componentsFilePath:
            Search4Ejb.parseLog(content,path)
        os.chdir(oldPath)
    addComponents=classmethod(addComponents)