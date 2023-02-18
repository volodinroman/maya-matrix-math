"""
Spiral Stair, that involves rotation of an object around a custom vector in space

In this example we will use a vector between 2 spheres, but we can use any other vector
Make sure you have 2 spheres in your scene - pSphere1, pSphere2
"""


import maya.cmds as cmds
import maya.api.OpenMaya as om

def do(offset_value=0.5, rotation_value=20, obj=None):

    # get Cube DagPath
    cube = obj
    sl = om.MSelectionList()
    sl.add(cube)
    dpCube = sl.getDagPath(0)

    # find a vector between two spheres
    pos1 = cmds.xform("pSphere1", ws=1, t=1, q=1)
    pos2 = cmds.xform("pSphere2", ws=1, t=1, q=1)
    vector_x = om.MVector(pos2[0]-pos1[0], pos2[1]-pos1[1], pos2[2]-pos1[2]) # Vector
    vector_x.normalize()

    # find two other vectors
    vector_z = om.MVector(0,0,1)
    vector_y = vector_z ^ vector_x
    vector_y.normalize()
    vector_z = vector_x ^ vector_y
    vector_z.normalize()

    # calculate offset (along the vector) for each stair unit
    # the offset accumulates with each iteration
    offset = offset_value
    position = om.MPoint(pos1[0], pos1[1], pos1[2])
    new_position = position + vector_x * offset

    # build a matrix that should place our object in the beginning of the vector
    origin_matrix = om.MMatrix((
        (vector_x.x, vector_x.y, vector_x.z, 0),
        (vector_y.x, vector_y.y, vector_y.z, 0),
        (vector_z.x, vector_z.y, vector_z.z, 0),
        (new_position[0], new_position[1], new_position[2], 1.0)
    ))

    # create a translation matri
    # we want to shift each unit along Z axis by 0.2
    offset_Z = om.MMatrix((
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0.2, 1.0)
    ))

    # rotation around X
    degreeX = rotation_value
    angleX = om.MAngle(degreeX, om.MAngle.kDegrees)
    radX = angleX.asRadians() # convert degrees to radians
    rotationX = om.MEulerRotation(radX,0,0, om.MEulerRotation.kXYZ) # create a rotation object
    mRotationX = rotationX.asMatrix() # convert EulerRotation into MMatrix

    # rotation around Z
    angleZ = om.MAngle(90, om.MAngle.kDegrees)
    radZ = angleZ.asRadians() # convert degrees to radians
    rotationZ = om.MEulerRotation(0,0,radZ, om.MEulerRotation.kXYZ) # create a rotation object
    mRotationZ = rotationZ.asMatrix() # convert EulerRotation into MMatrix

    # final calculation
    matrix =  origin_matrix * origin_matrix.inverse()  * offset_Z * mRotationZ * mRotationX  * origin_matrix 

    tmCube = om.MTransformationMatrix(matrix)  

    # apply matrix to cube
    fnTrCube = om.MFnTransform(dpCube)
    fnTrCube.setTransformation(tmCube)



def main():

    offset = 0.1
    for i in range(0,740,20):
        obj = cmds.duplicate("pCube1")[0]
        do(offset_value=offset, rotation_value=i, obj=obj)
        offset += 0.16

