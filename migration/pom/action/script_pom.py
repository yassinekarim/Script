"""pom migration module"""
#!/usr/bin/python3
# -*-coding:utf-8 -*
from lxml import etree as ET
import os
BASESTRING = (str, bytes)
class PomMigration:
    pluginVersionList = None
    def get_plugin_version_list(cls):
        """getter for pom configuration list"""
        return cls.pluginVersionList
    get_plugin_version_list = classmethod(get_plugin_version_list)
    def create_dep(cls, group_id, artifact_id, version, scope):
        """create a new dependencies element """
        newdep = ET.Element("{http://maven.apache.org/POM/4.0.0}dependency")
        group_id_tag = ET.Element("{http://maven.apache.org/POM/4.0.0}groupId")
        group_id_tag.text = group_id
        newdep.append(group_id_tag)
        artifact_id_tag = ET.Element("{http://maven.apache.org/POM/4.0.0}artifactId")
        artifact_id_tag.text = artifact_id
        newdep.append(artifact_id_tag)
        if scope is not None:
            scope_tag = ET.Element("{http://maven.apache.org/POM/4.0.0}scope")
            scope_tag.text = scope
            newdep.append(scope_tag)
        if version is not None:
            version_tag = ET.Element("{http://maven.apache.org/POM/4.0.0}version")
            version_tag.text = version
            newdep.append(version_tag)
        return newdep
    create_dep = classmethod(create_dep)
    def new_dep(cls, element, group_id, artifact_id, vers):
        """if version is set update version"""
        version = element.find("{http://maven.apache.org/POM/4.0.0}version")
        if version != None:
            version = vers
        scope = element.find("{http://maven.apache.org/POM/4.0.0}scope")
        if scope != None:
            scope = scope.text
        return cls.create_dep(group_id, artifact_id, version, scope)
    new_dep = classmethod(new_dep)
    def find_version(cls, file_path, artifact_id):
        """parse parent pom to find version of artifactId"""
        parser = ET.XMLParser(remove_blank_text=True)
        tree = ET.parse(file_path, parser)
        root = tree.getroot()
        version = root.find("xmlns:version", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
        if version is not None:
            return version.text
        else:
            relativepath = root.find("xmlns:parent/xmlns:relativepath", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
            if relativepath is not None:
                absolute_file_path = os.path.abspath(file_path)
                project_path = absolute_file_path[:absolute_file_path.rfind("/")]
                old_path = os.getcwd()
                os.chdir(project_path)
                tmp = cls.find_version(relativepath.text, artifact_id)
                os.chdir(old_path)
                return tmp
            else:
                version_text = input("version of "+artifact_id+" cannot be determined please enter the version")
                return version_text
    find_version = classmethod(find_version)
    def verify_pom(cls, file_path, artifact_id):
        """verify if the entered project folder correspont to the expected artifact"""
        parser = ET.XMLParser(remove_blank_text=True)
        tree = ET.parse(file_path, parser)
        root = tree.getroot()
        artifact_id_tag = root.find("xmlns:artifactId", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
        if artifact_id_tag.text != artifact_id:
            print("error: in "+file_path+"  expected artifactId "+artifact_id+" found "+artifact_id_tag.text)
            return ""
        return cls.find_version(file_path, artifact_id)
    verify_pom = classmethod(verify_pom)
    def get_project_path(cls, artifact_id):
        """ask from the user the project path for artifactId and verify if the given path is correct"""
        project_path = input('Please enter the path to the project directory :')
        while not os.path.exists(project_path) and not os.path.isdir(project_path):
            print(project_path+" does not exist on disk or isn't a dir")
            project_path = input('Please enter the path to the project directory :')
        pom_file_path = os.path.join(project_path, "pom.xml")
        if not os.path.isfile(pom_file_path):
            print("error: no pom found in "+project_path)
            return cls.get_project_path(artifact_id)
        tmp = cls.verify_pom(pom_file_path, artifact_id)
        if tmp == "":
            return cls.get_project_path(artifact_id)
        return project_path
    get_project_path = classmethod(get_project_path)
    def parse_xml(cls, file_path):
        """parse pom.xml to change dependecies version"""
        parser = ET.XMLParser(remove_blank_text=True)
        tree = ET.parse(file_path, parser)
        root = tree.getroot()
        dependencies = root.findall("xmlns:dependencies/xmlns:dependency", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
        plugins = root.findall("xmlns:build/xmlns:plugins/xmlns:plugin", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
        richfaces = False
        jsf_impl = False
        is_ear = False
        packaging = root.find("{http://maven.apache.org/POM/4.0.0}packaging")
        if packaging is not None and packaging.text == "ear":
            is_ear = True
        for element in plugins:
            if isinstance(element.tag, BASESTRING):
                artifact_id = element.find("xmlns:artifactId", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text
                for plugin in cls.pluginVersionList:
                    if plugin.artifact_id == artifact_id:
                        plugin.execute_replace(element)
                        break
                if artifact_id == "maven-ear-plugin":
                    configuration = element.find("xmlns:configuration", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
                    jboss = configuration.find("xmlns:jboss", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
                    if jboss is not None:
                        version = jboss.find("xmlns:version", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
                        if version is not None:
                            if version.text == "5":
                                version.text = "6"
                            configuration.append(version)
                        configuration.remove(jboss)
        for element in dependencies:
            if isinstance(element.tag, BASESTRING):
                if "org.apache.maven.plugins" in element.find("xmlns:groupId", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text:
                    artifact_id = element.find("xmlns:artifactId", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text
                    for plugin in cls.pluginVersionList:
                        if plugin.artifact_id == artifact_id:
                            plugin.execute_replace(element)
                            break
                elif "org.richfaces." in element.find("xmlns:groupId", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text:
                    parent = element.getparent()
                    if not richfaces:
                        newdep = cls.new_dep(element, "org.richfaces.ui", "richfaces-components-ui", "4.3.6.Final")
                        parent.append(newdep)
                        newdep = cls.new_dep(element, "org.richfaces.core", "richfaces-core-impl", "4.3.6.Final")
                        parent.append(newdep)
                        richfaces = True
                    parent.remove(element)
                elif "com.sun.facelets" == element.find("xmlns:groupId", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text:
                    parent = element.getparent()
                    if not jsf_impl:
                        newdep = cls.new_dep(element, "com.sun.faces", "jsf-impl", "2.1.7-jbossorg-2")
                        parent.append(newdep)
                        jsf_impl = True
                    parent.remove(element)
                elif "jsf-impl" == element.find("xmlns:artifactId", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text:
                    parent = element.getparent()
                    if not jsf_impl:
                        newdep = cls.new_dep(element, "com.sun.faces", "jsf-impl", "2.1.7-jbossorg-2")
                        parent.append(newdep)
                        jsf_impl = True
                    parent.remove(element)
                elif "jsf-api" == element.find("xmlns:artifactId", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text:
                    parent = element.getparent()
                    newdep = cls.new_dep(element, "org.jboss.spec.javax.faces", "jboss-jsf-api_2.1_spec", "2.1.19.1.Final")
                    parent.append(newdep)
                    parent.remove(element)
                elif "javax.ejb" == element.find("xmlns:groupId", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text:
                    parent = element.getparent()
                    newdep = cls.new_dep(element, "org.jboss.spec.javax.ejb", "jboss-ejb-api_3.1_spec", "1.0.1.Final")
                    parent.append(newdep)
                    parent.remove(element)
                elif "hibernate-annotations" == element.find("xmlns:artifactId", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text:
                    parent = element.getparent()
                    newdep = cls.new_dep(element, "org.hibernate", "hibernate-core", "4.0.1.Final")
                    parent.append(newdep)
                    parent.remove(element)
                elif "jboss-seam-jul" == element.find("xmlns:artifactId", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text:
                    parent = element.getparent()
                    parent.remove(element)
                elif "ejb3-persistence" == element.find("xmlns:artifactId", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text:
                    parent = element.getparent()
                    parent.remove(element)
                elif "org.hibernate" == element.find("xmlns:groupId", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text:
                    version = element.find("xmlns:version", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
                    if version is not None:
                        element.remove(version)
                elif "javax.persistence" == element.find("xmlns:groupId", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text:
                    parent = element.getparent()
                    newdep = cls.new_dep(element, "org.hibernate.javax.persistence", "hibernate-jpa-2.0-api", "1.0.1.Final")
                    parent.append(newdep)
                    parent.remove(element)
                elif "drools-api" == element.find("xmlns:artifactId", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text:
                    parent = element.getparent()
                    parent.remove(element)
                elif "jbpm-jpdl" == element.find("xmlns:artifactId", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text:
                    parent = element.getparent()
                    parent.remove(element)
                elif "net.ihe.gazelle" in element.find("xmlns:groupId", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'}).text:
                    artifact_id = element.find("xmlns:artifactId", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
                    version = element.find("xmlns:version", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
                    dep_type = element.find("xmlns:type", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
                    if dep_type is not None and dep_type.text == "ejb":
                        is_migrated = input('is the project with artifactId = '+artifact_id.text+' already migrated answer yes if the project directory is a subfolder of the parent project(y/n) [y]')or 'y'
                        while is_migrated != 'y'and is_migrated != 'n':
                            print('incorect input try again:')
                            is_migrated = input('is the project with artifactId = '+artifact_id.text+' already migrated answer yes if the project directory is a subfolder of the parent project(y/n) [y]')or 'y'
                        if is_migrated == 'y':
                            if version is not None:
                                version_text = input('Please enter the version of the migrated project ['+version.text+']') or version.text
                                version.text = version_text
                        else:
                            from migration.main import Main
                            project_path = cls.get_project_path(artifact_id.text)
                            print(project_path)
                            Main.walk(project_path)
        tree.write(file_path, pretty_print=True, encoding='utf-8', xml_declaration=True)
        return is_ear
    parse_xml = classmethod(parse_xml)