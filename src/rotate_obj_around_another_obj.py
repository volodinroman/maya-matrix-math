"""
This script rotates a Cube around a local Y axis of a Cone
"""

import maya.cmds as cmds
import maya.api.OpenMaya as om

def main():

    # make sure you have pCone1 and pCube1 already created
    cone = "pCone1"
    cube = "pCube1"

    sl = om.MSelectionList()
    sl.add(cone)
    sl.add(cube)

    dpCone = sl.getDagPath(0)
    dpCube = sl.getDagPath(1)

    # we want to rotate this object
    mCube = dpCube.inclusiveMatrix() # get world matrix
    # around this object
    mCone = dpCone.inclusiveMatrix() # get world matrix

    # rotate by 30 degrees
    degree = 30
    angle = om.MAngle(degree, om.MAngle.kDegrees)
    rad = angle.asRadians() # convert degrees to radians
    rotation = om.MEulerRotation(0,rad,0, om.MEulerRotation.kXYZ)
    mRotation = rotation.asMatrix() # convert EulerRotation into MMatrix

    # next we place Cube into a local space of the Cone, 
    #   apply rotation matrix, and push it back to world space

    matrix =  mCube * mCone.inverse() * mRotation * mCone 

    # convert MMatrix into MTransformationMatrix
    tmCube = om.MTransformationMatrix(matrix)  

    # apply matrix to cube
    fnTrCube = om.MFnTransform(dpCube)
    fnTrCube.setTransformation(tmCube)
