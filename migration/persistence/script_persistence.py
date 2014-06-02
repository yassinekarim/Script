#!/opt/python3/bin/python3 
# -*-coding:utf-8 -*
from lxml import etree as ET
from migration.utils.change_definition import ChangeDefinition
from migration.utils.jndiMigration import JndiMigration
class PersistenceMigration:
    """migrate persistence.xml"""
    def parseXml(cls,filePath):
        """pase the xml, update definition and jndi  add property to use infinispan """
        parser = ET.XMLParser(remove_blank_text=True,load_dtd=True)
        tree = ET.parse(filePath,parser)
        tree=ChangeDefinition.changedefinition(tree)
        root = tree.getroot()
        for persistenceUnit in root:
            if (persistenceUnit.tag=="{http://java.sun.com/xml/ns/persistence}persistence-unit"):
                for element in persistenceUnit:
                    if(element.tag=="{http://java.sun.com/xml/ns/persistence}jta-data-source"):
                        element.text=JndiMigration.changeJndi(element.text,"jboss")
                    elif(element.tag=="{http://java.sun.com/xml/ns/persistence}properties"):
                        for prop in element:
                            if(prop.get("name")=="jboss.entity.manager.factory.jndi.name"):
                                prop.set("value",JndiMigration.changeJndi(prop.get("value"),"jboss"))
                        ET.SubElement(element,"{http://java.sun.com/xml/ns/persistence}property",name="hibernate.id.new_generator_mappings",value="false")
                        ET.SubElement(element,"{http://java.sun.com/xml/ns/persistence}property",name="hibernate.cache.infinispan.cachemanager",value="java:jboss/infinispan/hibernate")
                        ET.SubElement(element,"{http://java.sun.com/xml/ns/persistence}property",name="hibernate.transaction.manager_lookup_class",value="org.hibernate.transaction.JBossTransactionManagerLookup")
            else:
                print ("tag != persistence-unit")
        tree.write(filePath,pretty_print=True,encoding='utf-8')
    parseXml=classmethod(parseXml)