"""module for Xhtml file migration"""
#!/usr/bin/python3
# -*-coding:utf-8 -*
from lxml import etree as ET
from migration.richfaces.action.script_rich import RichElement
from migration.richfaces.action.script_a4j import A4jElement
import re
class XhtmlTransformation:
    """upgrade to jsf 2.1 and richfaces 4.3.6"""
    def new_xhtml(cls, root):
        """replace http://richfaces.ajax4jsf.org/rich tag by http://richfaces.org/rich"""
        basestring = (str, bytes)
        for el in root.iter():
            if isinstance(el.tag, basestring):
                el.tag = str(el.tag).replace("http://richfaces.ajax4jsf.org/rich", "http://richfaces.org/rich")
                el.tag = str(el.tag).replace("http://jboss.com/products/seam/taglib", "http://jboss.org/schema/seam/taglib")
        return root
    new_xhtml = classmethod(new_xhtml)
    doctype = None
    changeDoctype = False
    def is_rich_element(cls, tag):
        """return True  if the tag is a rich:tag"""
        tag = str(tag)
        return tag.startswith("{http://richfaces.org/rich}")
    is_rich_element = classmethod(is_rich_element)
    def is_a4j_element(cls, tag):
        """return True  if the tag is a a4j:tag"""
        tag = str(tag)
        return tag.startswith("{http://richfaces.org/a4j}")
    is_a4j_element = classmethod(is_a4j_element)
    def replace_modal_panel(cls, text, show, file_path, element, tree):
        """replace Api call for modal modal panel wit new one"""
        result = re.search(r"Richfaces\."+show+r"ModalPanel\(.*?\)", text)
        while result:
            match = result.group()
            virgule_pos = match.find(",")
            if virgule_pos == -1:
                text = text.replace(match, "#{rich:component("+match[25:match.__len__()-1]+")}."+show+"()")
            else:
                modal_panel = match[25:virgule_pos]
                json = match[virgule_pos+1:match.__len__()-2]   
                print(json+" found at element "+tree.getpath(element)+" in "+file_path+" please use  #{rich:component("+modal_panel+")}.resize(width, height);and #{rich:component("+modal_panel+")}.moveTo(top, left); to correct the issue")
                text = text.replace(match, "#{rich:component("+modal_panel+")}."+show+"()")
            result = re.search(r"Richfaces\."+show+r"ModalPanel\(.*?\)", text)
        return text
    replace_modal_panel = classmethod(replace_modal_panel)
    def common_attribute_change(cls, element, file_path, tree):
        """replace atribute/value for both a4j and richfaces """
        for key, value in element.attrib.items():
            if key == "reRender":
                element.set("render", value)
                element.attrib.pop("reRender")
            elif key == "ajaxSingle":
                if value == "true":
                    element.set("execute", "@this")
                element.attrib.pop("ajaxSingle")
            elif key == "limitToList":
                element.set("limitRender", value)
                element.attrib.pop("limitToList")
            # elif key in ["ignoreDupResponse", "requestDelay", "timeout"]:
            #     child = ET.Element("{http://richfaces.org/a4j}attachQueue")
            #     child.set(key, value)
            #     element.append(child)
            elif key == "process":
                element.set("execute", value)
                element.attrib.pop("process")
            elif key == "event":
                if value.startswith("on"):
                    value = value[2:]
                    element.set(key, value)
                if value == "viewactivated":
                    element.set(key, "change")
                if value == "changed":
                    element.set(key, "change")
            elif key.startswith("on")or key == "href":
                text = element.get(key)
                text = cls.replace_modal_panel(text, "show", file_path, element, tree)
                text = cls.replace_modal_panel(text, "hide", file_path, element, tree)
                element.set(key, text)
        return element
    common_attribute_change = classmethod(common_attribute_change)
    def change_nsmap(cls, tree, keys):
        """update nameSpace map and save doctype"""
        root = tree.getroot()
        cls.doctype = tree.docinfo.doctype
        NSMAP = root.nsmap
        for key, ns in keys:
            NSMAP[key] = ns;
        NSMAP["g"] = "http://www.ihe.net/gazelle"
        NSMAP["gdk"] = "http://www.ihe.net/gazellecdk"
        root = XhtmlTransformation.new_xhtml(root)
        new_root = ET.Element(root.tag, nsmap=NSMAP)
        for key, value in root.attrib.items():
            new_root.set(key, value)
        new_root.text = root.text
        for element in root:
            new_root.append(element)
        tree._setroot(new_root)
        if not tree.docinfo.doctype == cls.doctype:
            cls.changeDoctype = True
        return tree
    change_nsmap = classmethod(change_nsmap)
    def upgrade(cls, file_path):
        """parse the Xhtml file and apply the change according to the tag"""
        print(file_path)
        A4jElement.subviewId = 1
        cls.changeDoctype = False
        parser = ET.XMLParser(remove_blank_text=True, resolve_entities=False)
        tree = ET.parse(file_path, parser)
        root = tree.getroot()
        inv_nsmap = {root.nsmap[k] : k for k in root.nsmap}
        xmlns_keys = list()
        key_rich = inv_nsmap.get("http://richfaces.ajax4jsf.org/rich")
        key_seam = inv_nsmap.get("http://jboss.com/products/seam/taglib")
        if key_rich != None :
            xmlns_keys.append((key_rich, "http://richfaces.org/rich"))
        if key_seam != None:
            xmlns_keys.append((key_seam, "http://jboss.org/schema/seam/taglib"))
        if xmlns_keys:
            tree = XhtmlTransformation.change_nsmap(tree, xmlns_keys)
            root = tree.getroot()
        for element in root.iter():
            element = XhtmlTransformation.common_attribute_change(element, file_path, tree)
            if element.tag == "{http://www.w3.org/1999/xhtml}body":
                #change <body> to <h:body>
                element.tag = "{http://java.sun.com/jsf/html}body"
            elif element.tag == "{http://www.w3.org/1999/xhtml}head":
                element.tag = "{http://java.sun.com/jsf/html}head"
            elif XhtmlTransformation.is_rich_element(element.tag):
                RichElement.componant_change(element)
            elif XhtmlTransformation.is_a4j_element(element.tag):
                A4jElement.componant_change(element, file_path)
            elif element.tag == "{http://java.sun.com/jsf/facelets}include":
                src = element.get("viewId")
                if src:
                    element.set("src", src)
                    element.attrib.pop("viewId")
            # elif element.tag is ET.Comment:
            #     if 'rich:spacer xmlns:rich = "http://richfaces.org/rich"' in element.text:
            #         element1 = ET.fromstring(element.text)
            #         element1.tag = "{http://www.ihe.net/gazellecdk}spacer"
            #         parent = element.getparent()
            #         parent.insert(parent.index(element), element1)
            #         parent.remove(element)
        tree.write(file_path, pretty_print=True, encoding='utf-8')
        if cls.changeDoctype:
            cls.add_doc_type(file_path)
    upgrade = classmethod(upgrade)
    def add_doc_type(cls, file_path):
        """add docype to xhtml"""
        #changing nsmap leads to remove doctype
        f = open(file_path, "r")
        content = f.read()
        f.close()
        content = cls.doctype+"\n"+content
        f = open(file_path, "w")
        f.write(content)
        f.close()
    add_doc_type = classmethod(add_doc_type)
