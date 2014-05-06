#!/usr/local/bin/python3.4
# -*-coding:utf-8 -*
import sys
if len(sys.argv) < 2:
    print("Saisissez le chemin vers les log du serveur en paramètre")
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

print(jndiList)