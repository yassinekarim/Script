#!/opt/python3/bin/python3 
# -*-coding:utf-8 -*
from lxml import etree as ET

def parseXml(filePath):
    parser = ET.XMLParser(remove_blank_text=True)
    tree = ET.parse(filePath,parser)
    root = tree.getroot()
    

#     <context-param>
#       <param-name>org.richfaces.skin</param-name>
#       <param-value>blueSky</param-value>
#    </context-param>
#     <context-param>
#         <param-name>javax.faces.FACELETS_LIBRARIES</param-name>
#         <param-value>/WEB-INF/gazelle.taglib.xml</param-value>
#     </context-param>
# <!--   <context-param>

#     <param-name>org.richfaces.builtin.sort.enabled</param-name>

#     <param-value>false</param-value>

# </context-param>
#    -->
#     <!-- <context-param>  
#      <param-name>javax.faces.DISABLE_FACELET_JSF_VIEWHANDLER</param-name>  
#      <param-value>true</param-value>  
# </context-param>  -->


#   <!-- <context-param>
#        <param-name>org.ajax4jsf.VIEW_HANDLERS</param-name>
#        <param-value>javax.faces.application.ViewHandlerWrapper</param-value>
#   </context-param> -->
#    <!-- Suppress spurious stylesheets -->

#   <!--  <context-param>
#       <param-name>org.richfaces.enableControlSkinning</param-name>
#       <param-value>false</param-value>
#    </context-param>

#    <context-param>
#       <param-name>org.richfaces.enableControlSkinningClasses</param-name>
#       <param-value>false</param-value>
#    </context-param>  -->

#    <!-- Change load strategy to DEFAULT to disable sending scripts/styles as packs -->

#  <!--  <context-param>
#       <param-name>org.richfaces.resourceOptimization.enabled</param-name>
#       <param-value>true</param-value>
#    </context-param> -->

#    <!-- <context-param>
#       <param-name>org.richfaces.LoadScriptStrategy</param-name>
#       <param-value>ALL</param-value>