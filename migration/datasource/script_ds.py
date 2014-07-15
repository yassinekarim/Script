#!/opt/python3/bin/python3
# -*-coding:utf-8 -*
import sys
from lxml import etree as ET
from migration.utils.jndiMigration import JndiMigration
import os
import subprocess
basestring = (str,bytes)

class DataSourceMigration:
    
    def parseXml(cls,filePath):
        """parse *-ds.xml to change for the new version"""
        parser = ET.XMLParser(remove_blank_text=True)
        tree = ET.parse(filePath,parser)
        root = tree.getroot()
        localTxDatasource=root.find("local-tx-datasource")
        jndiName=localTxDatasource.find("jndi-name")
        connectionUrl=localTxDatasource.find("connectionUrl")
        userName=localTxDatasource.find("user-name")
        password=localTxDatasource.find("password")
        minPoolSize=localTxDatasource.find("min-pool-size")
        maxPoolSize=localTxDatasource.find("max-pool-size")
        idleTimeoutMinutes=localTxDatasource.find("idle-timeout-minutes")
        preparedStatementCacheSize=localTxDatasource.find("prepared-statement-cache-size")
        blockingTimeoutMillis=localTxDatasource.find("blocking-timeout-millis")
        newConnectionSql=localTxDatasource.find("new-connection-sql")
        checkValidConnectionSql=localTxDatasource.find("check-valid-connection-sql")
        newRoot = ET.Element("{http://www.jboss.org/ironjacamar/schema}datasources")
        datasource=ET.Element("{http://www.jboss.org/ironjacamar/schema}datasource")
        datasource.set("jta","true")
        datasource.set("enabled","true")
        datasource.set("use-java-context","true")
        datasource.set("pool-name",jndiName.text)
        datasource.set("jndi-name",JndiMigration.changeJndiDS(jndiName.text,"jboss"))
        security=ET.Element("{http://www.jboss.org/ironjacamar/schema}security")
        userName.tag="{http://www.jboss.org/ironjacamar/schema}user-name"
        password.tag="{http://www.jboss.org/ironjacamar/schema}password"
        security.append(userName)
        security.append(password)
        datasource.append(security)
        pool=ET.Element("{http://www.jboss.org/ironjacamar/schema}pool")
        minPoolSize.tag="{http://www.jboss.org/ironjacamar/schema}min-pool-size"
        maxPoolSize.tag="{http://www.jboss.org/ironjacamar/schema}max-pool-size"
        prefill=ET.Element("{http://www.jboss.org/ironjacamar/schema}prefill")
        prefill.text="false"
        useStrictMin=ET.Element("{http://www.jboss.org/ironjacamar/schema}use-strict-min")
        useStrictMin.text="false"
        flushStrategy=ET.Element("{http://www.jboss.org/ironjacamar/schema}flush-strategy")
        flushStrategy.text="FailingConnectionOnly"
        pool.append(minPoolSize)
        pool.append(maxPoolSize)
        pool.append(prefill)
        pool.append(useStrictMin)
        pool.append(flushStrategy)
        datasource.append(pool)
        validation=ET.Element("{http://www.jboss.org/ironjacamar/schema}validation")
        checkValidConnectionSql.tag="{http://www.jboss.org/ironjacamar/schema}check-valid-connection-sql"
        validateOnMatch=ET.Element("{http://www.jboss.org/ironjacamar/schema}validate-on-match")
        validateOnMatch.text="false"
        backgroundValidation=ET.Element("{http://www.jboss.org/ironjacamar/schema}background-validation")
        backgroundValidation.text="false"
        useFastFail=ET.Element("{http://www.jboss.org/ironjacamar/schema}use-fast-fail")
        useFastFail.text="false"
        validation.append(checkValidConnectionSql)
        validation.append(validateOnMatch)
        validation.append(backgroundValidation)
        validation.append(useFastFail)
        datasource.append(validation)
        timeout=ET.Element("{http://www.jboss.org/ironjacamar/schema}timeout")
        datasource.append(timeout)
        statement=ET.Element("{http://www.jboss.org/ironjacamar/schema}statement")
        datasource.append(statement)
        
        newRoot.append(datasource)
        tree._setroot(newRoot)
        index=filePath.rfind("/")
        subprocess.call(["mkdir","-p",filePath[:index]+"/META-INF"])
        subprocess.call(["rm",filePath])
        tree.write(filePath[:index]+"/META-INF/"+filePath[index:],pretty_print=True,encoding='utf-8')
        return isEar
    parseXml=classmethod(parseXml)