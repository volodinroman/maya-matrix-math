import maya.cmds as cmds
import maya.api.OpenMaya as om

cube = cmds.polyCube()[0]
cmds.move(2,3,4)
cmds.rotate(13,16,20)

sel_list = om.MSelectionList()
sel_list.add(cube)
dag_path = sel_list.getDagPath(0)
world_matrix = dag_path.inclusiveMatrix() # world matrix
iter = om.MItMeshVertex(dag_path) # iterates over the object's vertices

while not iter.isDone():
    
    pos = iter.position() # position in Object Space
    world_pos = pos * world_matrix # world position
    print(pos, world_pos)
    
    iter.next()
