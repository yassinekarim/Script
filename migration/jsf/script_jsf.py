#!/opt/python3/bin/python3 
# -*-coding:utf-8 -*
from lxml import etree as ET
from migration.richfaces.action.script_rich import RichElement
from migration.richfaces.action.script_a4j import A4jElement
import re
class XhtmlTransformation:
    """upgrade to jsf 2.1 and richfaces 4.3.6"""
    def newXhtml(cls,root):
        """replace http://richfaces.ajax4jsf.org/rich tag by http://richfaces.org/rich"""
        basestring = (str,bytes)
        for el in root.iter():
            if isinstance(el.tag, basestring):
                el.tag=str(el.tag).replace("http://richfaces.ajax4jsf.org/rich","http://richfaces.org/rich")
                el.tag=str(el.tag).replace("http://jboss.com/products/seam/taglib","http://jboss.org/schema/seam/taglib")
        return root
    newXhtml = classmethod(newXhtml)
    def isRich(cls,tag):
        """return True  if the tag is a rich:tag"""
        tag=str(tag)
        return tag.startswith("{http://richfaces.org/rich}")
    isRich = classmethod(isRich)
    def isA4J(cls,tag):
        """return True  if the tag is a a4j:tag"""
        tag=str(tag)
        return tag.startswith("{http://richfaces.org/a4j}")
    isA4J = classmethod(isA4J)
    def replaceModalPanel(cls,text,show,filePath,element,tree):
        result= re.search("Richfaces\."+show+"ModalPanel\(.*?\)",text)
        while result:
            match=result.group()
            vPos=match.find(",")
            if(vPos==-1):
                text=text.replace(match,"#{rich:component("+match[25:match.__len__()-1]+")}."+show+"()")
            else:
                modalPanel=match[25:vPos]
                json=match[vPos+1:match.__len__()-2]
                print(json+" found at element "+tree.getpath(element)+" in "+filePath+" please use  #{rich:component("+modalPanel+")}.resize(width,height);and #{rich:component("+modalPanel+")}.moveTo(top,left); to correct the issue")
                text=text.replace(match,"#{rich:component("+modalPanel+")}."+show+"()")
            result= re.search("Richfaces\."+show+"ModalPanel\(.*?\)",text)
        return text
    replaceModalPanel=classmethod(replaceModalPanel)
    def commonAttributeChange(cls,element,filePath,tree):
        """replace atribute/value for both a4j and richfaces """
        for key, value in element.attrib.items():
            if (key=="reRender"):
                element.set("render",value)
                element.attrib.pop("reRender")
            elif(key=="ajaxSingle"):
                if(value=="true"):
                    element.set("execute","@this")
                element.attrib.pop("ajaxSingle")
            elif (key=="limitToList"):
                element.set("limitRender",value)
                element.attrib.pop("limitToList")
            elif(key in ["ignoreDupResponse","requestDelay","timeout"]):
                child = ET.Element("{http://richfaces.org/a4j}attachQueue")
                child.set(key,value)
                element.append(child)
            elif(key=="process"):
                element.set("execute",value)
                element.attrib.pop("process")
            elif(key=="event"):
                if key.startswith("on"):
                    element.set(key,value[2:])
            elif(key.startswith("on")or key=="href"):
                text=element.get(key)
                text=cls.replaceModalPanel(text,"show",filePath,element,tree)
                text=cls.replaceModalPanel(text,"hide",filePath,element,tree)
                element.set(key,text)
        return element
    commonAttributeChange = classmethod(commonAttributeChange)
    def changeNsmap(cls,tree,key):
        """update nameSpace map """
        root=tree.getroot()
        NSMAP=root.nsmap
        NSMAP[key]="http://richfaces.org/rich"
        root=XhtmlTransformation.newXhtml(root)
        newRoot = ET.Element(root.tag, nsmap=NSMAP)
        
        for key,value in root.attrib.items():
            newRoot.set(key,value)
        
        newRoot.text=root.text
        for element in root:
            newRoot.append(element)
        tree._setroot(newRoot)
        return tree
    changeNsmap = classmethod(changeNsmap)
    def upgrade(cls, filePath):
        """parse the Xhtml file and apply the change according to the tag"""
        print(filePath)
        parser = ET.XMLParser(remove_blank_text=True,resolve_entities=False)
        tree = ET.parse(filePath,parser)
        root=tree.getroot()
        inv_nsmap = {root.nsmap[k] : k for k in root.nsmap}
        xmlnsKeys=list()
        keyRich=inv_nsmap.get("http://richfaces.ajax4jsf.org/rich")
        keySeam=inv_nsmap.get("http://jboss.com/products/seam/taglib")
        if(keyRich!=None ):
            xmlnsKeys.append((keyRich,"http://richfaces.org/rich"))
        if(keySeam!=None):
            xmlnsKeys.append((keySeam,"http://jboss.org/schema/seam/taglib"))
        if(xmlnsKeys):
            tree=XhtmlTransformation.changeNsmap(tree,xmlnsKeys)
            root=tree.getroot()
        for element in root.iter():
            element=XhtmlTransformation.commonAttributeChange(element,filePath,tree)
            if(element.tag=="{http://www.w3.org/1999/xhtml}body"):
                element.tag="{http://java.sun.com/jsf/html}body"  #change <body> to <h:body> 
            elif(element.tag=="{http://www.w3.org/1999/xhtml}head"):
                element.tag="{http://java.sun.com/jsf/html}head"
            elif(XhtmlTransformation.isRich(element.tag)):
                element=RichElement.componantChange(element)
            elif(XhtmlTransformation.isA4J(element.tag)):
                element=A4jElement.componantChange(element,filePath)
        tree.write(filePath,pretty_print=True,encoding='utf-8')
    upgrade=classmethod(upgrade)