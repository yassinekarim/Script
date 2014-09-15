"""script to read java configuration file"""
#!/usr/bin/python3
# -*-coding:utf-8 -*
import os
from migration.java.model.replacement import AnnotationReplacement
from migration.java.model.replacement import ClassReplacement
from migration.java.model.replacement import MethodReplacement
from lxml import etree as ET
class ConfigurationReader:
    """read the changement_java.xml file and consruct a list accordingly"""
    def read_annotation(cls, tag):
        """read annotation tag and return AnnotationReplacement object"""
        mapping = []
        for iterator in tag:
            if iterator.tag == "mapping":
                mapping.append((iterator.get("old"), iterator.get("new")))
            else:
                print("error: children of annotation has not the tag mapping")
        return AnnotationReplacement(tag.get("regex"), tag.get("replacement"), mapping)
    read_annotation = classmethod(read_annotation)
    def read_class(cls, tag):
        """read class tag and return ClassReplacement object"""
        method = []
        mapping = []
        for iterator in tag:
            if iterator.tag == "method":
                method.append(iterator.get("regex"))
            elif iterator.tag == "mapping":
                mapping.append((iterator.get("old"), iterator.get("new")))
            else:
                print("error: children of class has not the tag method or mapping")
        return ClassReplacement(tag.get("regex"), tag.get("replacement"), method, mapping)
    read_class = classmethod(read_class)
    def read_method(cls, tag):
        """read metod tag and return MethodReplacement object"""
        return MethodReplacement(tag.get("regex"), tag.get("replacement"), False, [])
    read_method = classmethod(read_method)
    def read_tag(cls, tag):
        """switch the tag to the right method"""
        if tag.tag == "annotation":
            return ConfigurationReader.read_annotation(tag)
        elif tag.tag == "class":
            return ConfigurationReader.read_class(tag)
        elif tag.tag == "method":
            return ConfigurationReader.read_method(tag)
    read_tag = classmethod(read_tag)
    def init_list(cls):
        """parse the xml file"""
        script_dir = os.path.dirname(__file__)
        replacement_list = []
        basestring = (str, bytes)
        parser = ET.XMLParser(remove_blank_text=True)
        tree = ET.parse(script_dir+"/changement_java.xml", parser)
        root = tree.getroot()
        for element in root:
            if isinstance(element.tag, basestring):
                replacement_list.append(ConfigurationReader.read_tag(element))
        return replacement_list
    init_list = classmethod(init_list)
