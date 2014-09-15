"""module for model java classes"""
#!/usr/bin/python3
# -*-coding:utf-8 -*
import re
class AbstractReplacement:
    """abstract class for java replacement"""
    def __init__(self, regex, replacement, mapping):
        """abstract constructor"""
        self.regex = regex
        self.replacement = replacement
        self.mapping = mapping
    def gazelle_replace(cls, content, debut, fin, old, new):
        """replace old by new in content without having to search in the whole file and update fin accordingly"""
        content = content[:debut]+content[debut:fin].replace(old, new, 1)+content[fin:]
        offset = new.__len__()-old.__len__()
        return offset, content
    gazelle_replace = classmethod(gazelle_replace)
    def change_mapping(self, content, debut, fin):
        """mapping is a list of(oldParameter, newParameter) if oldparameter is found in content[debut:fin] it will be replaced by newParameter and fin updated accordingly"""
        offset = 0
        for old, new in self.mapping:
            if old == new:
                continue
            regex = re.compile(old)
            result = regex.search(content[debut:fin])
            if result:
                tmp, content = AbstractReplacement.gazelle_replace(content, debut, fin, old, new)
                offset += tmp
        return offset, content
    def change_code(self, match, content, debut, fin, import_changed):
        """ replace code and ad import if necessay"""
        #remove white spaces from the border of the string
        match = match.strip()
        point_index = match.find(".")
        offset, content = self.change_mapping(content, debut, fin)
        fin += offset
        if point_index != -1:
            #found annotation with package declaration eg: @org.hibernate.annotations.CollectionOfElements(targetElement = java.lang.String.class)
            tmp, content = AbstractReplacement.gazelle_replace(content, debut, fin, match, self.replacement)
            offset += tmp
            return offset, import_changed, content
        else:
            #found annoataio withou package declaration eg :@CollectionOfElements(targetElement = java.lang.String.class)
            if not import_changed:
                element_str = match
                # eg :CollectionOfElements
                regex = re.compile(r"import[\s]+[\w.]+"+element_str)
                result = regex.search(content)
                if result:
                    tmp, content = AbstractReplacement.gazelle_replace(content, debut, fin, match, self.replacement[self.replacement.rfind(".")+1:])
                    offset += tmp
                    debut_import, fin_import = result.span()
                    # eg :import org.hibernate.annotations.CollectionOfElements
                    match_import = result.group()
                    #eg :org.hibernate.annotations.CollectionOfElements
                    import_str = match_import[7:]
                    #eg :javax.persistence.ElementCollection
                    new_import_str = self.replacement
                    tmp, content = AbstractReplacement.gazelle_replace(content, debut_import, fin_import, import_str, new_import_str)
                    offset += tmp
                else:
                    print("import not found for match "+match)
                    return offset, import_changed, content
                return offset, True, content
            else:
                tmp, content = AbstractReplacement.gazelle_replace(content, debut, fin, match, self.replacement[self.replacement.rfind(".")+1:])
                offset += tmp
                return offset, import_changed, content
    def execute_replace(self, content):
        """find all occurence of the regex and call change_code to change them one by one """
        regex = re.compile(self.regex, re.MULTILINE)
        iterator = regex.finditer(content)
        import_changed = False
        offset = 0
        for result in iterator:
            debut, fin = result.span()
            debut += offset
            fin += offset
            match = result.group()
            tmp, import_changed, content = self.change_code(match, content, debut, fin, import_changed)
            offset += tmp
        return content
class AnnotationReplacement(AbstractReplacement):
    """model for Anotation"""
    def __init__(self, regex, replacement, mapping):
        """constructor for annotation replacement"""
        AbstractReplacement.__init__(self, regex, replacement, mapping)
    def change_code(self, match, content, debut, fin, import_changed):
        """change the annotation, import and the parameter of the annotation """
        index_parenthese = match.find("(")
        str_without_p = match[:index_parenthese if index_parenthese != -1 else match.__len__()]
        #remove white spaces from the right of the string
        str_without_p = str_without_p.rstrip()
        point_index = str_without_p.find(".")
        index_at = match.find("@")
        offset, content = self.change_mapping(content, debut, fin)
        fin += offset
        if point_index != -1:
            #found annotation with package declaration eg: @org.hibernate.annotations.CollectionOfElements(targetElement = java.lang.String.class)
            tmp, content = AbstractReplacement.gazelle_replace(content, debut, fin, str_without_p[index_at:], self.replacement)
            offset += tmp
            return offset, import_changed, content
        else:
            #found annotation without package declaration eg :@CollectionOfElements(targetElement = java.lang.String.class)
            if not import_changed:
                # eg :CollectionOfElements
                element_str = str_without_p[str_without_p.find("@")+1:]
                regex = re.compile(r"import[\s]+[\w.]+"+element_str)
                result = regex.search(content)
                if result is not None:
                    tmp, content = AbstractReplacement.gazelle_replace(content, debut, fin, str_without_p[index_at+1:], self.replacement[self.replacement.rfind(".")+1:])
                    offset += tmp
                    debut_import, fin_import = result.span()
                    # eg :import org.hibernate.annotations.CollectionOfElements
                    match_import = result.group()
                    #eg :org.hibernate.annotations.CollectionOfElements
                    import_str = match_import[7:]
                    #eg :javax.persistence.ElementCollection
                    new_import_str = self.replacement[1:]
                    tmp, content = AbstractReplacement.gazelle_replace(content, debut_import, fin_import, import_str, new_import_str)
                    offset += tmp
                else:
                    print("import not found for match "+match)
                    return offset, False, content
                return offset, True, content
            else:
                tmp, content = AbstractReplacement.gazelle_replace(content, debut, fin, str_without_p[index_at+1:], self.replacement[self.replacement.rfind(".")+1:])
                offset += tmp
                return offset, import_changed, content
class MethodReplacement(AbstractReplacement):
    """define change of code for method remplacement"""
    def __init__(self, regex, replacement, apply_change, mapping):
        """constructor for method replacement"""
        AbstractReplacement.__init__(self, regex, replacement, mapping)
        self.apply_change = apply_change
    def change_code(self, match, content, debut, fin, import_changed):
        """if the apply change  is set to true call parent change_code else do nothing"""
        if self.apply_change:
            return super().change_code(match, content, debut, fin, True)
        else:
            return 0, True, content
class ClassReplacement(AbstractReplacement):
    """define change of code for a class remplacement"""
    def __init__(self, regex, replacement, method_change, mapping):
        """constructor for class replacement"""
        AbstractReplacement.__init__(self, regex, replacement, mapping)
        self.method_change = method_change
    def execute_replace(self, content):
        """find all occurence of the regex and call change_code to change them one by one """
        regex = re.compile(self.regex, re.MULTILINE)
        iterator = regex.finditer(content)
        import_changed = False
        regex_match = False
        offset = 0
        for result in iterator:
            debut, fin = result.span()
            debut = debut+offset
            fin = fin+offset
            match = result.group()
            tmp, import_changed, content = self.change_code(match, content, debut, fin+13, import_changed)
            offset += tmp
            regex_match = True
        if regex_match == True:
            from migration.java.action.script_java import JavaTransformation
            replacement_list = JavaTransformation.get_replacement_list()
            for element in replacement_list:
                if isinstance(element, MethodReplacement ) and element.regex in self.method_change:
                    element.apply_change = True
        return content
