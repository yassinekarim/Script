#!/opt/python3/bin/python3 
# -*-coding:utf-8 -*
import os
import glob
import sys
from lxml import etree as ET
import migration.jsf.script_jsf import XhtmlTransformation
size = len(sys.argv)
if size == 1 or size > 2:
    print ("Usage: script_java.py project_folder")
    sys.exit(1)
inputPath = sys.argv[1]
if not os.path.exists(inputPath):
    print (inputPath+" does not exist on disk")
    sys.exit(1)
if not os.path.isdir(inputPath):
    print (inputPath+" isn't a dir")
    sys.exit(1)

for path, dirs, files in os.walk(inputPath):
    for filepath in [ os.path.join(path, f) for f in files if f.endswith(".xhtml")]:
        parser = ET.XMLParser(remove_blank_text=True)
        tree = ET.parse(filepath,parser)
        tree = htmlTransformation.upgrade(tree)
        tree.write(filepath,pretty_print=True,encoding='utf-8')
