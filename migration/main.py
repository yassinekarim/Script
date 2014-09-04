"""module for project migration"""
#!/usr/bin/python3
# -*-coding:utf-8 -*
import os
import subprocess
from migration.java.action.script_java import JavaTransformation
from migration.jsf.script_jsf import XhtmlTransformation
from migration.persistence.script_persistence import PersistenceMigration
from migration.web.script_web import WebMigration
from migration.faces_config.script_facesConfig import FaceConfigMigration
from migration.components.action.script_component import ComponentsMigration
from migration.pom.action.script_pom import PomMigration
from lxml import etree as ET
from migration.utils.change_definition import ChangeDefinition
from migration.datasource.script_ds import DataSourceMigration
class Main:
    """ad deploymen sructure remove obsolete file and migrate files"""
    def change_definition(cls, file_path):
        """change nsmap, file definiton and versio of xml configuration file"""
        parser = ET.XMLParser(remove_blank_text=True)
        tree = ET.parse(file_path, parser)
        tree = ChangeDefinition.changedefinition(tree)
        tree.write(file_path, pretty_print=True, encoding='utf-8')
    change_definition = classmethod(change_definition)
    def add_deployment_structure(cls):
        """add jboss-deployment-structure to ear"""
        script_dir = os.path.dirname(__file__)
        source = script_dir+"/jboss-deployment-structure.xml"
        ear_path = input('please enter the path to the src/main/application directory of the ear project : ')
        subprocess.call(["mkdir", "-p", ear_path+"/META-INF"])
        subprocess.call(["cp", source, ear_path+"/META-INF"])
    add_deployment_structure = classmethod(add_deployment_structure)
    def remove_file(cls, file_path):
        """remove the file specified as a parameter"""
        subprocess.call(["rm", file_path])
    remove_file = classmethod(remove_file)
    def walk(cls, inputPath):
        """browse the project folder and apply changes according to encountered files"""
        is_ear = False
        for path, dirs, files in os.walk(inputPath):
            for filepath in [ os.path.join(path, f) for f in files]:
                if not "target" in filepath:
                    if filepath.endswith(".xhtml") and filepath.__contains__("webapp"):
                        XhtmlTransformation.upgrade(filepath)
                    elif filepath.endswith(".java") :
                        JavaTransformation.parse_java(filepath)
                    elif filepath.endswith("/persistence.xml"):
                        PersistenceMigration.parse_xml(filepath)
                    elif filepath.endswith("/components.xml"):
                        ComponentsMigration.parse_xml(filepath)
                    elif filepath.endswith("/web.xml"):
                        WebMigration.parse_xml(filepath)
                    elif filepath.endswith("pom.xml"):
                        tmp = PomMigration.parse_xml(filepath)
                        is_ear = is_ear or tmp
                    elif filepath.endswith("/faces-config.xml"):
                        FaceConfigMigration.parse_xml(filepath)
                    elif filepath.endswith("/pages.xml"):
                        cls.change_definition(filepath)
                    elif filepath.endswith("-ds.xml"):
                        DataSourceMigration.parse_xml(filepath)
                    elif filepath.endswith("/jboss-web.xml"):
                        cls.remove_file(filepath)
        if is_ear:
            cls.add_deployment_structure()
            ComponentsMigration.add_components(inputPath)
    walk = classmethod(walk)
