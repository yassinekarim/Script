#!/usr/bin/python3
# -*-coding:utf-8 -*
from lxml import etree as ET
from migration.utils.jndiMigration import JndiMigration
import subprocess
basestring = (str,bytes)

class DataSourceMigration:
    
    def parseXml(cls,filePath):
        """parse *-ds.xml to change for the new version"""
        parser = ET.XMLParser(remove_blank_text=True)
        tree = ET.parse(filePath,parser)
        root = tree.getroot()
        localTxDatasource=root.find("local-tx-datasource")
        if(localTxDatasource is not None):      
            jndiName=localTxDatasource.find("jndi-name")
            connectionUrl=localTxDatasource.find("connection-url")
            userName=localTxDatasource.find("user-name")
            password=localTxDatasource.find("password")
            minPoolSize=localTxDatasource.find("min-pool-size")
            maxPoolSize=localTxDatasource.find("max-pool-size")
            idleTimeoutMinutes=localTxDatasource.find("idle-timeout-minutes")
            preparedStatementCacheSize=localTxDatasource.find("prepared-statement-cache-size")
            blockingTimeoutMillis=localTxDatasource.find("blocking-timeout-millis")
            checkValidConnectionSql=localTxDatasource.find("check-valid-connection-sql")
            NSMAP={None : "http://www.jboss.org/ironjacamar/schema"} 
            newRoot = ET.Element("datasources",nsmap=NSMAP)
            datasource=ET.Element("{http://www.jboss.org/ironjacamar/schema}datasource")
            datasource.set("jta","true")
            datasource.set("enabled","true")
            datasource.set("use-java-context","true")
            datasource.set("pool-name",jndiName.text)
            datasource.set("jndi-name",JndiMigration.changeJndiDS(jndiName.text,"jboss"))
            driver=ET.Element("{http://www.jboss.org/ironjacamar/schema}driver")
            driver.text="postgresql"
            connectionUrl.tag="{http://www.jboss.org/ironjacamar/schema}connection-url"
            datasource.append(connectionUrl)
            datasource.append(driver)
            security=ET.Element("{http://www.jboss.org/ironjacamar/schema}security")
            userName.tag="{http://www.jboss.org/ironjacamar/schema}user-name"
            password.tag="{http://www.jboss.org/ironjacamar/schema}password"
            security.append(userName)
            security.append(password)
            datasource.append(security)
            pool=ET.Element("{http://www.jboss.org/ironjacamar/schema}pool")
            if(minPoolSize is not None):
                minPoolSize.tag="{http://www.jboss.org/ironjacamar/schema}min-pool-size"
                pool.append(minPoolSize)
            if(minPoolSize is not None):   
                maxPoolSize.tag="{http://www.jboss.org/ironjacamar/schema}max-pool-size"
                pool.append(maxPoolSize)
            prefill=ET.Element("{http://www.jboss.org/ironjacamar/schema}prefill")
            prefill.text="false"
            useStrictMin=ET.Element("{http://www.jboss.org/ironjacamar/schema}use-strict-min")
            useStrictMin.text="false"
            flushStrategy=ET.Element("{http://www.jboss.org/ironjacamar/schema}flush-strategy")
            flushStrategy.text="FailingConnectionOnly"
            pool.append(prefill)
            pool.append(useStrictMin)
            pool.append(flushStrategy)
            datasource.append(pool)
            if(checkValidConnectionSql is not None):
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
            if(idleTimeoutMinutes is not None):
                idleTimeoutMinutes.tag="{http://www.jboss.org/ironjacamar/schema}idle-timeout-minutes"
                timeout.append(idleTimeoutMinutes)
            if(blockingTimeoutMillis is not None):
                blockingTimeoutMillis.tag="{http://www.jboss.org/ironjacamar/schema}blocking-timeout-millis"
                timeout.append(blockingTimeoutMillis)
            datasource.append(timeout)
            statement=ET.Element("{http://www.jboss.org/ironjacamar/schema}statement")
            trackStatements=ET.Element("{http://www.jboss.org/ironjacamar/schema}track-statements")
            trackStatements.text="false"
            if(checkValidConnectionSql is not None):
                preparedStatementCacheSize.tag="{http://www.jboss.org/ironjacamar/schema}prepared-statement-cache-size"
                statement.append(preparedStatementCacheSize)
            statement.append(trackStatements)
            datasource.append(statement)
            newRoot.append(datasource)
            tree._setroot(newRoot)
            index=filePath.rfind("/")
            subprocess.call(["mkdir","-p",filePath[:index]+"/META-INF"])
            subprocess.call(["rm",filePath])
            tree.write(filePath[:index]+"/META-INF/"+filePath[index:],pretty_print=True,encoding='utf-8',xml_declaration=True)
    parseXml=classmethod(parseXml)