"""read the plugin_version.xml file and consruct a list accordingly"""
#!/usr/bin/python3
# -*-coding:utf-8 -*
import os
from migration.pom.model.pomVersion import Plugin
from lxml import etree as ET
class PluginVersionReader:
    """read the plugin_version.xml file and consruct a list accordingly"""
    def read_tag(cls, tag):
        """read plugin tag and return pluginVersion object"""
        return Plugin(tag.find("artifactId").text, tag.find("version").text)
    read_tag = classmethod(read_tag)
    def init_list(cls):
        """parse the xml file"""
        script_dir = os.path.dirname(__file__)
        replacement_list = []
        basestring = (str, bytes)
        parser = ET.XMLParser(remove_blank_text=True)
        tree = ET.parse(script_dir+"/plugin_version.xml", parser)
        root = tree.getroot()
        for element in root:
            if isinstance(element.tag, basestring):
                replacement_list.append(cls.read_tag(element))
        return replacement_list
    init_list = classmethod(init_list)
