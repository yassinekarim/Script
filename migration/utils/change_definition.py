"""common module for changing definition of configuration file"""
#!/usr/bin/python3
# -*-coding:utf-8 -*
import re
from lxml import etree as ET
class ChangeDefinition:
    """class for changing definition"""
    def new_xml(cls, root):
        """change old seam xmlns tag to new one """
        basestring = (str, bytes)
        for el in root.iter():
            if isinstance(el.tag, basestring):
                el.tag = str(el.tag).replace("http://jboss.com/products/seam/", "http://jboss.org/schema/seam/")
        return root
    new_xml = classmethod(new_xml)
    def convert(cls, namespace):
        """change old xmlns to new one """
        namespace = str(namespace)
        if re.search("jboss.com/products/seam/", namespace):
            return namespace.replace("jboss.com/products/seam/", "jboss.org/schema/seam/")
        elif "http://www.w3.org/2001/XMLSchema-instance" == namespace:
            return namespace
        else:
            print("erreur namespace")
            return namespace
    convert = classmethod(convert)
    def change_def_seam(cls, page, tree):
        """change definition of pages.xml and components.xml"""
        root = tree.getroot()
        component_namespace = "http://jboss.org/schema/seam/"+page
        component = "{%s}" % component_namespace
        nsmap_ = {None : component_namespace}
        for key in root.nsmap.keys():
            nsmap_[key] = cls.convert(root.nsmap[key])
        print(component + page)
        new_root = ET.Element(component + page, nsmap=nsmap_)
        new_root.set('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation', root.get('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation').replace("http://jboss.com/products/seam/", "http://jboss.org/schema/seam/").replace("2.2", "2.3"))
        root = cls.new_xml(root)
        new_root.text = root.text
        for element in root:
            new_root.append(element)
        tree._setroot(new_root)
        return tree
    change_def_seam = classmethod(change_def_seam)
    def changedefinition(cls, tree):
        """change defintion of config file """
        root = tree.getroot()
        if "{http://java.sun.com/xml/ns/javaee}web-app" == root.tag:
            root.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation", "http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_3_0.xsd")
            root.set("version", "3.0")
        elif "{http://jboss.com/products/seam/components}components" == root.tag:
            tree = cls.change_def_seam("components", tree)
        elif root.tag == "{http://jboss.com/products/seam/pages}pages":
            tree = cls.change_def_seam("pages", tree)
        elif "{http://java.sun.com/xml/ns/persistence}persistence" == root.tag:
            root.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation", "http://java.sun.com/xml/ns/persistence http://java.sun.com/xml/ns/persistence/persistence_2_0.xsd")
            root.set("version", "2.0")
        elif "{http://java.sun.com/xml/ns/javaee}faces-config" == root.tag:
            root.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation", "http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-facesconfig_2_1.xsd")
            root.set("version", "2.1")
        return tree
    changedefinition = classmethod(changedefinition)
