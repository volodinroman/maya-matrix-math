import maya.api.OpenMaya as OpenMaya

# create a cube
cube = cmds.polyCube()[0]
cmds.xform(cube, t=[1,2,3], ro=[10,15,32], ws=1)

# get a dag path of the cube
selection_list = om.MSelectionList()
selection_list.add(cube)
dag_path = selection_list.getDagPath(0)

# get world matrix
world_matrix = dag_path.inclusiveMatrix() # gives us pCube1 world matrix

print(world_matrix)
