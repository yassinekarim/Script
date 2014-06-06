#!/opt/python3/bin/python3 
# -*-coding:utf-8 -*
import os
import sys
from migration.main import Main
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

Main.walk(inputPath)