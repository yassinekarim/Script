#!/opt/python3/bin/python3
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
        parent=element.getparent()
        while (parent.tag != "{http://java.sun.com/jsf/core}facet"):
            parent=parent.getparent()
        return parent
    getFacetParent=classmethod(getFacetParent)
    def componantChange(cls,element):
        """migrate rich components """
        #richfaces Validation
        if (element.tag== cls.richNs+"ajaxValidator"):
            element.tag=cls.richNs+"validator"
        elif (element.tag== cls.richNs+"beanValidator"):
            element.tag="{http://java.sun.com/jsf/core}validateBean"
            # comment=ET.Comment(ET.tostring(element))
            # parent=element.getparent()
            # parent.insert(parent.index(element),comment)
            # parent.remove(element)
        #richfaces Input Components
        elif (element.tag== cls.richNs+"calendar"):
            # comment=ET.Comment(ET.tostring(element))
            # parent=element.getparent()
            # parent.insert(parent.index(element),comment)
            # parent.remove(element)
            print ("method in client side API renamed")
        elif (element.tag== cls.richNs+"colorPicker"):
            comment=ET.Comment(ET.tostring(element))
            parent=element.getparent()
            parent.insert(parent.index(element),comment)
            parent.remove(element)
            print("colorPicker not implemented (custom component)")
        elif (element.tag== cls.richNs+"comboBox"):
            element.tag=cls.richNs+"select"
            element.set("enableManualInput","true")
            print ("select Unified version of suggestionBox and comboBox from 3.3.x.")
        elif (element.tag== cls.richNs+"editor"):
            script=ET.Element("{http://www.w3.org/1999/xhtml}script")
            script.set("type","text/javascript")
            script.text="window.CKEDITOR_BASEPATH = '#{request.contextPath}/org.richfaces.resources/javax.faces.resource/org.richfaces.ckeditor/'"
            parent=element.getparent()
            parent.insert(0,script)
            print ("you should configure rich editor manually see home.xhtml in simmulaor common for a sample")
        elif (element.tag== cls.richNs+"fileUpload"):
            pass
        elif (element.tag in [cls.richNs+"inplaceInput",cls.richNs+"inplaceSelect"]):
            if(element.get("onviewactivated")):
                element.set("onchange",element.get("onviewactivated"))
                element.attrib.pop("onviewactivated")
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
        #Rich Panel/Output Components
        elif (element.tag== cls.richNs+"modalPanel"):
            element.tag=cls.richNs+"popupPanel"
            if(element.get("showWhenRendered")):
                element.set("show",element.get("showWhenRendered"))
                element.attrib.pop("showWhenRendered") 
        elif (element.tag in [cls.richNs+"panelBar",cls.richNs+"panelBarItem"]):
            element.tag=element.tag.replace("panelBar","accordion")
        elif (element.tag== cls.richNs+"panelMenu"):
            if(element.get("ValueChangeListener")):
                element.set("itemchangeListener",element.get("ValueChangeListener"))
                element.attrib.pop("ValueChangeListener")
        elif (element.tag== cls.richNs+"separator"):
            element.tag=cls.xhtmlNs+"hr"
        elif (element.tag== cls.richNs+"simpleTogglePanel"):
            element.tag=cls.richNs+"collapsiblePanel"
        elif (element.tag == cls.richNs+"tabPanel"):
            element=RichElement.migrateValueChangeAttribute(element)
        elif (element.tag == cls.richNs+"tab"):
            element=RichElement.migrateValueChangeAttribute(element)
            if(element.get("label")):
                element.set("header",element.get("label"))
                element.attrib.pop("label")
        elif (element.tag== cls.richNs+"togglePanel"):
            RichElement.migrateValueChangeAttribute(element)
        elif (element.tag== cls.richNs+"facets"):
            element.tag=cls.richNs+"togglePanelItem"
            element=RichElement.migrateValueChangeAttribute(element)
        elif (element.tag== cls.richNs+"toggleControl"):
            if(element.get("targetItem") is None):
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
        elif (element.tag== cls.richNs+"toolBar"):
            element.tag=cls.richNs+"toolbar"
        elif (element.tag== cls.richNs+"toolBarGroup"):
            element.tag=cls.richNs+"toolbarGroup"
        elif (element.tag== cls.richNs+"toolTip"):
            element.tag=cls.richNs+"tooltip"
        #Rich Menu Components
        elif (element.tag== cls.richNs+"menuItem"):
            if(element.get("value")):
                element.set("label",element.get("value"))
                element.attrib.pop("value")
        elif (element.tag== cls.richNs+"menuGroup"):
            if(element.get("value")):
                element.set("label",element.get("value"))
                element.attrib.pop("value")
        elif (element.tag== cls.richNs+"menuSeparator"):
            pass
        #Rich Ordering Components
        elif (element.tag== cls.richNs+"listShuttle"):
            element.tag=cls.richNs+"pickList"
            print ("""The RF 3 listShuttle and pickList components were merged into the single pickList comopnent with RichFaces 4
    Note: The sourceList is not longer mutable, and is available only by subtraacting the target list from thh complete list.""")
        #Rich Iteration Components
        elif (element.tag== cls.richNs+"column"):
            element.tag="{http://www.ihe.net/gazelle}column"
            sortOrder=element.get("sortOrder")
            if(sortOrder):
                element.set("sortOrder",sortOrder.lower())
            if(element[0].tag=="{http://java.sun.com/jsf/core}facet"):
                element[0].tag="{http://java.sun.com/jsf/facelets}define"
        elif (element.tag== cls.richNs+"columnGroup"):
            element.tag=cls.richNs+"columnGroup"
        elif (element.tag== cls.richNs+"columns"):
            comment=ET.Comment(ET.tostring(element))
            parent=element.getparent()
            parent.insert(parent.index(element),comment)
            parent.remove(element)
            print ("columns not implemented")
        elif (element.tag== cls.richNs+"dataOrderingList"):
            element.tag=cls.richNs+"list"
            element.set("type","ordered")
        elif (element.tag== cls.richNs+"dataDefinitionList"):
            element.tag=cls.richNs+"list"
            element.set("type","definitions")
        elif (element.tag== cls.richNs+"dataList"):
            element.tag=cls.richNs+"list"
            element.set("type","unordered")
        elif (element.tag== cls.richNs+"dataFilterSlider"):
            comment=ET.Comment(ET.tostring(element))
            parent=element.getparent()
            parent.insert(parent.index(element),comment)
            parent.remove(element)
            print ("dataFilterSlider not implemented")
        elif (element.tag== cls.richNs+"datascroller"):
            element.tag=cls.richNs+"dataScroller"
        elif (element.tag== cls.richNs+"dataTable"):
            pass
        elif(element.tag==cls.richNs+"subTable"):
            element.tag=cls.richNs+"collapsibleSubTable"
        elif(element.tag==cls.richNs+"scrollableDataTable"):
            element.tag=cls.richNs+"extendedDataTable"
        #Rich Tree Components
        elif(element.tag==cls.richNs+"tree"):
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
                        if(child.tag!=cls.richNs+"tree"or key!="var" )
                        child.attrib[key]=value.replace(var,var+".data")
            if(element.get("treeNodeVar")):
                element.set("var",element.get("treeNodeVar"))
                element.attrib.pop("treeNodeVar")
        elif(element.tag==cls.richNs+"treeNode"):
            if(element.get("icon")):
                element.set("iconExpanded",element.get("icon"))
                element.set("iconCollapsed",element.get("icon"))
                element.attrib.pop("icon")
        elif(element.tag==cls.richNs+"treeNodesAdaptor"):
            element.tag=cls.richNs+"treeModelAdaptor"
        elif (element.tag==cls.richNs+"recursiveTreeNodesAdaptor"):
            element.tag=cls.richNs+"treeModelRecursiveAdaptor"
        # Rich Drag'n'Drop Components
        elif(element.tag==cls.richNs+"dragSupport"):
            element.tag=cls.richNs+"dragSource"
            if(element.get("DragType")):
                element.set("type",element.get("DragType"))
                element.attrib.pop("DragType")
        elif (element.tag==cls.richNs+"dropSupport"):
            element.tag=cls.richNs+"dropTarget"
        elif(element.tag==cls.richNs+"dndParam"):
            comment=ET.Comment(ET.tostring(element))
            parent=element.getparent()
            parent.insert(parent.index(element),comment)
            parent.remove(element)
            print ("dndParam : not implemented")
        # Rich Miscellaneous Components
        elif(element.tag==cls.richNs+"effect"):
            comment=ET.Comment(ET.tostring(element))
            parent=element.getparent()
            parent.insert(parent.index(element),comment)
            parent.remove(element)
            print ("effect : not implemented")
        elif (element.tag==cls.richNs+"gmap"):
            comment=ET.Comment(ET.tostring(element))
            parent=element.getparent()
            parent.insert(parent.index(element),comment)
            parent.remove(element)
            print ("gmap : not implemented")
        elif(element.tag==cls.richNs+"insert"):
            element.tag="{http://www.ihe.net/gazellecdk}insert"
        elif(element.tag==cls.richNs+"page"):
            comment=ET.Comment(ET.tostring(element))
            parent=element.getparent()
            parent.insert(parent.index(element),comment)
            parent.remove(element)
            print ("page : not implemented")
        elif(element.tag==cls.richNs+"virtualEarth"):
            comment=ET.Comment(ET.tostring(element))
            parent=element.getparent()
            parent.insert(parent.index(element),comment)
            parent.remove(element)
            print ("virtualEarth : not implemented")
        elif(element.tag==cls.richNs+"spacer"):
            element.tag="{http://www.ihe.net/gazellecdk}spacer"
        return element
    componantChange=classmethod(componantChange)