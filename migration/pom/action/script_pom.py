#!/opt/python3/bin/python3
# -*-coding:utf-8 -*
import sys
from lxml import etree as ET
import os
basestring = (str,bytes)

class PomMigration:
    pluginVersionList=None
    def getPluginVersionList(cls):
        return cls.pluginVersionList
    getPluginVersionList=classmethod(getPluginVersionList)
    def createDep(cls,groupId,artifactId,version,scope):
        """create a new dependencies element """
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
        """ if version is set update version"""
        version=element.find("{http://maven.apache.org/POM/4.0.0}version")
        if(version!=None):
            version=vers
        scope=element.find("{http://maven.apache.org/POM/4.0.0}scope")
        if(scope!=None):
            scope=scope.text
        return cls.createDep(groupId,artifactId,version,scope)
    newDep=classmethod(newDep)
    def findVersion(cls,filePath):
        parser=ET.XMLParser(remove_blank_text=True)
        tree=ET.parse(filePath,parser)
        root=tree.getroot()
        version=root.find("xmlns:version",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
        if (version is not None):
            return version.text
        else:
            relativePath=root.find("xmlns:parent/xmlns:relativePath", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
            if(relativePath is not None):
                absoluteFilePath=os.path.abspath(filePath)
                projectPath=absoluteFilePath[:absoluteFilePath.rfind("/")]
                oldPath = os.getcwd()
                absoluteProjectPath=os.path.abspath(projectPath)
                os.chdir(projectPath)
                tmp=cls.findVersion(relativePath.text)
                os.chdir(oldPath)
                return tmp
            else:
                versionText=input("version of "+artifactId+" cannot be determined please enter the version")
                return versionText

    findVersion=classmethod(findVersion)
    def verifyPom(cls,filePath,artifactId):
        parser=ET.XMLParser(remove_blank_text=True)
        tree=ET.parse(filePath,parser)
        root=tree.getroot()
        artifactIdTag=root.find("xmlns:artifactId",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
        if(artifactIdTag.text!=artifactId):
            print ("error: in "+filePath+"  expected artifactId "+artifactId+" found "+artifactIdTag.text)
            return ""
        version=root.find("xmlns:version",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
        if (version is not None):
            return version.text
        else:
            relativePath=root.find("xmlns:parent/xmlns:relativePath", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
            if(relativePath is not None):
                absoluteFilePath=os.path.abspath(filePath)
                projectPath=absoluteFilePath[:absoluteFilePath.rfind("/")]
                oldPath = os.getcwd()
                absoluteProjectPath=os.path.abspath(projectPath)
                os.chdir(projectPath)
                tmp=cls.findVersion(relativePath.text)
                os.chdir(oldPath)
                return tmp
            else:
                versionText=input("version of "+artifactId+" cannot be determined please enter the version")
                return versionText

    verifyPom=classmethod(verifyPom)
    def getProjectPath(cls,artifactId):
        projectPath=input('Please enter the path to the project directory :')
        while (not os.path.exists(projectPath) and not os.path.isdir(projectPath)):
            print (projectPath+" does not exist on disk or isn't a dir")
            projectPath=input('Please enter the path to the project directory :')
        pomFilePath=os.path.join(projectPath, "pom.xml")
        if(not os.path.isfile(pomFilePath)):
            print ("error: no pom found in "+projectPath)
            return cls.getProjectPath(artifactId)
        tmp=cls.verifyPom(pomFilePath,artifactId)
        if(tmp==""):
            return cls.getProjectPath(artifactId)
        return projectPath

    getProjectPath=classmethod(getProjectPath)
    def parseXml(cls,filePath):
        """parse pom.xml to change dependecies version"""
        parser = ET.XMLParser(remove_blank_text=True)
        tree = ET.parse(filePath,parser)
        root = tree.getroot()
        dependencies=root.findall("xmlns:dependencies/xmlns:dependency", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
        plugins=root.findall("xmlns:build/xmlns:plugins/xmlns:plugin", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
        richfaces=False
        jsfImpl=False
        isEar=False
        packaging=root.find("{http://maven.apache.org/POM/4.0.0}packaging")
        if (not (packaging is None) and packaging.text=="ear"):
            isEar=True
        for element in plugins:
            if isinstance(element.tag, basestring):
                artifactId=element.find("xmlns:artifactId",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text
                for plugin in cls.pluginVersionList:
                    if(plugin.artifactId==artifactId):
                        plugin.executeReplace(element)
                        break
                if(artifactId=="maven-ear-plugin"):
                    configuration=element.find("xmlns:configuration",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
                    jboss=configuration.find("xmlns:jboss",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
                    if (jboss is not None):
                        version=jboss.find("xmlns:version",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
                        if(version is not None):
                            if(version.text=="5"):
                                version.text="6"
                            configuration.append(version)
                        configuration.remove(jboss)
        for element in dependencies:
            if isinstance(element.tag, basestring):
                if ("org.apache.maven.plugins" in element.find("xmlns:groupId",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text):
                    artifactId=element.find("xmlns:artifactId",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text
                    for plugin in pluginVersionList:
                        if(plugin.artifactId==artifactId):
                            plugin.executeReplace(element)
                            break
                elif("org.richfaces." in element.find("xmlns:groupId",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text):
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
                elif("jboss-seam-jul"==element.find("xmlns:artifactId",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text):
                    parent=element.getparent()
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
                elif("net.ihe.gazelle" in element.find("xmlns:groupId",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text):
                    groupId=element.find("xmlns:groupId",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
                    artifactId=element.find("xmlns:artifactId",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
                    version=element.find("xmlns:version",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
                    depType=element.find("xmlns:type",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
                    if(depType is not None and depType.text=="ejb"):
                        isMigrated=input('is the project with artifactId='+artifactId.text+' already migrated (y/n) [y]')or 'y'
                        while(isMigrated!='y'and isMigrated!='n'):
                            print('incorect input try again:')
                            isMigrated=input('is the project with artifactId='+artifactId.text+' already migrated answer yes if the project directory is a subfolder of the parent project (y/n) [y]')or 'y'
                        if (isMigrated=='y'):
                            if (version is not None):
                                versionText=input('Please enter the version of the migrated project ['+version.text+']') or version.text
                                version.text=versionText
                        else:
                            from migration.main import Main
                            projectPath=cls.getProjectPath(artifactId.text)
                            print(projectPath)
                            Main.walk(projectPath)
        tree.write(filePath,pretty_print=True,encoding='utf-8',xml_declaration=True)
        return isEar
    parseXml=classmethod(parseXml)