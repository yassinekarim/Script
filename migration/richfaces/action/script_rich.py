#!/opt/python3/bin/python3 
# -*-coding:utf-8 -*
from lxml import etree as ET


class RichElement:
    """docstring for RichElement"""

    richNs="{http://richfaces.org/rich}"
    hNs="{http://java.sun.com/jsf/html}"
    xhtmlNs="{http://www.w3.org/1999/xhtml}"  
    def migrateValueChangeAttribute(cls,element):
        if(element.get("ValueChangeListener")):
            element.set("itemchangeListener",element.get("ValueChangeListner"))
            element.attrib.pop("itemchangeListener")
        if(element.get("ValueChangeEvent")):
            element.set("ItemChangeEvent",element.get("ValueChangeEvent"))
            element.attrib.pop("ItemChangeEvent")
    migrateValueChangeAttribute=classmethod(migrateValueChangeAttribute)

    def componantChange(cls,element):
        #richfaces Valisation
        if (element.tag== cls.richNs+"ajaxValidator"):
            element.tag=cls.richNs+"validator"
        elif (element.tag== cls.richNs+"beanValidator"):
            element.tag==cls.hNs+"validateBean"
            print ("summary not supported")
        #richfaces Input Components
        elif (element.tag== cls.richNs+"calendar"):
            print ("method in client side API renamed")
        elif (element.tag== cls.richNs+"colorPicker"):
            print("colorPicker not implemented (custom component)")
        elif (element.tag== cls.richNs+"comboBox"):
            element.tag=cls.richNs+"autocomplete"
            print ("autoComplete Unified version of suggestionBox and comboBox from 3.3.x.")
        elif (element.tag== cls.richNs+"editor"):
            print ("not sure if editor works")
        elif (element.tag== cls.richNs+"fileUpload"):
            print ("")
        elif (element.tag in [cls.richNs+"inplaceInput",cls.richNs+"inplaceSelect"]):
            if(element.get("onviewactivated")):
                element.set("onchange",element.get("onviewactivated"))
                element.attrib.pop("onviewactivated")
        elif (element.tag== cls.richNs+"suggestionBox"):
            element.tag=cls.richNs+"autocomplete"
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
                element.set("itemchangeListener",element.get("ValueChangeListner"))
                element.attrib.pop("itemchangeListener")
        elif (element.tag== cls.richNs+"separator"):
            element.tag=cls.xhtmlNs+"hr"
        elif (element.tag== cls.richNs+"simpleTogglePanel"):
            element.tag==cls.richNs+"collapsiblePanel"
        elif (element.tag in [cls.richNs+"tabPanel",cls.richNs+"tab"]):
            RichElement.migrateValueChangeAttribute(element)
        elif (element.tag== cls.richNs+"togglePanel"):
            RichElement.migrateValueChangeAttribute(element)
        elif (element.tag== cls.richNs+"facets"):
            element.tag=cls.richNs+"togglePanelItem"
            RichElement.migrateValueChangeAttribute(element)
        elif (element.tag== cls.richNs+"toggleControl"):
            RichElement.MigrateValueChangeAttribute(element)
        elif (element.tag== cls.richNs+"toolBar"):
            element.tag=cls.richNs+"toolbar"
        elif (element.tag== cls.richNs+"toolBarGroup"):
            element.tag=cls.richNs+"toolbarGroup"
        elif (element.tag== cls.richNs+"toolTip"):
            element.tag=cls.richNs+"tooltip"
        #Rich Ordering Components
        elif (element.tag== cls.richNs+"listShuttle"):
            element.tag=cls.richNs+"pickList"
            print ("""The RF 3 listShuttle and pickList components were merged into the single pickList comopnent with RichFaces 4
    Note: The sourceList is not longer mutable, and is available only by subtraacting the target list from thh complete list.""")
        #Rich Iteration Components
        elif (element.tag== cls.richNs+"column"):
            element.tag=cls.richNs+"column"
        elif (element.tag== cls.richNs+"columnGroup"):
            element.tag=cls.richNs+"columnGroup"
        elif (element.tag== cls.richNs+"column"):
            element.tag=cls.richNs+"column"
        elif (element.tag== cls.richNs+"columns"):
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
            print ("dataFilterSlider not implemented")
        elif (element.tag== cls.richNs+"datascroller"):
            element.tag=cls.richNs+"dataScroller"
        elif (element.tag== cls.richNs+"dataTable"):
            print ("dataTable : built i sorting/filtering not suppored")
        elif(element.tag==cls.richNs+"subTable"):
            element.tag=cls.richNs+"collapsibleSubTable"
        elif(element.tag==cls.richNs+"scrollableDataTable"):
            element.tag=cls.richNs+"extendedDataTable"
        #Rich Tree Components
        elif(element.tag==cls.richNs+"treeNodesAdaptor"):
            element.tag=cls.richNs+"treeModelAdaptor"
        elif (element.tag==cls.richNs+"recursiveTreeNodesAdaptor"):
            element.tag=cls.richNs+"treeModelRecursiveAdaptor"
        # Rich Drag'n'Drop Components
        elif(element.tag==cls.richNs+"dragSupport"):
            element.tag=cls.richNs+"dragSource"
        elif (element.tag==cls.richNs+"dropSupport"):
            element.tag=cls.richNs+"dropTarget"
        elif(element.tag==cls.richNs+"dndParam"):
            print ("dndParam : not implemented")
        # Rich Miscellaneous Components
        elif(element.tag==cls.richNs+"effect"):
            print ("effect : not implemented")
        elif (element.tag==cls.richNs+"gmap"):
            print ("gmap : not implemented")
        elif(element.tag==cls.richNs+"insert"):
            print ("insert : use syntax highlighter custom component")
        elif(element.tag==cls.richNs+"page"):
            print ("page : not implemented")
        elif(element.tag==cls.richNs+"virtualEarth"):
            print ("virtualEarth : not implemented")
    componantChange=classmethod(componantChange)