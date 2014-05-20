#!/usr/bin/python3
# -*-coding:utf-8 -*
import re
class AbstractReplacement:
    def __init__(self, regex,replacement):
        self.regex = regex
        self.replacement = replacement
    def gazelleReplace(cls,content,debut,fin,old,new):
        """replace old by new in content without having to search in the whole file and update fin accordingly"""
        content=content[:debut]+content[debut:fin].replace(old,new)+content[fin:]
        fin =fin+new.__len__()-old.__len__()
        return fin,content
    gazelleReplace = classmethod(gazelleReplace)

    def executeReplace(self,content):
        """find all occurence of the regex and call changeCode to change them one by one """
        regex = re.compile(self.regex,re.MULTILINE)
        it = regex.finditer(content)
        importChanged=False
        for result in it:
            debut,fin=result.span()
            match=result.group()
            importChanged,content=self.changeCode(match,content,debut,fin,importChanged)
        return content

    def changeCode(self,match,content,debut,fin,importChanged):
        """ replace code and ad import if ecessay"""
        match=match.strip() #remove white spaces from the border of the string
        pointIndex=match.find(".")
        if (pointIndex!=-1):#found annotation with package declaration eg: @org.hibernate.annotations.CollectionOfElements(targetElement = java.lang.String.class)
            fin,content=AbstractReplacement.gazelleReplace(content,debut,fin,match,self.replacement)
            return importChanged,content
        else:#found annoataio withou package declaration eg :@CollectionOfElements(targetElement = java.lang.String.class)
            fin,content=AbstractReplacement.gazelleReplace(content,debut,fin,match,self.replacement[self.replacement.rfind(".")+1:])
            if (not importChanged):
                elementStr=match # eg :CollectionOfElements
                regex = re.compile("import[\s]+[\w.]+"+elementStr)  #!!!!!!!!!!!!!!!!! problem multiple match !!!!!!!!!!!!!!!!!!!!!!!!!!! 
                result= regex.search(content)
                if result:
                    debutImport,finImport=result.span()
                    matchImport=result.group() # eg :import org.hibernate.annotations.CollectionOfElements
                    importStr=matchImport[7:] #eg :org.hibernate.annotations.CollectionOfElements
                    newImportStr=self.replacement #eg :javax.persistence.ElementCollection
                    finImport,content=AbstractReplacement.gazelleReplace(content,debutImport,finImport,importStr,newImportStr)
                else:
                    print ("import not found for match "+match)
                return True,content
            else:
                return importChanged,content


class AnnotationReplacement(AbstractReplacement):

    def __init__(self,regex, replacement, mapping):
        AbstractReplacement.__init__(self, regex,replacement)
        self.mapping = mapping
        
    def changeAnnotationParameter(self,content,debut,fin):
        """mapping is a list of (oldParameter,newParameter) if oldparameter is found in content[debut:fin] it will be replaced by newParameter and fin updated accordingly"""
        for old,new in self.mapping:
            if (old==new):
                continue
            regex = re.compile(old)
            result = regex.search(content[debut:fin])
            if result:
                fin,content=AbstractReplacement.gazelleReplace(content,debut,fin,old,new)
        return fin,content
    def changeCode(self,match,content,debut,fin,importChanged):
        """change the annotation, import and the parameter of the annotation """
        indexParenthese= match.find("(")
        strWithoutP=match[:indexParenthese if indexParenthese!=-1 else match.__len__()]
        strWithoutP=strWithoutP.rstrip() #remove white spaces from the right of the string
        pointIndex=strWithoutP.find(".")
        indexAt=match.find("@")
        fin,content=self.changeAnnotationParameter(content,debut,fin)
        if (pointIndex!=-1):#found annotation with package declaration eg: @org.hibernate.annotations.CollectionOfElements(targetElement = java.lang.String.class)
            fin,content=AbstractReplacement.gazelleReplace(content,debut,fin,strWithoutP[indexAt:],self.replacement)
            return importChanged,content
        else:#found annoataio withou package declaration eg :@CollectionOfElements(targetElement = java.lang.String.class)
            fin,content=AbstractReplacement.gazelleReplace(content,debut,fin,strWithoutP[indexAt+1:],self.replacement[self.replacement.rfind(".")+1:])
            if (not importChanged):
                elementStr=strWithoutP[strWithoutP.find("@")+1:] # eg :CollectionOfElements
                regex = re.compile("import[\s]+[\w.]+"+elementStr)  #!!!!!!!!!!!!!!!!! problem multiple match !!!!!!!!!!!!!!!!!!!!!!!!!!! 
                result= regex.search(content)
                if result:
                    debutImport,finImport=result.span()
                    matchImport=result.group() # eg :import org.hibernate.annotations.CollectionOfElements
                    importStr=matchImport[7:] #eg :org.hibernate.annotations.CollectionOfElements
                    newImportStr=self.replacement[1:] #eg :javax.persistence.ElementCollection
                    finImport,content=AbstractReplacement.gazelleReplace(content,debutImport,finImport,importStr,newImportStr)
                else:
                    print ("import not found for match "+match)
                return True,content
            else:
                return importChanged,content


    

class ClassReplacement(AbstractReplacement):

    def __init__(self,regex, replacement):
        AbstractReplacement.__init__(self, regex,replacement)

class MethodReplacement(AbstractReplacement): #!!!!!!!!!!!!!!probleme surcharge de methode !!!!!!!!!!
    def __init__(self,regex, replacement):
        AbstractReplacement.__init__(self, regex,replacement) 



