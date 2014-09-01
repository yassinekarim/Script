#!/usr/bin/python3
# -*-coding:utf-8 -*

class Plugin:
    def __init__(self,artifactId,version):
        self.artifactId = artifactId
        self.version = version
    def executeReplace(self,element):
        """replace the version tag"""
        version=element.find("xmlns:version",namespaces={'xmlns': 'http://maven.apache.org/POM/4.0.0'})
        if (version is not None):
            version.text=self.version
