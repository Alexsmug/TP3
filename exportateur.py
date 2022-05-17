
from multiprocessing.sharedctypes import Value
from random import Random, random
import hou
import json


def init(par):
    parent:hou.Node = par
    g:hou.ParmTemplateGroup =  parent.parmTemplateGroup()
    if g.find("Export") == None:
        p:hou.ButtonParmTemplate = hou.ButtonParmTemplate("Export","Export values")
        p.setScriptCallback("hou.pwd().hm().update()")
        p.setScriptCallbackLanguage(hou.scriptLanguage.Python)
        g.append (p)
        # implémentation du boutton d'exportation et du paramêtre de position
    
    if g.find("multi") == None:
        folder:hou.StringParmTemplate = hou.StringParmTemplate("multi","path",1)
        g.append(folder)
    parent.setParmTemplateGroup(g)

    


def update():
    parent:hou.Node = hou.node('/obj/team_python_v2')
    points:hou.Node = parent.node('position')
    multi:hou.Parm = points.parm('expressions')
    # référence pour aller chercher l'information requise de la node qui créer les points dans le code geo_creator
    
    
    filename = parent.parm("multi").eval()
    # création d'un fichier .json pour y exporter les valeurs des point y compris l'emplacement de celui-ci
    
    data = {
            
    }
    
    for i in range(1,multi.eval()+1):
        data[i] = {}
        valv3_1x:hou.Parm = points.parm("valv3_"+str(i)+"x")
        if isinstance(valv3_1x, hou.Parm):
            data[i]["valv3_1x"] = valv3_1x.eval()
        valv3_1y:hou.Parm = points.parm("valv3_"+str(i)+"y")
        if isinstance(valv3_1y, hou.Parm):
            data[i]["valv3_1y"] = valv3_1y.eval()    
        valv3_1z:hou.Parm = points.parm("valv3_"+str(i)+"z")
        if isinstance(valv3_1z, hou.Parm):
            data[i]["valv3_1z"] = valv3_1y.eval()   
    #   Pour aller chercher la valeur positionelle de chaque point 
    


    
    
    
   
    
    
    
    file = open(filename,"w")
    json.dump(data,file,indent=4) 
    # indentation des paramêtres dans le fichier .json
    

    
    

def deinit(par):
    parent:hou.Node = par
    g:hou.ParmTemplateGroup =  parent.parmTemplateGroup()
    test:hou.ParmTemplate = g.find("Export")
    multi:hou.ParmTemplate = g.find("multi")
    if  test != None:
        g.remove(test)
    if multi != None:
        g.remove(multi)
    parent.setParmTemplateGroup(g)