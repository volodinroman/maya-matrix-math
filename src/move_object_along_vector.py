import maya.api.OpenMaya as OpenMaya
import maya.cmds as cmds

# Create Cone and move/rotate it
cone, _ = cmds.polyCone()
cmds.move(3,3,3)
cmds.rotate(13,45,67)

# Create Cube 
cube, _ = cmds.polyCube()

# Add Cube and Cone to Selections list
sel_list = OpenMaya.MSelectionList()
sel_list.add(cone)
sel_list.add(cube)

# Cone data
cone_dag_path = sel_list.getDagPath(0)
cone_matrix = cone_dag_path.inclusiveMatrix() # get Cone world matrix
cone_transform_matrix = OpenMaya.MTransformationMatrix(cone_matrix) 

# Cube data
cube_dag_path = sel_list.getDagPath(1)
cube_matrix = cube_dag_path.inclusiveMatrix() # get Cube world matrix
cube_transform_fn = OpenMaya.MFnTransform(cube_dag_path)
cube_transform_matrix = OpenMaya.MTransformationMatrix(cube_matrix)
cube_pos = cube_transform_matrix.translation(OpenMaya.MSpace.kWorld)

# Distance to move along
offset_distance = 3 

# Offset vector 
cone_y_vec = OpenMaya.MVector(0,1,0) * cone_matrix
cone_y_vec.normalize()
offset = cone_y_vec * offset_distance # as MVector


def move_along_vector():
    """
    Move a cube along Cone.Y axis, starting from the original Cube position
    """
    
    position = cube_pos + offset
    cube_transform_matrix.setTranslation(position, OpenMaya.MSpace.kWorld)
    cube_transform_fn.setTransformation(cube_transform_matrix)

def move_orient_along_vector():
    """
    Move and orient a cube along Cone.Y axis, starting from the original Cube position
    """
    position = cube_pos + offset
    new_matrix = cube_matrix * cone_transform_matrix.asRotateMatrix()
    cube_transform_matrix = OpenMaya.MTransformationMatrix(new_matrix)
    cube_transform_matrix.setTranslation(position, OpenMaya.MSpace.kWorld)
    cube_transform_fn.setTransformation(cube_transform_matrix)

def move_orient_translate_along_vector():
    """
    Move and orient a cube along Cone.Y axis, starting from Cone position
    """

    # we have to invert Cone's scale matrix back to (1,1,1) as we don't want our cube
    # to inherit Cone scale values, only translation and rotation
    matrix = cone_transform_matrix.asScaleMatrix().inverse() * cone_matrix

    cube_transform_matrix = OpenMaya.MTransformationMatrix(matrix)

    position = cube_transform_matrix.translation(OpenMaya.MSpace.kWorld)
    position = position + offset
    cube_transform_matrix.setTranslation(position, OpenMaya.MSpace.kWorld)
    cube_transform_fn.setTransformation(cube_transform_matrix)


