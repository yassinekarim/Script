"""script to migrate JNDI"""
#!/usr/bin/python3
# -*-coding:utf-8 -*
class JndiMigration:
    """provides two methods to migrate JNDI"""
    def change_jndi(cls, jndi_string, scope):
        """update Jndi to match ejb3.1 jndi rules"""
        if ":" in jndi_string:
            index = jndi_string.rfind(':')
            if jndi_string[:index] == "java":
                if jndi_string[index+1] == "/":
                    return jndi_string[:index+1]+scope+"/root"+jndi_string[index+1:]
                else:
                    return jndi_string[:index+1]+scope+jndi_string[index+1:]
            else:
                print("erreur")
        elif jndi_string[0] == "/":
            return "java:"+scope+"/root"+jndi_string
        else:
            return "java:"+scope+"/"+jndi_string
    change_jndi = classmethod(change_jndi)
    def change_jndi_ds(cls, jndi_string, scope):
        """provide correct JNDI Datasource"""
        if ":" in jndi_string:
            index = jndi_string.rfind(':')
            if jndi_string[:index] == "java":
                if jndi_string[index+1] == "/":
                    return jndi_string[:index+1]+scope+"/datasources"+jndi_string[index+1:]
                else:
                    return jndi_string[:index+1]+scope+jndi_string[index+1:]
            else:
                print("erreur")
        elif jndi_string[0] == "/":
            return "java:"+scope+"/datasources"+jndi_string
        else:
            return "java:"+scope+"/datasources/"+jndi_string
    change_jndi_ds = classmethod(change_jndi_ds)
