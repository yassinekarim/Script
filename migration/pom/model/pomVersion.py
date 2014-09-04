"""module for pom configuraion classes"""
#!/usr/bin/python3
# -*-coding:utf-8 -*
class Plugin:
    """model for Plugin dependencies """
    def __init__(self, artifact_id, version):
        """constructor for Plugin Class"""
        self.artifact_id = artifact_id
        self.version = version
    def execute_replace(self, element):
        """replace the version tag"""
        version = element.find("xmlns:version", namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
        if version is not None:
            version.text = self.version
