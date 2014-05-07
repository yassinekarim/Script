#!/usr/local/bin/python3.4
# -*-coding:utf-8 -*
import sys
from lxml import etree as ET
if len(sys.argv) < 3:
    print("Saisissez le chemin vers les log du serveur et le fichier components.xml en paramètre")
    sys.exit(1)
jndiList=list()
with open(sys.argv[1], 'r') as log:
    texte = log.read()
    listTexte=texte.split('\n')
    listLog=iter(listTexte)
    for ligne in listLog:
        if "[org.jboss.as.ejb3.deployment.processors.EjbJndiBindingsDeploymentUnitProcessor]" in ligne:
            listLog.__next__()
            ligne=listLog.__next__()
            if 'java'in ligne: 
                ligne=listLog.__next__()
                jndi=ligne.split('!')#jndi[0] contains the JNdi and jndi[1] contains the local interface 
                jndiList.append((jndi[0][1:],jndi[1].replace(jndi[1][jndi[1].rfind('.')+1:],jndi[0][jndi[0].rfind('/')+1:]))) # replace local interface class by the implementation class
tree = ET.parse(sys.argv[2])
root = tree.getroot()
for jndi,classe in jndiList:
    el =ET.fromstring('<component class="'+classe+'" jndi-name="'+jndi+'" />')
    el.tail='\n\t'
    root.insert(2, el)
    
print(ET.tostring(tree, pretty_print=True))
tree.write(sys.argv[2],pretty_print=True,encoding='utf-8')