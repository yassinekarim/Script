#!/opt/python3/bin/python3 
# -*-coding:utf-8 -*

def changeJndi(jndiString,scope):
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