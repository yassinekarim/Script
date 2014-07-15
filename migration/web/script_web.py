#!/opt/python3/bin/python3 
# -*-coding:utf-8 -*
from lxml import etree as ET
from migration.utils.change_definition import ChangeDefinition
class WebMigration:
    
    def parseXml(cls,filePath):
        """parse the web.xml update definition and richfaces context-param"""
        parser = ET.XMLParser(remove_blank_text=True,load_dtd=True)
        tree = ET.parse(filePath,parser)
        tree=ChangeDefinition.changedefinition(tree)
        root = tree.getroot()
        ressourceOptimisation=False
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
        tree.write(filePath,pretty_print=True,encoding='utf-8', xml_declaration=True)
    parseXml=classmethod(parseXml)
