#!/usr/bin/python3
# -*-coding:utf-8 -*
from lxml import etree as ET


class RichElement:
    """upgrade rich tag"""

    richNs="{http://richfaces.org/rich}"
    hNs="{http://java.sun.com/jsf/html}"
    xhtmlNs="{http://www.w3.org/1999/xhtml}"  
    def migrateValueChangeAttribute(cls,element):
        """migrate value change attribute a common attribute to some rich tag"""
        if(element.get("ValueChangeListener")):
            element.set("itemchangeListener",element.get("ValueChangeListener"))
            element.attrib.pop("ValueChangeListener")
        if(element.get("ValueChangeEvent")):
            element.set("ItemChangeEvent",element.get("ValueChangeEvent"))
            element.attrib.pop("ValueChangeEvent")
        return element
    migrateValueChangeAttribute=classmethod(migrateValueChangeAttribute)
    def getFacetParent(cls,element):
        """return first parent facet tag of the element"""
        parent=element.getparent()
        while (parent.tag != "{http://java.sun.com/jsf/core}facet"):
            parent=parent.getparent()
        return parent
    getFacetParent=classmethod(getFacetParent)
    def richValidation(cls,element):
        """migration of validation components"""
        if (element.tag== cls.richNs+"ajaxValidator"):
            element.tag=cls.richNs+"validator"
            return True
        elif (element.tag== cls.richNs+"beanValidator"):
            element.tag="{http://java.sun.com/jsf/core}validateBean"
            return True
            # comment=ET.Comment(ET.tostring(element))
            # parent=element.getparent()
            # parent.insert(parent.index(element),comment)
            # parent.remove(element)
        return False
    richValidation=classmethod(richValidation)
    def richInput(cls,element):
        """migration of input components"""
        if (element.tag== cls.richNs+"calendar"):
            # comment=ET.Comment(ET.tostring(element))
            # parent=element.getparent()
            # parent.insert(parent.index(element),comment)
            # parent.remove(element)
            print ("method in client side API renamed")
            return True
        elif (element.tag== cls.richNs+"colorPicker"):
            comment=ET.Comment(ET.tostring(element))
            parent=element.getparent()
            parent.insert(parent.index(element),comment)
            parent.remove(element)
            print("colorPicker not implemented (custom component)")
            return True
        elif (element.tag== cls.richNs+"comboBox"):
            element.tag=cls.richNs+"select"
            element.set("enableManualInput","true")
            print ("select Unified version of suggestionBox and comboBox from 3.3.x.")
            return True
        elif (element.tag== cls.richNs+"editor"):
            script=ET.Element("{http://www.w3.org/1999/xhtml}script")
            script.set("type","text/javascript")
            script.text="window.CKEDITOR_BASEPATH = '#{request.contextPath}/org.richfaces.resources/javax.faces.resource/org.richfaces.ckeditor/'"
            parent=element.getparent()
            parent.insert(0,script)
            print ("you should configure rich editor manually see home.xhtml in simmulator common for a sample")
            return True
        elif (element.tag== cls.richNs+"fileUpload"):
            return True
        elif (element.tag in [cls.richNs+"inplaceInput",cls.richNs+"inplaceSelect"]):
            if(element.get("onviewactivated")):
                element.set("onchange",element.get("onviewactivated"))
                element.attrib.pop("onviewactivated")
            return True
        elif (element.tag== cls.richNs+"suggestionbox"):
            element.tag=cls.richNs+"autocomplete"
            if(element.get("suggestionAction")):
                element.set("autocompleteMethod",element.get("suggestionAction"))
                element.attrib.pop("suggestionAction")
            selfRendered=element.get("selfRendered")
            if(selfRendered is not None and selfRendered =="true"):
                element.set("mode","cachedAjax")
            else:
                element.set("mode","ajax")
            if(selfRendered is not None):
                element.attrib.pop("selfRendered")
            print ("autoComplete Unified version of suggestionBox and comboBox from 3.3.x.")
            return True
        return False
    richInput=classmethod(richInput)
    def richOutput(cls,element):
        """migration of output/panel components"""
        if (element.tag== cls.richNs+"modalPanel"):
            element.tag=cls.richNs+"popupPanel"
            if(element.get("showWhenRendered")):
                element.set("show",element.get("showWhenRendered"))
                element.attrib.pop("showWhenRendered")
            return True
        elif (element.tag in [cls.richNs+"panelBar",cls.richNs+"panelBarItem"]):
            element.tag=element.tag.replace("panelBar","accordion")
            return True
        elif (element.tag== cls.richNs+"panelMenu"):
            if(element.get("ValueChangeListener")):
                element.set("itemchangeListener",element.get("ValueChangeListener"))
                element.attrib.pop("ValueChangeListener")
            return True
        elif (element.tag== cls.richNs+"separator"):
            element.tag=cls.xhtmlNs+"hr"
            return True
        elif (element.tag== cls.richNs+"simpleTogglePanel"):
            element.tag=cls.richNs+"collapsiblePanel"
            return True
        elif (element.tag == cls.richNs+"tabPanel"):
            element=RichElement.migrateValueChangeAttribute(element)
            return True
        elif (element.tag == cls.richNs+"tab"):
            element=RichElement.migrateValueChangeAttribute(element)
            if(element.get("label")):
                element.set("header",element.get("label"))
                element.attrib.pop("label")
            return True
        elif (element.tag== cls.richNs+"togglePanel"):
            RichElement.migrateValueChangeAttribute(element)
            return True
        elif (element.tag== cls.richNs+"facets"):
            element.tag=cls.richNs+"togglePanelItem"
            element=RichElement.migrateValueChangeAttribute(element)
            return True
        elif (element.tag== cls.richNs+"toggleControl"):
            if(element.get("targetItem") is None and element.get("switchToState") is not None ):
                element=RichElement.migrateValueChangeAttribute(element)
                element.set("targetItem",element.get("switchToState"))
                element.attrib.pop("switchToState")
                facet=cls.getFacetParent(element)
                facet.tag=cls.richNs+"togglePanelItem"
                iD=element.get("id")
                style=element.get("style")
                value=element.get("value")
                link=ET.Element(cls.hNs+"commandLink")
                if(iD is not None):
                    link.set("id",iD)
                    element.attrib.pop("id")
                if(style is not None):
                    link.set("style",style)
                    element.attrib.pop("style")
                if(value is not None):
                    link.set("value",value)
                    element.attrib.pop("value")
                parent=element.getparent()
                parent.insert(parent.index(element),link)
                link.append(element)
                # parent.remove(element)
            return True
        elif (element.tag== cls.richNs+"toolBar"):
            element.tag=cls.richNs+"toolbar"
            return True
        elif (element.tag== cls.richNs+"toolBarGroup"):
            element.tag=cls.richNs+"toolbarGroup"
            return True
        elif (element.tag== cls.richNs+"toolTip"):
            element.tag=cls.richNs+"tooltip"
            return True
        return False
    richOutput=classmethod(richOutput)
    def richMenu(cls,element):
        """migration of Menu components"""
        if (element.tag== cls.richNs+"menuItem"):
            if(element.get("value")):
                element.set("label",element.get("value"))
                element.attrib.pop("value")
            return True
        elif (element.tag== cls.richNs+"menuGroup"):
            if(element.get("value")):
                element.set("label",element.get("value"))
                element.attrib.pop("value")
            return True
        elif (element.tag== cls.richNs+"menuSeparator"):
            return True
        return False
    richMenu=classmethod(richMenu)
    def richOrdering(cls,element):
        """migration of ordering components"""
        if (element.tag== cls.richNs+"listShuttle"):
            element.tag=cls.richNs+"pickList"
            print ("""The RF 3 listShuttle and pickList components were merged into the single pickList comopnent with RichFaces 4
    Note: The sourceList is not longer mutable, and is available only by subtraacting the target list from thh complete list.""")
            return True
        #Rich Iteration Components
        elif (element.tag== cls.richNs+"column"):
            element.tag="{http://www.ihe.net/gazelle}column"
            sortOrder=element.get("sortOrder")
            if(sortOrder):
                element.set("sortOrder",sortOrder.lower())
            if(element[0].tag=="{http://java.sun.com/jsf/core}facet"):
                element[0].tag="{http://java.sun.com/jsf/facelets}define"
            return True
        elif (element.tag== cls.richNs+"columnGroup"):
            element.tag=cls.richNs+"columnGroup"
            return True
        elif (element.tag== cls.richNs+"columns"):
            comment=ET.Comment(ET.tostring(element))
            parent=element.getparent()
            parent.insert(parent.index(element),comment)
            parent.remove(element)
            print ("columns not implemented")
            return True
        elif (element.tag== cls.richNs+"dataOrderingList"):
            element.tag=cls.richNs+"list"
            element.set("type","ordered")
            return True
        elif (element.tag== cls.richNs+"dataDefinitionList"):
            element.tag=cls.richNs+"list"
            element.set("type","definitions")
            return True
        elif (element.tag== cls.richNs+"dataList"):
            element.tag=cls.richNs+"list"
            element.set("type","unordered")
            return True
        elif (element.tag== cls.richNs+"dataFilterSlider"):
            comment=ET.Comment(ET.tostring(element))
            parent=element.getparent()
            parent.insert(parent.index(element),comment)
            parent.remove(element)
            print ("dataFilterSlider not implemented")
            return True
        elif (element.tag== cls.richNs+"datascroller"):
            element.tag=cls.richNs+"dataScroller"
            return True
        elif (element.tag== cls.richNs+"dataTable"):
            return True
        elif(element.tag==cls.richNs+"subTable"):
            element.tag=cls.richNs+"collapsibleSubTable"
            return True
        elif(element.tag==cls.richNs+"scrollableDataTable"):
            element.tag=cls.richNs+"extendedDataTable"
            return True
        return False
    richOrdering=classmethod(richOrdering)
    def richTree(cls,element):
        """migration of tree components"""
        if(element.tag==cls.richNs+"tree"):
            if(element.get("nodeFace")):
                element.set("nodeType",element.get("nodeFace"))
                element.attrib.pop("nodeFace")
            if(element.get("switchType")):
                element.set("toggleType",element.get("switchType"))
                element.attrib.pop("switchType")
            var=element.get("var")
            if(var is not None):
                for child in element.iter():
                    for key,value in child.attrib.items():
                        if(child.tag!=cls.richNs+"tree"or key!="var" ):
                            child.attrib[key]=value.replace(var,var+".data")
            if(element.get("treeNodeVar")):
                element.set("var",element.get("treeNodeVar"))
                element.attrib.pop("treeNodeVar")
            return True
        elif(element.tag==cls.richNs+"treeNode"):
            if(element.get("icon")):
                element.set("iconExpanded",element.get("icon"))
                element.set("iconCollapsed",element.get("icon"))
                element.attrib.pop("icon")
            return True
        elif(element.tag==cls.richNs+"treeNodesAdaptor"):
            element.tag=cls.richNs+"treeModelAdaptor"
            return True
        elif (element.tag==cls.richNs+"recursiveTreeNodesAdaptor"):
            element.tag=cls.richNs+"treeModelRecursiveAdaptor"
            return True
        return False
    richTree=classmethod(richTree)
    def richDND(cls,element):
        """migration of drag and drop components"""
        if(element.tag==cls.richNs+"dragSupport"):
            element.tag=cls.richNs+"dragSource"
            if(element.get("DragType")):
                element.set("type",element.get("DragType"))
                element.attrib.pop("DragType")
            return True
        elif (element.tag==cls.richNs+"dropSupport"):
            element.tag=cls.richNs+"dropTarget"
            return True
        elif(element.tag==cls.richNs+"dndParam"):
            comment=ET.Comment(ET.tostring(element))
            parent=element.getparent()
            parent.insert(parent.index(element),comment)
            parent.remove(element)
            print ("dndParam : not implemented")
            return True
        return False
    richDND=classmethod(richDND)
    def richMiscellaneous(cls,element):
        """migration of Miscellaneous components"""
        if(element.tag==cls.richNs+"effect"):
            comment=ET.Comment(ET.tostring(element))
            parent=element.getparent()
            parent.insert(parent.index(element),comment)
            parent.remove(element)
            print ("effect : not implemented")
            return True
        elif (element.tag==cls.richNs+"gmap"):
            comment=ET.Comment(ET.tostring(element))
            parent=element.getparent()
            parent.insert(parent.index(element),comment)
            parent.remove(element)
            print ("gmap : not implemented")
            return True
        elif(element.tag==cls.richNs+"insert"):
            element.tag="{http://www.ihe.net/gazellecdk}insert"
            return True
        elif(element.tag==cls.richNs+"page"):
            comment=ET.Comment(ET.tostring(element))
            parent=element.getparent()
            parent.insert(parent.index(element),comment)
            parent.remove(element)
            print ("page : not implemented")
            return True
        elif(element.tag==cls.richNs+"virtualEarth"):
            comment=ET.Comment(ET.tostring(element))
            parent=element.getparent()
            parent.insert(parent.index(element),comment)
            parent.remove(element)
            print ("virtualEarth : not implemented")
            return True
        elif(element.tag==cls.richNs+"spacer"):
            element.tag="{http://www.ihe.net/gazellecdk}spacer"
            return True
        return False
    richMiscellaneous=classmethod(richMiscellaneous)

    def componantChange(cls,element):
        """migrate rich components """
        if (cls.richValidation(element)==True):
            return
        elif (cls.richInput(element)==True):
            return
        elif (cls.richOutput(element)==True):
            return
        elif (cls.richMenu(element)==True):
            return
        elif (cls.richOrdering(element)==True):
            return
        elif (cls.richTree(element)==True):
            return
        elif (cls.richDND(element)==True):
            return
        elif (cls.richMiscellaneous(element)==True):
            return
    componantChange=classmethod(componantChange)

