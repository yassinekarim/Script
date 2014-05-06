#!/usr/local/bin/python3.4
# -*-coding:utf-8 -*
import re
import xml.etree.ElementTree as ET
def nom_de_la_fonction(path):
	tree = ET.parse('pom.xml')
	root = tree.getroot()
	
	#INFO  [org.jboss.as.ejb3.deployment.processors.EjbJndiBindingsDeploymentUnitProcessor]