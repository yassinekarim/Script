#!/opt/python3/bin/python3 
# -*-coding:utf-8 -*
from migration.java.model.replacement import MethodReplacement
class JavaTransformation:
    """migration function for java file replace old code (annotation/function/instruction) by the upgraded code according to a list of (regex,replacement)"""
 
    replacementList=None
    def getReplacemetList(cls):
        return cls.replacementList
    getReplacemetList=classmethod(getReplacemetList)
    
    def upgradeCode(cls,content):
        """return the upgraded code as a string"""
        for element in JavaTransformation.replacementList:
            content=element.executeReplace(content)

        return content
    upgradeCode = classmethod(upgradeCode)

    def reInitMethodList(cls):
        """re initialize method list for each new parsed file """
        for element in JavaTransformation.replacementList:
            if isinstance(element,MethodReplacement ):
                element.applyChange=False
    reInitMethodList = classmethod(reInitMethodList)
        