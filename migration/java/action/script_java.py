"""script to parse java file"""
#!/usr/bin/python3
# -*-coding:utf-8 -*
from migration.java.model.replacement import MethodReplacement
import re
class JavaTransformation:
    """migration function for java file replace old code(annotation/function/instruction) by the upgraded code according to a list of(regex, replacement)"""
    replacement_list = None
    def get_replacement_list(cls):
        """getter for the java replacements list costructed from conf file"""
        return cls.replacement_list
    get_replacement_list = classmethod(get_replacement_list)
    def add_method(cls,it,content):
        """add mehod get id for previous matches"""
        offset = 0
        for result in it:
            match = result.group()
            class_match = match[match.find('<')+1:match.__len__()-1]
            class_match = class_match.strip()
            if class_match.__len__()>1:
                if "extend" in match:
                    fin = content.rfind('}')
                    content = content[:fin]+"""@Override
        protected Object getId("""+class_match+""" t) {
        // TODO Auto-generated method stub
        return t.getId();
        }""" +content[fin-1:]
                else:
                    debut, fin = result.span()
                    tmp = content[debut+offset:]
                    index = tmp.find(";")
                    method = """{
                    @Override
        protected Object getId("""+class_match+""" t) {
        // TODO Auto-generated method stub
        return t.getId();
        }
        }"""
                    tmp = tmp[:index]+method+tmp[index:]
                    content = content[:debut+offset]+tmp
                    offset += method.__len__()
        return content
    add_method = classmethod(add_method)
    def search_datamodel(cls, content):
        """seach for class that extend or instanciate FilterDataModel/HibernateDataModel"""
        regex_list = [r"extends[\s]*FilterDataModel[\s]*<.+>", r"extends[\s]*HibernateDataModel[\s]*<.+>", r"new[\s]*FilterDataModel[\s]*<.+>", r"new[\s]*HibernateDataModel[\s]*<.+>"]
        for reg in regex_list:
            regex = re.compile(reg)
            it = regex.finditer(content)
            content = cls.add_method(it,content)
        return content
    search_datamodel = classmethod(search_datamodel)
    def upgrade_code(cls, content):
        """return the upgraded code as a string"""
        for element in JavaTransformation.replacement_list:
            content = element.execute_replace(content)
        content = cls.search_datamodel(content)
        return content
    upgrade_code = classmethod(upgrade_code)
    def re_init_method_list(cls):
        """re initialize method list for each new parsed file """
        for element in JavaTransformation.replacement_list:
            if isinstance(element, MethodReplacement ):
                element.apply_change = False
    re_init_method_list = classmethod(re_init_method_list)
    def parse_java(cls, file_path):
        """read the java file and replace it's content with the upgraded content"""
        f = open(file_path, "r")
        content = f.read()
        f.close()
        content = JavaTransformation.upgrade_code(content)
        JavaTransformation.re_init_method_list()
        f = open(file_path, "w")
        f.write(content)
        f.close()
    parse_java = classmethod(parse_java)
