import maya.cmds as cmds
import maya.api.OpenMaya as om

def create_and_transform_cube():
    """Create a cube and apply transformations."""
    cube = cmds.polyCube()[0]
    cmds.move(2, 3, 4, cube)
    cmds.rotate(13, 16, 20, cube)
    return cube

def get_world_matrix(object_name):
    """Get the world matrix of the specified object."""
    sel_list = om.MSelectionList()
    sel_list.add(object_name)
    dag_path = sel_list.getDagPath(0)
    return dag_path.inclusiveMatrix()

def print_vertex_positions(object_name):
    """Print object space and world space positions of object vertices."""
    world_matrix = get_world_matrix(object_name)
    vertex_iter = om.MItMeshVertex(object_name)

    while not vertex_iter.isDone():
        pos = vertex_iter.position(om.MSpace.kObject)  # Object Space position
        world_pos = pos * world_matrix  # Convert to World Space position
        print(f"Object space: {pos}, World space: {world_pos}")
        vertex_iter.next()

# Main execution
cube = create_and_transform_cube()
print_vertex_positions(cube)

"""
Result:
(-0.5, -0.5, 0.5, 1) (1.85051, 2.30744, 4.49801, 1)
(0.5, -0.5, 0.5, 1) (2.7538, 2.63621, 4.22238, 1)
(-0.5, 0.5, 0.5, 1) (1.57552, 3.24426, 4.71425, 1)
(0.5, 0.5, 0.5, 1) (2.47881, 3.57303, 4.43861, 1)
(-0.5, 0.5, -0.5, 1) (1.2462, 3.36379, 3.77762, 1)
(0.5, 0.5, -0.5, 1) (2.14949, 3.69256, 3.50199, 1)
(-0.5, -0.5, -0.5, 1) (1.52119, 2.42697, 3.56139, 1)
(0.5, -0.5, -0.5, 1) (2.42448, 2.75574, 3.28575, 1)
"""
