#!/usr/bin/python3
# -*-coding:utf-8 -*
import os
import glob
import sys
import migration.java.model.replacement

class JavaTransformation:
    """migration function for java file replace old code (annotation/function/instruction) by the upgraded code according to a list of (regex,replacement)"""
    def initList():
        replacementList=[]
        element=migration.java.model.replacement.AnnotationReplacement("^[\t ]*@[\s]*(org.hibernate.annotations.)?CollectionOfElements[\s]*((\(([^,)]+)(,[^,)]+)*\))?)?","@javax.persistence.ElementCollection",[("targetElement","targetClass"),("fetch","fetch")])
        replacementList.append(element)
        element=migration.java.model.replacement.ClassReplacement("^[\t ]*(org.richfaces.model.)?UploadItem","org.richfaces.model.UploadedFile")
        replacementList.append(element)
        element=migration.java.model.replacement.MethodReplacement("getUploadedFile","getUploadItem")
        replacementList.append(element)
        return replacementList

    replacementList=initList()



    def upgradeCode(cls,content):
        """return the upgraded code as a string"""
        for element in JavaTransformation.replacementList:
                content=element.executeReplace(content)

        return content
    upgradeCode = classmethod(upgradeCode)

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
    for filepath in [ os.path.join(path, f) for f in files if f.endswith(".java")]:
        f=open(filepath,"r")
        content = f.read()
        f.close()
        content=JavaTransformation.upgradeCode(content)
        f = open(filepath,"w")
        f.write(content)
        f.close()
        