#!/usr/bin/python3
# -*-coding:utf-8 -*
import os
import sys
from migration.main import Main
from migration.java.action.confReader import ConfigurationReader
from migration.java.action.script_java import JavaTransformation
from migration.pom.action.script_pom import PomMigration
from migration.pom.action.pluginVersionReader import PluginVersionReader
SIZE = len(sys.argv)
if SIZE == 1 or SIZE > 2:
    print("Usage: script_java.py project_folder")
    sys.exit(1)
INPUT_PATH = sys.argv[1]
if not os.path.exists(INPUT_PATH):
    print(INPUT_PATH+" does not exist on disk")
    sys.exit(1)
if not os.path.isdir(INPUT_PATH):
    print(INPUT_PATH+" isn't a dir")
    sys.exit(1)
#reads argument read conf files and call main module
JavaTransformation.replacement_list = ConfigurationReader.init_list()
PomMigration.pluginVersionList = PluginVersionReader.init_list()
Main.walk(INPUT_PATH)
