"""script to parse persistence.xml"""
#!/usr/bin/python3
# -*-coding:utf-8 -*
from lxml import etree as ET
from migration.utils.change_definition import ChangeDefinition
from migration.utils.jndiMigration import JndiMigration
class PersistenceMigration:
    """migrate persistence.xml"""
    def parse_xml(cls, file_path):
        """pase the xml, update definition and jndi  add property to desactivae the new hibernate 4.0.1.Final"""
        parser = ET.XMLParser(remove_blank_text=True, load_dtd=True)
        tree = ET.parse(file_path, parser)
        tree = ChangeDefinition.changedefinition(tree)
        root = tree.getroot()
        for persistence_unit in root:
            if persistence_unit.tag == "{http://java.sun.com/xml/ns/persistence}persistence-unit":
                cls.parse_persisence_unit(persistence_unit)
            else:
                print("tag != persistence-unit")
        tree.write(file_path, pretty_print=True, encoding='utf-8', xml_declaration=True)
    parse_xml = classmethod(parse_xml)
    def parse_persisence_unit(cls,persistence_unit):
        """parse a persistence_unit"""
        for element in persistence_unit:
            if element.tag == "{http://java.sun.com/xml/ns/persistence}jta-data-source":
                element.text = JndiMigration.change_jndi_ds(element.text, "jboss")
            elif element.tag == "{http://java.sun.com/xml/ns/persistence}properties":
                for prop in element:
                    if prop.get("name") == "jboss.entity.manager.factory.jndi.name":
                        prop.set("value", JndiMigration.change_jndi(prop.get("value"), "jboss"))
                ET.SubElement(element, "{http://java.sun.com/xml/ns/persistence}property", name = "hibernate.id.new_generator_mappings", value = "false")
    parse_persisence_unit = classmethod(parse_persisence_unit)
