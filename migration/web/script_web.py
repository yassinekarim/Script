"""module for web.xml migration"""
#!/usr/bin/python3
# -*-coding:utf-8 -*
from lxml import etree as ET
from migration.utils.change_definition import ChangeDefinition
from migration.components.action.script_ejb import Search4Ejb
class WebMigration:
    """this class contains method for web.xml migration"""
    project_file_path = ""
    file_path = ""
    def update_resteasy_param(cls, element,jndi_list):
        param_value = element.find("{http://java.sun.com/xml/ns/javaee}param-value")
        param_values = param_value.text.strip().split(',')
        new_jndi_list = list()
        for old_jndi in param_values:
            old_jndi = old_jndi[:old_jndi.__len__()-6]
            old_jndi = old_jndi[old_jndi.rfind('/')+1:]
            new_jndi = [s for s in [jndi_tuple[0] for jndi_tuple in jndi_list] if old_jndi in s]
            new_jndi_list.append(new_jndi[0])
        param_value.text = ','.join(new_jndi_list)
    update_resteasy_param = classmethod(update_resteasy_param)
    def update_jndi(cls):
        """update resteasy jndi using the parsed log"""
        parser = ET.XMLParser(remove_blank_text=True, load_dtd=True)
        tree = ET.parse(cls.file_path, parser)
        root = tree.getroot()
        jndi_list = Search4Ejb.jndi_list
        for element in root:
            if element.tag == "{http://java.sun.com/xml/ns/javaee}context-param":
                param_name = element.find("{http://java.sun.com/xml/ns/javaee}param-name")
                if param_name.text == "resteasy.jndi.resources":
                    cls.update_resteasy_param(element,jndi_list)
        tree.write(cls.file_path, pretty_print=True, encoding='utf-8', xml_declaration=True)
    update_jndi = classmethod(update_jndi)
    def context_param_migration(cls,element,ressource_optimisation):
        """context param migration"""
        param_name = element.find("{http://java.sun.com/xml/ns/javaee}param-name")
        param_value = element.find("{http://java.sun.com/xml/ns/javaee}param-value")
        if param_name.text == "org.richfaces.SKIN":
            param_name.text = "org.richfaces.skin"
            if param_value.text == "laguna":
                param_value.text = "blueSky"
        elif param_name.text == "org.richfaces.BASE_SKIN":
            param_name.text = "org.richfaces.baseSkin"
        elif param_name.text == "org.richfaces.CONTROL_SKINNING":
            param_name.text = "org.richfaces.enableControlSkinning"
            if param_value.text == "disable":
                param_value.text = "false"
            else:
                param_value.text = "true"
        elif param_name.text == "org.richfaces.CONTROL_SKINNING_CLASSES":
            param_name.text = "org.richfaces.enableControlSkinningClasses"
            if param_value.text == "disable":
                param_value.text = "false"
            else:
                param_value.text = "true"
        elif param_name.text == "org.richfaces.CONTROL_SKINNING_LEVEL":
            element.getparent().remove(element)
        elif param_name.text == "org.richfaces.LoadScriptStrategy" or param_name.text == "org.richfaces.LoadStyleStrategy":
            if ressource_optimisation:
                element.getparent().remove(element)
            else:
                param_name.text = "org.richfaces.resourceOptimization.enabled"
                ressource_optimisation = True
                if param_value.text == "ALL":
                    param_value.text = "true"
                else:
                    param_value.text = "false"
        return ressource_optimisation
    context_param_migration = classmethod(context_param_migration)
    def parse_xml(cls, file_path):
        """parse the web.xml update definition, richfaces context-param and add richfaces recources servlet"""
        if cls.project_file_path in file_path:
            cls.file_path = file_path
        parser = ET.XMLParser(remove_blank_text=True, load_dtd=True)
        tree = ET.parse(file_path, parser)
        tree = ChangeDefinition.changedefinition(tree)
        root = tree.getroot()
        ressource_optimisation = False
        ressoure_servlet = False
        for element in root:
            if element.tag == "{http://java.sun.com/xml/ns/javaee}context-param":
                ressource_optimisation=cls.context_param_migration(element,ressource_optimisation)
            elif not ressoure_servlet and element.tag == "{http://java.sun.com/xml/ns/javaee}servlet-mapping":
                ressoure_servlet = True
                servlet = ET.fromstring("""<servlet>
<servlet-name>Resource Servlet</servlet-name>
<servlet-class>org.richfaces.webapp.ResourceServlet</servlet-class>
<load-on-startup>1</load-on-startup>
</servlet>""")
                servletMapping = ET.fromstring("""<servlet-mapping>
<servlet-name>Resource Servlet</servlet-name>
<url-pattern>/org.richfaces.resources/*</url-pattern>
</servlet-mapping>""")
                parent = element.getparent()
                index = parent.index(element)
                parent.insert(index+1, servlet)
                parent.insert(index+2, servletMapping)
        tree.write(file_path, pretty_print=True, encoding='utf-8', xml_declaration=True)
    parse_xml = classmethod(parse_xml)
