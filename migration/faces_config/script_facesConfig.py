"""faces-config.xml migration module"""
#!/usr/bin/python3
# -*-coding:utf-8 -*
from lxml import etree as ET
from migration.utils.change_definition import ChangeDefinition
class FaceConfigMigration:
    """faces config migration class"""
    def parse_xml(cls, file_path):
        """parse the web.xml update definition and richfaces context-param"""
        parser = ET.XMLParser(remove_blank_text=True, load_dtd=True)
        tree = ET.parse(file_path, parser)
        tree = ChangeDefinition.changedefinition(tree)
        root = tree.getroot()
        cls.remove_view_handler(root)
        tree.write(file_path, pretty_print=True, encoding='utf-8', xml_declaration=True)
    parse_xml = classmethod(parse_xml)
    def remove_view_handler(cls, root):
        """remove view handler tag"""
        for element in root:
            if element.tag == "{http://java.sun.com/xml/ns/javaee}application":
                view = element.find("{http://java.sun.com/xml/ns/javaee}view-handler")
                if view is not None:
                    element.remove(view)
    remove_view_handler = classmethod(remove_view_handler)
