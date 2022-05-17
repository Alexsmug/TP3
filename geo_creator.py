# Fait par Alex

from multiprocessing.sharedctypes import Value
from turtle import position
import hou



def init(par):
    parent:hou.Node = par
    g:hou.ParmTemplateGroup =  parent.parmTemplateGroup()
    if g.find("create") == None:
        p:hou.ButtonParmTemplate = hou.ButtonParmTemplate("create","Create_points")
        p.setScriptCallback("hou.pwd().hm().update()")
        p.setScriptCallbackLanguage(hou.scriptLanguage.Python)
        g.append(p)
    
    if g.find("multi") == None:
        folder:hou.FolderParmTemplate = hou.FolderParmTemplate("multi","Positions",folder_type=hou.folderType.MultiparmBlock)
        vec3:hou.FloatParmTemplate = hou.FloatParmTemplate("posf","position",3,naming_scheme=hou.parmNamingScheme.XYZW)
        folder.addParmTemplate(vec3)
        g.append(folder)
    
    
    



        parent.setParmTemplateGroup(g)




































def deinit(par):
    parent:hou.Node = par
    g:hou.ParmTemplateGroup =  parent.parmTemplateGroup()
    test:hou.ParmTemplate = g.find("create")
    multi:hou.ParmTemplate = g.find("multi")
    
    if  test != None:
        g.remove(test)
    if multi != None:
        g.remove(multi)
    parent.setParmTemplateGroup(g)


def update():
    print("Update was called, do stuff here.")
    # Un print pour vérifier si tout fonctionne
    
    obj:hou.Node = hou.node("/obj/team_python_v2")
    multi:hou.Parm = obj.parm("multi") 
    
    PointGenerateSop:hou.Node = obj.createNode("pointgenerate","points")
    # Nous tentons de créer une node qui va générer nos points
    # le 'pointgenerate'est utiliser pour créer le nombre de point que l'utilisateur demande
    npts = PointGenerateSop.parm("npts")
    npts.set(multi.multiParmInstancesCount())
    # La node point generate est créer et recois le nombre de point que l'usager désire

    AttributeExpressionSop:hou.Node = obj.createNode("attribexpression","position")
    AttributeExpressionSop.setInput(0,PointGenerateSop)
    # Nous connectons le générateur de point avec la 'node' qui va servir a leur donner une position en XYZ

 

    expression:hou.Parm = obj.parm("expressions")
    expression = AttributeExpressionSop.parm("expressions")
    # Création du point node pour changer la position des points    
    expression.setExpression('ch("../points/npts")')
    # Nous rajoutons une 'relative reference' entre les deux nodes, pour que les 2 nodes est le même nombre de points

    # Nous devons par la suite changer la value du parm "snippet" pour le mettre a value, pour avoir les données de vector xyz




# points:hou.Node = parent.node("position")
    
    
    for i in range(1,multi.multiParmInstancesCount()+1):
        a = AttributeExpressionSop.parm("snippet" + str(i))
        a.set("value")
# Nous changons la valeur du 'parm''snippet' pour le mettre a 'value' pour avoir un 'vector3' de XYZ

    
    num = 1

    for parm in multi.multiParmInstances():
        value = parm.eval()
       
        

        if parm.name().find("x") > -1:
            xp = AttributeExpressionSop.parm("valv3_"+str(num)+"x")
            xp.set(value)

        if parm.name().find("y") > -1:
            yp = AttributeExpressionSop.parm("valv3_"+str(num)+"y")
            yp.set(value)

        if parm.name().find("z") > -1:
            zp = AttributeExpressionSop.parm("valv3_"+str(num)+"z")
            zp.set(value)
            num+=1

        
# la section plus haut est utilisé pour fixer la position des points selon les valeurs de position donner par l'utilisateur
