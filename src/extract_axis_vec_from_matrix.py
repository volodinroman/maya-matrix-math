import maya.api.OpenMaya as OpenMaya
import maya.cmds as cmds

# create a cube and move/rotate it
cube = cmds.polyCube()[0]
cmds.move(2,2,3)
cmds.rotate(13,28,44)


# define axis vectors
axis_x = OpenMaya.MVector(1,0,0)
axis_y = OpenMaya.MVector(0,1,0)
axis_z = OpenMaya.MVector(0,0,1)

def axis_vector(geo, vector):
    
    sel_list = OpenMaya.MSelectionList()
    sel_list.add(geo)
    dag_path = sel_list.getDagPath(0)
    world_matrix = dag_path.inclusiveMatrix() # get world matrix
    
    vec = vector * world_matrix # get a world direction of the axis
    vec.normalize() # normalize to set vector length to 1
        
    return vec
    
vec_z = axis_vector(cube, axis_z)
