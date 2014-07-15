#!/opt/python3/bin/python3
# -*-coding:utf-8 -*
import os
from migration.pom.model.pomVersion import Plugin
from lxml import etree as ET

class PluginVersionReader:
    """read the plugin_version.xml file and consruct a list accordingly"""
      
    def readTag(cls,tag):
        """read plugin tag and return pluginVersion object"""
        return Plugin(tag.find("artifactId").text,tag.find("version").text)
    readTag= classmethod(readTag)
    def initList(cls):
        """parse the xml file"""
        script_dir = os.path.dirname(__file__)
        replacementList=[]
        basestring = (str,bytes)
        parser = ET.XMLParser(remove_blank_text=True)
        tree = ET.parse(script_dir+"/plugin_version.xml",parser)
        root = tree.getroot()
        for element in root:
            if isinstance(element.tag, basestring):
                replacementList.append(cls.readTag(element))
        return replacementList
    initList = classmethod(initList)