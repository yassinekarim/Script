#!/opt/python3/bin/python3 
# -*-coding:utf-8 -*
from lxml import etree as ET
from migration.richfaces.action.script_rich import RichElement
from migration.richfaces.action.script_a4j import A4jElement
class XhtmlTransformation:
    """upgrade to jsf 2.1 and richfaces 4.3.6"""
    def newXhtml(cls,root):
        """replace http://richfaces.ajax4jsf.org/rich tag by http://richfaces.org/rich"""
        basestring = (str,bytes)
        for el in root.iter():
            if isinstance(el.tag, basestring):
                el.tag=str(el.tag).replace("http://richfaces.ajax4jsf.org/rich","http://richfaces.org/rich")
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
    def commonAttributeChange(cls,element):
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
        """parse the Xhtml file and apply the change according to the tag+"""
        print (filePath)
        parser = ET.XMLParser(remove_blank_text=True,resolve_entities=False)
        tree = ET.parse(filePath,parser)
        root=tree.getroot()
        inv_nsmap = {root.nsmap[k] : k for k in root.nsmap}
        if(inv_nsmap.get("http://richfaces.ajax4jsf.org/rich")!=None ):
            tree=XhtmlTransformation.changeNsmap(tree,inv_nsmap.get("http://richfaces.ajax4jsf.org/rich"))
            root=tree.getroot()
        for element in root.iter():
            if(element.tag=="{http://www.w3.org/1999/xhtml}body"):
                element.tag="{http://java.sun.com/jsf/html}body"  #change <body> to <h:body> 
            elif(element.tag=="{http://www.w3.org/1999/xhtml}head"):
                element.tag="{http://java.sun.com/jsf/html}head"
            elif(XhtmlTransformation.isRich(element.tag)):
                element=XhtmlTransformation.commonAttributeChange(element)
                element=RichElement.componantChange(element)
            elif(XhtmlTransformation.isA4J(element.tag)):
                element=XhtmlTransformation.commonAttributeChange(element)
                element=A4jElement.componantChange(element,filePath)
        tree.write(filePath,pretty_print=True,encoding='utf-8')
    upgrade=classmethod(upgrade)