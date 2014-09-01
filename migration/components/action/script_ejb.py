#!/usr/bin/python3
# -*-coding:utf-8 -*
from lxml import etree as ET
class Search4Ejb:
    jndiList=list()
    def parseLog(cls,logContent,componentPath):
        """parse the log to find ejb jndi and add them to components.xml"""        
        listTexte=logContent.split('\n')
        listLog=iter(listTexte)
        for ligne in listLog:
            if "[org.jboss.as.ejb3.deployment.processors.EjbJndiBindingsDeploymentUnitProcessor]" in ligne:
                listLog.__next__()
                ligne=listLog.__next__()
                if 'java'in ligne: 
                    ligne=listLog.__next__()
                    jndi=ligne.split('!')#jndi[0] contains the JNdi and jndi[1] contains the local interface 
                    cls.jndiList.append((jndi[0][1:],jndi[1].replace(jndi[1][jndi[1].rfind('.')+1:],jndi[0][jndi[0].rfind('/')+1:]))) # replace local interface class by the implementation class
        parser = ET.XMLParser(remove_blank_text=True)
        tree = ET.parse(componentPath,parser)
        root = tree.getroot()
        for jndi,classe in cls.jndiList:
            el =ET.fromstring('<component class="'+classe+'" jndi-name="'+jndi+'" />')
            root.insert(2, el)
        tree.write(componentPath,pretty_print=True,encoding='utf-8')
    parseLog=classmethod(parseLog)


# f = open(sys.argv[1],"r")
# content = f.read()     
# Search4Ejb.parseLog(content,sys.argv[2])
# f.close()
