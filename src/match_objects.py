"""
We have 2 objects in Maya scene. We will take a world matrix of the 1st object and apply it to the 2nd object. If we have 2 identical cubes, at the end they will overlap.
"""

import maya.api.OpenMaya as OpenMaya
import maya.cmds as cmds

# create 2 objects and move/rotate one of them
cube = cmds.polyCube()[0]
cone = cmds.polyCone()[0]
cmds.xform(cube, t=[3,5,6], ro=[13,30,50], ws=1)

# get worldMatrix of the 1st object
selection_list = OpenMaya.MSelectionList()
selection_list.add(cube)
dag_path = selection_list.getDagPath(0) # get object DagPath
world_matrix = dag_path.inclusiveMatrix() # inclusive matrix includes object transformations including his parents

# convert world_matrx (MMatrix) into transformation matrix (MTransformationMatrix)
transform_matrix = OpenMaya.MTransformationMatrix(world_matrix)

# wrap the 2nd object with MFnTransform class
selection_list.add(cone)
dag_path_2 = selection_list.getDagPath(1)
fn_transform = OpenMaya.MFnTransform(dag_path_2)

# MFnTransform class allows us to apply transformation matrix to an object
fn_transform.setTransformation(transform_matrix)

# at this point two objects should match and overlap in space
