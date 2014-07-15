#!/opt/python3/bin/python3 
# -*-coding:utf-8 -*
class JndiMigration:

    def changeJndi(cls,jndiString,scope):
        """update Jndi to match ejb3.1 jndi rules"""
        if (":" in jndiString):
            index=jndiString.rfind(':')
            if (jndiString[:index]=="java"):
                if (jndiString[index+1]=="/"):
                    return jndiString[:index+1]+scope+"/root"+jndiString[index+1:]
                else:
                    return jndiString[:index+1]+scope+jndiString[index+1:]
            else:
                print ("erreur")
        elif (jndiString[0]=="/"):
            return "java:"+scope+"/root"+jndiString
        else:
            return "java:"+scope+"/"+jndiString
    changeJndi = classmethod(changeJndi)

    def changeJndiDS(cls,jndiString,scope):
        """update Jndi to match ejb3.1 jndi rules"""
        if (":" in jndiString):
            index=jndiString.rfind(':')
            if (jndiString[:index]=="java"):
                if (jndiString[index+1]=="/"):
                    return jndiString[:index+1]+scope+"/datasources"+jndiString[index+1:]
                else:
                    return jndiString[:index+1]+scope+jndiString[index+1:]
            else:
                print ("erreur")
        elif (jndiString[0]=="/"):
            return "java:"+scope+"/datasources"+jndiString
        else:
            return "java:"+scope+"/datasources/"+jndiString
    changeJndi = classmethod(changeJndi)