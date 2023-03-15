import maya.api.OpenMaya as OpenMaya

def apply_transformation(dag: OpenMaya.MDagPath, matrix: OpenMaya.MMatrix) -> None:
    transform = OpenMaya.MFnTransform(dag)
    transform_matrix = OpenMaya.MTransformationMatrix(matrix)
    transform.setTransformation(transform_matrix)


sel_list = OpenMaya.MSelectionList() 
sel_list.add("pCube1")
dagPath_Cube = sel_list.getDagPath(0) 
cube_world_matrix = dagPath_Cube.inclusiveMatrix() # get pCube1 world matrix

# let's move the cube 3 units up
offset_matrix = OpenMaya.MMatrix() # creates an empty (Identity) matrix

"""
The MMatrix is a mathematical object that requires conversion 
into an MTransformationMatrix to be utilized as a transformation matrix.
"""

offset_matrix_transform = OpenMaya.MTransformationMatrix(offset_matrix) # Transformation matrix

# set translation values
offset = OpenMaya.MVector(0, 3.0, 0)

# kWorld means we apply transformation in world space
offset_matrix_transform.setTranslation(offset, OpenMaya.MSpace.kWorld) 

# now let's apply the offset matrix to our object matrix
# we need to get back to mathematical entity (MMatrix) to perform multiplication
offset_matrix = offset_matrix_transform.asMatrix() # get MMatrix

final_matrix = cube_world_matrix * offset_matrix

# let's get pCube1 transform node object, 
# convert final matrix into transformation matrix and apply it to the transform node
apply_transformation(dagPath_Cube, final_matrix)

# let's undo this action
offset_matrix_inverse = offset_matrix.inverse()
final_matrix_undo = final_matrix * offset_matrix_inverse

apply_transformation(dagPath_Cube, final_matrix_undo)
