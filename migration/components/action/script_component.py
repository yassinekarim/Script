"""module for components.xml migration"""
#!/usr/bin/python3
# -*-coding:utf-8 -*
from lxml import etree as ET
from migration.utils.change_definition import ChangeDefinition
from migration.utils.jndiMigration import JndiMigration
from migration.components.action.script_ejb import Search4Ejb
from migration.web.script_web import WebMigration
import os
class ComponentsMigration:
    """component.xml migration """
    def parse_xml(cls, file_path):
        """parse the xml change core init tag"""
        cls.componentsFilePath.append(file_path)
        parser = ET.XMLParser(remove_blank_text=True)
        tree = ET.parse(file_path, parser)
        tree = ChangeDefinition.changedefinition(tree)
        root = tree.getroot()
        for element in root:
            if element.tag == "{http://jboss.org/schema/seam/components}component":
                if element.get("name") == "org.jboss.seam.core.init":
                    init = ET.Element('{http://jboss.org/schema/seam/core}init')
                    for prop in element:
                        if prop.get("name") == "jndi-pattern":
                            prop.text = JndiMigration.change_jndi(prop.text.strip(), "app")
                        init.set(prop.get("name"), prop.text)
                    root.remove(element)
                    root.insert(2, init)
            elif element.tag == "{http://jboss.org/schema/seam/persistence}managed-persistence-context":
                jndi = element.get("persistence-unit-jndi-name")
                if jndi is not None:
                    element.attrib.pop("persistence-unit-jndi-name")
                    # element.set("persistence-unit-jndi-name", JndiMigration.change_jndi(jndi, "jboss"))
                element.set("entity-manager-factory", "#{entityManagerFactory}")
        tree.write(file_path, pretty_print=True, encoding='utf-8')
    parse_xml = classmethod(parse_xml)
    componentsFilePath = list()
    def add_components(cls, project_path):
        """build and deploy project and give the log to Search4Ejb"""
        old_path = os.getcwd()
        os.chdir(project_path)
        # print("begin mvn clean package"+absoluteProjectPath)
        # subprocess.call(["mvn", "clean", "package"], shell = True)
        # print("end mvn clean package")
        print("Veuillez deployer l'ear")
        log = input("Saisissez le chemin vers le fichier de log : ")
        f = open(log, "r")
        content = f.read()
        f.close()
        os.chdir(old_path)
        for path in cls.componentsFilePath:
            Search4Ejb.parse_log(content, path)
            WebMigration.update_jndi()
    add_components = classmethod(add_components)
