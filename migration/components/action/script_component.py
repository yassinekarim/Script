#!/opt/python3/bin/python3 
# -*-coding:utf-8 -*
from lxml import etree as ET

def parseXml(filePath):
    parser = ET.XMLParser(remove_blank_text=True)
    tree = ET.parse(filePath,parser)
    root = tree.getroot()
    