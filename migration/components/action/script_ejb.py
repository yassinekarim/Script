"""script for parsing jboss7 log file"""
#!/usr/bin/python3
# -*-coding:utf-8 -*
from lxml import etree as ET
class Search4Ejb:
    """parse the jboss7 log file"""
    jndi_list = list()
    def parse_log(cls, log_content, component_path):
        """parse the log to find ejb jndi and add them to components.xml"""
        list_texte = log_content.split('\n')
        list_log = iter(list_texte)
        for ligne in list_log:
            if "[org.jboss.as.ejb3.deployment.processors.EjbJndiBindingsDeploymentUnitProcessor]" in ligne:
                list_log.__next__()
                ligne = list_log.__next__()
                if 'java'in ligne:
                    ligne = list_log.__next__()
                    #jndi[0] contains the JNdi and jndi[1] contains the local interface
                    jndi = ligne.split('!')
                    # replace local interface class by the implementation class
                    cls.jndi_list.append((jndi[0][1:], jndi[1].replace(jndi[1][jndi[1].rfind('.')+1:], jndi[0][jndi[0].rfind('/')+1:])))
        parser = ET.XMLParser(remove_blank_text=True)
        tree = ET.parse(component_path, parser)
        root = tree.getroot()
        for jndi, classe in cls.jndi_list:
            el = ET.fromstring('<component class = "'+classe+'" jndi-name = "'+jndi+'" />')
            root.insert(2, el)
        tree.write(component_path, pretty_print=True, encoding='utf-8')
    parse_log = classmethod(parse_log)
# f = open(sys.argv[1], "r")
# content = f.read()
# Search4Ejb.parse_log(content, sys.argv[2])
# f.close()
