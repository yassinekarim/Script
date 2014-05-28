#!/opt/python3/bin/python3
# -*-coding:utf-8 -*
import sys
from lxml import etree as ET
basestring = (str,bytes)

class PomMigration:

    def createDep(cls,groupId,artifactId,version,scope):
        newdep = ET.Element("{http://maven.apache.org/POM/4.0.0}dependency")    
        groupIdTag=ET.Element("{http://maven.apache.org/POM/4.0.0}groupId")
        groupIdTag.text=groupId
        newdep.append(groupIdTag)
        artifactIdTag=ET.Element("{http://maven.apache.org/POM/4.0.0}artifactId")
        artifactIdTag.text=artifactId
        newdep.append(artifactIdTag)
        if(scope):
            scopeTag=ET.Element("{http://maven.apache.org/POM/4.0.0}scope")
            scopeTag.text=scope
            newdep.append(scopeTag)
        if(version):
            versionTag=ET.Element("{http://maven.apache.org/POM/4.0.0}version")
            versionTag.text=version
            newdep.append(versionTag)
        return newdep
    createDep=classmethod(createDep)
    def newDep(cls,element,groupId,artifactId,vers):
        version=element.find("{http://maven.apache.org/POM/4.0.0}version")
        if(version!=None):
            version=vers
        scope=element.find("{http://maven.apache.org/POM/4.0.0}scope")
        if(scope!=None):
            scope=scope.text
        return cls.createDep(groupId,artifactId,version,scope)
    newDep=classmethod(newDep)
    def parseXml(cls,filePath):   
        parser = ET.XMLParser(remove_blank_text=True)
        tree = ET.parse(filePath,parser)
        root = tree.getroot()
        dependencies=root.findall("xmlns:dependencies/xmlns:dependency", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
        richfaces=False
        jsfImpl=False
        for element in dependencies:
            if isinstance(element.tag, basestring):
                if("org.richfaces." in element.find("xmlns:groupId",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text):
                    parent=element.getparent()
                    if(not richfaces):
                        newdep=cls.newDep(element,"org.richfaces.ui","richfaces-components-ui","4.3.6.Final")
                        parent.append(newdep)
                        newdep=cls.newDep(element,"org.richfaces.core","richfaces-core-impl","4.3.6.Final")
                        parent.append(newdep)
                        richfaces=True
                    parent.remove(element)
                elif("com.sun.facelets" ==element.find("xmlns:groupId",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text):
                    parent=element.getparent()
                    if(not jsfImpl):
                        newdep=cls.newDep(element,"com.sun.faces","jsf-impl","2.1.7-jbossorg-2")
                        parent.append(newdep)
                        jsfImpl=True
                    parent.remove(element)
                elif("jsf-impl" == element.find("xmlns:artifactId",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text):
                    parent=element.getparent()
                    if(not jsfImpl):
                        newdep=cls.newDep(element,"com.sun.faces","jsf-impl","2.1.7-jbossorg-2")
                        parent.append(newdep)
                        jsfImpl=True
                    parent.remove(element)
                elif("jsf-api" == element.find("xmlns:artifactId",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text):
                    parent=element.getparent()
                    newdep=cls.newDep(element,"org.jboss.spec.javax.faces","jboss-jsf-api_2.1_spec","2.1.19.1.Final")
                    parent.append(newdep)
                    parent.remove(element)
                elif("javax.ejb"==element.find("xmlns:groupId",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text):
                    parent=element.getparent()
                    newdep=cls.newDep(element,"org.jboss.spec.javax.ejb","jboss-ejb-api_3.1_spec","1.0.1.Final")
                    parent.append(newdep)
                    parent.remove(element)
                elif("hibernate-annotations"==element.find("xmlns:artifactId",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text):
                    parent=element.getparent()
                    newdep=cls.newDep(element,"org.hibernate","hibernate-core","4.0.1.Final")
                    parent.append(newdep)
                    parent.remove(element)   
                elif("ejb3-persistence"==element.find("xmlns:artifactId",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text):
                    parent=element.getparent()
                    parent.remove(element)   
                elif("org.hibernate"==element.find("xmlns:groupId",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text):
                    version=element.find("xmlns:version",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
                    if (version):
                        element.remove(version)
                elif("javax.persistence"==element.find("xmlns:groupId",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text):
                    parent=element.getparent()
                    newdep=cls.newDep(element,"org.hibernate.javax.persistence","hibernate-jpa-2.0-api","1.0.1.Final")
                    parent.append(newdep)
                    parent.remove(element)
                elif("drools-api"==element.find("xmlns:artifactId",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text):
                    parent=element.getparent()
                    parent.remove(element)
                elif("jbpm-jpdl"==element.find("xmlns:artifactId",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text):
                    parent=element.getparent()
                    parent.remove(element)
                    
        tree.write(filePath,pretty_print=True,encoding='utf-8')
    parseXml=classmethod(parseXml)
