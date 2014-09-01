#!/usr/bin/python3
# -*-coding:utf-8 -*
from migration.java.model.replacement import MethodReplacement
import re
class JavaTransformation:
    """migration function for java file replace old code (annotation/function/instruction) by the upgraded code according to a list of (regex,replacement)"""
 
    replacementList=None
    def getReplacemetList(cls):
        return cls.replacementList
    getReplacemetList=classmethod(getReplacemetList)
    def addMethod(cls,content):
        """add getId method to class wich extend's HibernateDataModel"""
        regexList=["extends[\s]*FilterDataModel[\s]*<.+>","extends[\s]*HibernateDataModel[\s]*<.+>","new[\s]*FilterDataModel[\s]*<.+>","new[\s]*HibernateDataModel[\s]*<.+>"]
        for reg in regexList:
            regex = re.compile(reg)  #!!!!!!!!!!!!!!!!! problem multiple match !!!!!!!!!!!!!!!!!!!!!!!!!!! 
            result= regex.search(content)
            if result:
                match=result.group()
                classMatch=match[match.find('<')+1:match.__len__()-1]
                classMatch=classMatch.strip()
                if (classMatch.__len__()>1):
                    if("extend" in match):
                        fin=content.rfind('}')
                        content=content[:fin]+"""@Override
        protected Object getId("""+classMatch+""" t) {
            // TODO Auto-generated method stub
            return t.getId();
        }""" +content[fin-1:]
                    else:
                        debut,fin=result.span()
                        index=content[fin:].find(";")
                        content=content[:fin+index]+"""{
                        @Override
        protected Object getId("""+classMatch+""" t) {
            // TODO Auto-generated method stub
            return t.getId();
        }
        }"""+content[fin+index:]


        return content
    addMethod=classmethod(addMethod)
    def upgradeCode(cls,content):
        """return the upgraded code as a string"""
        for element in JavaTransformation.replacementList:
            content=element.executeReplace(content)
        content=cls.addMethod(content)
        return content
    upgradeCode = classmethod(upgradeCode)

    def reInitMethodList(cls):
        """re initialize method list for each new parsed file """
        for element in JavaTransformation.replacementList:
            if isinstance(element,MethodReplacement ):
                element.applyChange=False
    reInitMethodList = classmethod(reInitMethodList)

    def parseJava(cls,filePath):
        """read the java file and replace it's content with the upgraded content"""
        f=open(filePath,"r")
        content = f.read()
        f.close()
        content=JavaTransformation.upgradeCode(content)
        JavaTransformation.reInitMethodList()
        f = open(filePath,"w")
        f.write(content)
        f.close()
    parseJava=classmethod(parseJava)