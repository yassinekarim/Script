#!/opt/python3/bin/python3 
# -*-coding:utf-8 -*
from lxml import etree as ET
from migration.utils.change_definition import ChangeDefinition
from migration.components.action.script_ejb import Search4Ejb
class WebMigration:
    projectFilePath=""
    filePath=""
    def updateJndi(cls):
        parser = ET.XMLParser(remove_blank_text=True,load_dtd=True)
        tree = ET.parse(cls.filePath,parser)   
        root = tree.getroot()
        jndiList=Search4Ejb.jndiList
        for element in root:
            if(element.tag=="{http://java.sun.com/xml/ns/javaee}context-param"):
                paramName=element.find("{http://java.sun.com/xml/ns/javaee}param-name")
                paramValue=element.find("{http://java.sun.com/xml/ns/javaee}param-value")
                if(paramName.text=="resteasy.jndi.resources"):
                    paramValues=paramValue.text.strip().split(',')
                    newJndiList=list()
                    for oldJndi in paramValues:
                        oldJndi=oldJndi[:len(oldJndi)-6]
                        oldJndi=oldJndi[oldJndi.rfind('/')+1:]
                        newJNdi=[s for s in [jndiTuple[0] for jndiTuple in jndiList] if oldJndi in s]
                        newJndiList.append(newJNdi[0])
                    paramValue.text=','.join(newJndiList)
        tree.write(cls.filePath,pretty_print=True,encoding='utf-8', xml_declaration=True)         
    updateJndi=classmethod(updateJndi)
    def parseXml(cls,filePath):
        """parse the web.xml update definition and richfaces context-param"""
        if (cls.projectFilePath in filePath):
            cls.filePath=filePath
        parser = ET.XMLParser(remove_blank_text=True,load_dtd=True)
        tree = ET.parse(filePath,parser)
        tree=ChangeDefinition.changedefinition(tree)
        root = tree.getroot()
        ressourceOptimisation=False
        ressoureServlet=False
        for element in root:
            if(element.tag=="{http://java.sun.com/xml/ns/javaee}context-param"):
                paramName=element.find("{http://java.sun.com/xml/ns/javaee}param-name")
                paramValue=element.find("{http://java.sun.com/xml/ns/javaee}param-value")
                if(paramName.text=="org.richfaces.SKIN"):
                    paramName.text="org.richfaces.skin"
                    if(paramValue.text=="laguna"):
                        paramValue.text="blueSky"
                elif(paramName.text=="org.richfaces.BASE_SKIN"):
                    paramName.text="org.richfaces.baseSkin"
                elif(paramName.text=="org.richfaces.CONTROL_SKINNING"):
                    paramName.text="org.richfaces.enableControlSkinning"
                    if(paramValue.text=="disable"):
                        paramValue.text="false"
                    else:
                        paramValue.text="true"
                elif(paramName.text=="org.richfaces.CONTROL_SKINNING_CLASSES"):
                    paramName.text="org.richfaces.enableControlSkinningClasses"
                    if(paramValue.text=="disable"):
                        paramValue.text="false"
                    else:
                        paramValue.text="true"
                elif(paramName.text=="org.richfaces.CONTROL_SKINNING_LEVEL"):
                    element.getparent().remove(element)
                elif(paramName.text=="org.richfaces.LoadScriptStrategy" or paramName.text=="org.richfaces.LoadStyleStrategy"):
                    if(ressourceOptimisation):
                        root.remove(element)
                    else:
                        paramName.text="org.richfaces.resourceOptimization.enabled"
                        ressourceOptimisation=True
                        if(paramValue.text=="ALL"):
                            paramValue.text="true"
                        else:
                            paramValue.text="false"
            elif(not ressoureServlet):
                if(element.tag=="{http://java.sun.com/xml/ns/javaee}servlet-mapping"):
                    ressoureServlet=True
                    servlet=ET.fromstring("""<servlet>
    <servlet-name>Resource Servlet</servlet-name>
    <servlet-class>org.richfaces.webapp.ResourceServlet</servlet-class>
    <load-on-startup>1</load-on-startup>
</servlet>""")
                    servletMapping=ET.fromstring("""<servlet-mapping>
    <servlet-name>Resource Servlet</servlet-name>
    <url-pattern>/org.richfaces.resources/*</url-pattern>
</servlet-mapping>""")
                    parent=element.getparent()
                    index=parent.index(element)
                    parent.insert(index+1,servlet)
                    parent.insert(index+2,servletMapping)
        tree.write(filePath,pretty_print=True,encoding='utf-8', xml_declaration=True)
    parseXml=classmethod(parseXml)
