#!/opt/python3/bin/python3 
# -*-coding:utf-8 -*
import os
import glob
import sys
from migration.java.action.confReader import ConfigurationReader
from migration.java.action.script_java import JavaTransformation 
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


JavaTransformation.replacementList=ConfigurationReader.initList()
for path, dirs, files in os.walk(inputPath):
    for filepath in [ os.path.join(path, f) for f in files if f.endswith(".java")]:
        f=open(filepath,"r")
        content = f.read()
        f.close()
        content=JavaTransformation.upgradeCode(content)
        JavaTransformation.reInitMethodList()
        f = open(filepath,"w")
        f.write(content)
        f.close()
        