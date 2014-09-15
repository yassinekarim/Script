"""-ds.xml parser"""
#!/usr/bin/python3
# -*-coding:utf-8 -*
from lxml import etree as ET
from migration.utils.jndiMigration import JndiMigration
import subprocess
class DataSourceMigration:
    """ data source file """
    def parse_xml(cls, file_path):
        """parse *-ds.xml to change for the new version"""
        parser = ET.XMLParser(remove_blank_text=True)
        tree = ET.parse(file_path, parser)
        root = tree.getroot()
        iterator = root.findall("local-tx-datasource")
        nsmap_ = {None : "http://www.jboss.org/ironjacamar/schema"}
        new_root = ET.Element("datasources", nsmap=nsmap_)
        for localtxdatasource in iterator:
            datasource = cls.parse_datasource(localtxdatasource)
            new_root.append(datasource)
        if iterator:
            tree._setroot(new_root)
            index = file_path.rfind("/")
            subprocess.call(["mkdir", "-p", file_path[:index]+"/META-INF"])
            subprocess.call(["rm", file_path])
            tree.write(file_path[:index]+"/META-INF/"+file_path[index:], pretty_print=True, encoding='utf-8', xml_declaration=True)
    parse_xml = classmethod(parse_xml)
    def parse_datasource(cls, localtxdatasource):
        """parse the info in a local-tx-datasource and construct a new ode with the corect architecture"""
        jndi_name = localtxdatasource.find("jndi-name")
        connection_url = localtxdatasource.find("connection-url")
        user_name = localtxdatasource.find("user-name")
        password = localtxdatasource.find("password")
        min_pool_size = localtxdatasource.find("min-pool-size")
        max_pool_size = localtxdatasource.find("max-pool-size")
        idle_timeoutminutes = localtxdatasource.find("idle-timeout-minutes")
        preparedstatementcachesize = localtxdatasource.find("prepared-statement-cache-size")
        blockingtimeoutmillis = localtxdatasource.find("blocking-timeout-millis")
        checkvalidconnectionsql = localtxdatasource.find("check-valid-connection-sql")
        datasource = ET.Element("{http://www.jboss.org/ironjacamar/schema}datasource")
        datasource.set("jta", "true")
        datasource.set("enabled", "true")
        datasource.set("use-java-context", "true")
        datasource.set("pool-name", jndi_name.text)
        datasource.set("jndi-name", JndiMigration.change_jndi_ds(jndi_name.text, "jboss"))
        driver = ET.Element("{http://www.jboss.org/ironjacamar/schema}driver")
        driver.text = "postgresql"
        connection_url.tag = "{http://www.jboss.org/ironjacamar/schema}connection-url"
        datasource.append(connection_url)
        datasource.append(driver)
        security = ET.Element("{http://www.jboss.org/ironjacamar/schema}security")
        user_name.tag = "{http://www.jboss.org/ironjacamar/schema}user-name"
        password.tag = "{http://www.jboss.org/ironjacamar/schema}password"
        security.append(user_name)
        security.append(password)
        datasource.append(security)
        pool = ET.Element("{http://www.jboss.org/ironjacamar/schema}pool")
        if min_pool_size is not None:
            min_pool_size.tag = "{http://www.jboss.org/ironjacamar/schema}min-pool-size"
            pool.append(min_pool_size)
        if min_pool_size is not None:
            max_pool_size.tag = "{http://www.jboss.org/ironjacamar/schema}max-pool-size"
            pool.append(max_pool_size)
        prefill = ET.Element("{http://www.jboss.org/ironjacamar/schema}prefill")
        prefill.text = "false"
        use_strict_min = ET.Element("{http://www.jboss.org/ironjacamar/schema}use-strict-min")
        use_strict_min.text = "false"
        flush_strategy = ET.Element("{http://www.jboss.org/ironjacamar/schema}flush-strategy")
        flush_strategy.text = "FailingConnectionOnly"
        pool.append(prefill)
        pool.append(use_strict_min)
        pool.append(flush_strategy)
        datasource.append(pool)
        if checkvalidconnectionsql is not None:
            validation = ET.Element("{http://www.jboss.org/ironjacamar/schema}validation")
            checkvalidconnectionsql.tag = "{http://www.jboss.org/ironjacamar/schema}check-valid-connection-sql"
            validate_on_match = ET.Element("{http://www.jboss.org/ironjacamar/schema}validate-on-match")
            validate_on_match.text = "false"
            background_validation = ET.Element("{http://www.jboss.org/ironjacamar/schema}background-validation")
            background_validation.text = "false"
            use_fast_fail = ET.Element("{http://www.jboss.org/ironjacamar/schema}use-fast-fail")
            use_fast_fail.text = "false"
            validation.append(checkvalidconnectionsql)
            validation.append(validate_on_match)
            validation.append(background_validation)
            validation.append(use_fast_fail)
            datasource.append(validation)
        timeout = ET.Element("{http://www.jboss.org/ironjacamar/schema}timeout")
        if idle_timeoutminutes is not None:
            idle_timeoutminutes.tag = "{http://www.jboss.org/ironjacamar/schema}idle-timeout-minutes"
            timeout.append(idle_timeoutminutes)
        if blockingtimeoutmillis is not None:
            blockingtimeoutmillis.tag = "{http://www.jboss.org/ironjacamar/schema}blocking-timeout-millis"
            timeout.append(blockingtimeoutmillis)
        datasource.append(timeout)
        statement = ET.Element("{http://www.jboss.org/ironjacamar/schema}statement")
        track_statements = ET.Element("{http://www.jboss.org/ironjacamar/schema}track-statements")
        track_statements.text = "false"
        if checkvalidconnectionsql is not None:
            preparedstatementcachesize.tag = "{http://www.jboss.org/ironjacamar/schema}prepared-statement-cache-size"
            statement.append(preparedstatementcachesize)
        statement.append(track_statements)
        datasource.append(statement)
        return datasource
    parse_datasource = classmethod(parse_datasource)
