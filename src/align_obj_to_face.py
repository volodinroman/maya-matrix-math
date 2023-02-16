import maya.cmds as cmds
import maya.api.OpenMaya as OpenMaya

# lets create a cube and locator
cube = cmds.polyCube()[0]
cmds.move(3,4,5)
cmds.rotate(45, 70,35)
locator = cmds.spaceLocator()[0]

def construct_face_matrix(obj, face_idx):
    """
    obj - object full path, eg. "|pCube1"
    face_idx - int ID of a face
    """

    # get object world matrix
    sel_list = OpenMaya.MSelectionList()
    sel_list.add(obj)
    dag_path = sel_list.getDagPath(0)
    world_matrix = dag_path.inclusiveMatrix()

    # create Faces iterator and set index "face_idx"
    face_iter = OpenMaya.MItMeshPolygon(dag_path)
    face_iter.setIndex(face_idx)

    # find face normal vector in World Space
    vec_normal = face_iter.getNormal()
    vec_normal = vec_normal * world_matrix # local to world conversion
    vec_normal.normalize() # set length to 1

    # find tangent vector in World Space
    # tangent vector is a vector between the face center and the center of the one of its edge
    # edge center = (vtx[1].position + vtx[0].position) / 2 
    face_center = face_iter.center(OpenMaya.MSpace.kWorld) # get face center coordinate as MPoint
    points = face_iter.getPoints(OpenMaya.MSpace.kWorld) # get all points of the current face
    edge_center = OpenMaya.MPoint(  (points[0].x + points[1].x)/2, 
                                    (points[0].y + points[1].y)/2, 
                                    (points[0].z + points[1].z)/2)

    vec_tangent = OpenMaya.MVector( edge_center.x - face_center.x, 
                                    edge_center.y - face_center.y, 
                                    edge_center.z - face_center.z)
    vec_tangent.normalize()

    # find up vector
    vec_up = vec_normal ^ vec_tangent
    vec_up.normalize()


    # generate an output matrix
    output_matrix = OpenMaya.MMatrix((
        (vec_tangent.x, vec_tangent.y, vec_tangent.z, 0),
        (vec_up.x, vec_up.y, vec_up.z, 0),
        (vec_normal.x, vec_normal.y, vec_normal.z, 0),
        (face_center.x, face_center.y, face_center.z, 1.0)
    ))


    output_transformation_matrix = OpenMaya.MTransformationMatrix(output_matrix)
    return output_transformation_matrix



def main():
    face_matrix = construct_face_matrix(cube, 2)

    # set this transformation matrix to Locator
    sel_list = OpenMaya.MSelectionList()
    sel_list.add(locator)
    dag_path = sel_list.getDagPath(0)
    fn_transform = OpenMaya.MFnTransform(dag_path)
    fn_transform.setTransformation(face_matrix)



main()
