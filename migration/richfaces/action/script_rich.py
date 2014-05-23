#!/opt/python3/bin/python3 
# -*-coding:utf-8 -*
from lxml import etree as ET

richNs="{http://richfaces.org/rich}"
hNs="{http://java.sun.com/jsf/html}"
xhtmlNs="{http://www.w3.org/1999/xhtml}"

def MigrateValueChangeAttribute(element):
    if(element.get("ValueChangeListener")):
        element.set("itemchangeListener",element.get("ValueChangeListner"))
        element.attrib.pop("itemchangeListener")
    if(element.get("ValueChangeEvent")):
        element.set("ItemChangeEvent",element.get("ValueChangeEvent"))
        element.attrib.pop("ItemChangeEvent")


def richComponantChange(element):

    #richfaces Valisation
    if (element.tag== richNs+"ajaxValidator"):
        element.tag=richNs+"validator"
    elif (element.tag== richNs+"beanValidator"):
        element.tag==hNs+"validateBean"
        print ("summary not supported")

    #richfaces Input Components
    elif (element.tag== richNs+"calendar"):
        print ("method in client side API renamed")
    elif (element.tag== richNs+"colorPicker"):
        print("colorPicker not implemented (custom component)")
    elif (element.tag== richNs+"comboBox"):
        element.tag=richNs+"autocomplete"
        print ("autoComplete Unified version of suggestionBox and comboBox from 3.3.x.")
    elif (element.tag== richNs+"editor"):
        print ("not sure if editor works")
    elif (element.tag== richNs+"fileUpload"):
        print ("")
    elif (element.tag in [richNs+"inplaceInput",richNs+"inplaceSelect"]):
        if(element.get("onviewactivated")):
            element.set("onchange",element.get("onviewactivated"))
            element.attrib.pop("onviewactivated")
        
    elif (element.tag== richNs+"suggestionBox"):
        element.tag=richNs+"autocomplete"
        print ("autoComplete Unified version of suggestionBox and comboBox from 3.3.x.")
    #Rich Panel/Output Components
    elif (element.tag== richNs+"modalPanel"):
        element.tag=richNs+"popupPanel"
        if(element.get("showWhenRendered")):
            element.set("show",element.get("showWhenRendered"))
            element.attrib.pop("showWhenRendered") 
    elif (element.tag in [richNs+"panelBar",richNs+"panelBarItem"]):
        element.tag=element.tag.replace("panelBar","accordion")
    elif (element.tag== richNs+"panelMenu"):
        if(element.get("ValueChangeListener")):
            element.set("itemchangeListener",element.get("ValueChangeListner"))
            element.attrib.pop("itemchangeListener")
    elif (element.tag== richNs+"separator"):
        element.tag=xhtmlNs+"hr"
    elif (element.tag== richNs+"simpleTogglePanel"):
        element.tag==richNs+"collapsiblePanel"
    elif (element.tag in [richNs+"tabPanel",richNs+"tab"]):
        MigrateValueChangeAttribute(element)
    elif (element.tag== richNs+"togglePanel"):
        MigrateValueChangeAttribute(element)
    elif (element.tag== richNs+"facets"):
        element.tag=richNs+"togglePanelItem"
        MigrateValueChangeAttribute(element)
    elif (element.tag== richNs+"toggleControl"):
        MigrateValueChangeAttribute(element)
    elif (element.tag== richNs+"toolBar"):
        element.tag=richNs+"toolbar"
    elif (element.tag== richNs+"toolBarGroup"):
        element.tag=richNs+"toolbarGroup"
    elif (element.tag== richNs+"toolTip"):
        element.tag=richNs+"tooltip"
    #Rich Ordering Components
    elif (element.tag== richNs+"listShuttle"):
        element.tag=richNs+"pickList"
        print ("""The RF 3 listShuttle and pickList components were merged into the single pickList comopnent with RichFaces 4
Note: The sourceList is not longer mutable, and is available only by subtraacting the target list from thh complete list.""")
    #Rich Iteration Components
    elif (element.tag== richNs+"column"):
        element.tag=richNs+"column"
    elif (element.tag== richNs+"columnGroup"):
        element.tag=richNs+"columnGroup"
    elif (element.tag== richNs+"column"):
        element.tag=richNs+"column"
    elif (element.tag== richNs+"columns"):
        print ("columns not implemented")
    elif (element.tag== richNs+"dataOrderingList"):
        element.tag=richNs+"list"
        element.set("type","ordered")
    elif (element.tag== richNs+"dataDefinitionList"):
        element.tag=richNs+"list"
        element.set("type","definitions")
    elif (element.tag== richNs+"dataList"):
        element.tag=richNs+"list"
        element.set("type","unordered")
    elif (element.tag== richNs+"dataFilterSlider"):
        print ("dataFilterSlider not implemented")
    elif (element.tag== richNs+"datascroller"):
        element.tag=richNs+"dataScroller"
    elif (element.tag== richNs+"dataTable"):
        print ("dataTable : built i sorting/filtering not suppored")
    elif(element.tag==richNs+"subTable"):
        element.tag=richNs+"collapsibleSubTable"
    elif(element.tag==richNs+"scrollableDataTable"):
        element.tag=richNs+"extendedDataTable"
    #Rich Tree Components
    elif(element.tag==richNs+"treeNodesAdaptor"):
        element.tag=richNs+"treeModelAdaptor"
    elif (element.tag==richNs+"recursiveTreeNodesAdaptor"):
        element.tag=richNs+"treeModelRecursiveAdaptor"
    # Rich Drag'n'Drop Components
    elif(element.tag==richNs+"dragSupport"):
        element.tag=richNs+"dragSource"
    elif (element.tag==richNs+"dropSupport"):
        element.tag=richNs+"dropTarget"
    elif(element.tag==richNs+"dndParam"):
        print ("dndParam : not implemented")
    # Rich Miscellaneous Components
    elif(element.tag==richNs+"effect"):
        print ("effect : not implemented")
    elif (element.tag==richNs+"gmap"):
        print ("gmap : not implemented")
    elif(element.tag==richNs+"insert"):
        print ("insert : use syntax highlighter custom component")
    elif(element.tag==richNs+"page"):
        print ("page : not implemented")
    elif(element.tag==richNs+"virtualEarth"):
        print ("virtualEarth : not implemented")