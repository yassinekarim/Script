#!/opt/python3/bin/python3
# -*-coding:utf-8 -*
import re

class AbstractReplacement:
    def __init__(self, regex,replacement,mapping):
        self.regex = regex
        self.replacement = replacement
        self.mapping=mapping
    def gazelleReplace(cls,content,debut,fin,old,new):
        """replace old by new in content without having to search in the whole file and update fin accordingly"""
        content=content[:debut]+content[debut:fin].replace(old,new,1)+content[fin:]
        offset =new.__len__()-old.__len__()
        return offset,content
    gazelleReplace = classmethod(gazelleReplace)
    def changeMapping(self,content,debut,fin):
        """mapping is a list of (oldParameter,newParameter) if oldparameter is found in content[debut:fin] it will be replaced by newParameter and fin updated accordingly"""
        offset=0
        for old,new in self.mapping:
            if (old==new):
                continue
            regex = re.compile(old)
            result = regex.search(content[debut:fin])
            
            if result:
                tmp,content=AbstractReplacement.gazelleReplace(content,debut,fin,old,new)
                offset+=tmp
        return offset,content


    def changeCode(self,match,content,debut,fin,importChanged):
        """ replace code and ad import if necessay"""
        match=match.strip() #remove white spaces from the border of the string
        pointIndex=match.find(".")
        offset,content=self.changeMapping(content,debut,fin)
        fin+=offset
        if (pointIndex!=-1):#found annotation with package declaration eg: @org.hibernate.annotations.CollectionOfElements(targetElement = java.lang.String.class)
            tmp,content=AbstractReplacement.gazelleReplace(content,debut,fin,match,self.replacement)
            offset+=tmp
            return offset,importChanged,content
        else:#found annoataio withou package declaration eg :@CollectionOfElements(targetElement = java.lang.String.class)
            tmp,content=AbstractReplacement.gazelleReplace(content,debut,fin,match,self.replacement[self.replacement.rfind(".")+1:])
            offset+=tmp
            if (not importChanged):
                elementStr=match # eg :CollectionOfElements
                regex = re.compile("import[\s]+[\w.]+"+elementStr)  #!!!!!!!!!!!!!!!!! problem multiple match !!!!!!!!!!!!!!!!!!!!!!!!!!! 
                result= regex.search(content)
                if result:
                    debutImport,finImport=result.span()
                    matchImport=result.group() # eg :import org.hibernate.annotations.CollectionOfElements
                    importStr=matchImport[7:] #eg :org.hibernate.annotations.CollectionOfElements
                    newImportStr=self.replacement #eg :javax.persistence.ElementCollection
                    tmp,content=AbstractReplacement.gazelleReplace(content,debutImport,finImport,importStr,newImportStr)
                    offset+=tmp
                else:
                    print ("import not found for match "+match)
                return offset,True,content
            else:
                return offset,importChanged,content
    def executeReplace(self,content):
        """find all occurence of the regex and call changeCode to change them one by one """
        regex = re.compile(self.regex,re.MULTILINE)
        it = regex.finditer(content)
        importChanged=False
        offset=0
        for result in it:
            debut,fin=result.span()
            debut+=offset
            fin+=offset
            match=result.group()
            tmp,importChanged,content=self.changeCode(match,content,debut,fin,importChanged)
            offset+=tmp
        return content

class AnnotationReplacement(AbstractReplacement):

    def __init__(self,regex, replacement, mapping):
        AbstractReplacement.__init__(self, regex,replacement,mapping)
        

    def changeCode(self,match,content,debut,fin,importChanged):
        """change the annotation, import and the parameter of the annotation """
        indexParenthese= match.find("(")
        strWithoutP=match[:indexParenthese if indexParenthese!=-1 else match.__len__()]
        strWithoutP=strWithoutP.rstrip() #remove white spaces from the right of the string
        pointIndex=strWithoutP.find(".")
        indexAt=match.find("@")
        offset,content=self.changeMapping(content,debut,fin)
        fin+=offset
        if (pointIndex!=-1):#found annotation with package declaration eg: @org.hibernate.annotations.CollectionOfElements(targetElement = java.lang.String.class)
            tmp,content=AbstractReplacement.gazelleReplace(content,debut,fin,strWithoutP[indexAt:],self.replacement)
            offset+=tmp
            return offset,importChanged,content
        else:#found annoataio withou package declaration eg :@CollectionOfElements(targetElement = java.lang.String.class)
            tmp,content=AbstractReplacement.gazelleReplace(content,debut,fin,strWithoutP[indexAt+1:],self.replacement[self.replacement.rfind(".")+1:])
            offset+=tmp
            if (not importChanged):
                elementStr=strWithoutP[strWithoutP.find("@")+1:] # eg :CollectionOfElements
                regex = re.compile("import[\s]+[\w.]+"+elementStr)  #!!!!!!!!!!!!!!!!! problem multiple match !!!!!!!!!!!!!!!!!!!!!!!!!!! 
                result= regex.search(content)
                if result:
                    debutImport,finImport=result.span()
                    matchImport=result.group() # eg :import org.hibernate.annotations.CollectionOfElements
                    importStr=matchImport[7:] #eg :org.hibernate.annotations.CollectionOfElements
                    newImportStr=self.replacement[1:] #eg :javax.persistence.ElementCollection
                    tmp,content=AbstractReplacement.gazelleReplace(content,debutImport,finImport,importStr,newImportStr)
                    offset+=tmp
                else:
                    print ("import not found for match "+match)
                return offset,True,content
            else:
                return offset,importChanged,content
class MethodReplacement(AbstractReplacement): 
    def __init__(self,regex, replacement,applyChange,mapping):
        AbstractReplacement.__init__(self, regex,replacement,mapping) 
        self.applyChange=applyChange
    def changeCode(self,match,content,debut,fin,importChanged):
        if (self.applyChange):
            return super().changeCode(match,content,debut,fin,True)
        else:
            return 0,True,content

class ClassReplacement(AbstractReplacement):

    def __init__(self,regex, replacement,methodChange,mapping):
        AbstractReplacement.__init__(self, regex,replacement,mapping)
        self.methodChange=methodChange
    def executeReplace(self,content):
        """find all occurence of the regex and call changeCode to change them one by one """
        regex = re.compile(self.regex,re.MULTILINE)
        it = regex.finditer(content)
        importChanged=False
        regexMatch=False
        offset=0
        for result in it:
            debut,fin=result.span()
            debut=debut+offset
            fin=fin+offset  
            match=result.group()
            tmp,importChanged,content=self.changeCode(match,content,debut,fin+13,importChanged)
            offset+=tmp
            regexMatch=True
        if(regexMatch):
            from migration.java.action.script_java import JavaTransformation
            replacementList=JavaTransformation.getReplacemetList()
            for element in replacementList:
                if isinstance(element,MethodReplacement ):
                    if (element.regex in self.methodChange):
                        element.applyChange=True
        return content