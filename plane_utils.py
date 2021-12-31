# python3.7
"""
    - utility functions to generate random 3D earthquake
        locations, rotations and fault plane fitting

"""
import numpy as np

def rotate( X, Y, angle):
    """
    rotate two vectors (X and Y) about angle and
    return rotated coordinates
    """
    meanX, meanY = X.mean(), Y.mean()
    rotXY = np.dot(np.array([X-meanX, Y-meanY]).T,
                   createRotationMatrix(angle))
    return rotXY[:,0], rotXY[:,1]

def createRotationMatrix( alpha):
    """
        2D rotation matrix
    """
    if alpha > (2*np.pi):
        print( 'change to radians')
        alpha = alpha*np.pi/180
    else:
        pass
    rotationMatrix = np.array( [[np.cos(alpha), -np.sin(alpha)],
                                [np.sin(alpha), np.cos(alpha)]])
    return rotationMatrix

#=============================================
#
#=============================================
def fitPlane( x, y, z):
    """
    singular value decomposition to get 3 largest PCAs
    input: points - vectors[x,y,z]
    output: mPlaneVec (plane determined by three vectors:
            mPlaneVec[0] = strike
            mPlaneVec[1] = dip
            mPlaneVec[2] = norm
            eigenVal
    """
    #stack vector in matrix
    mPoints = np.array([x,y,z])
    mPoints = deMeanCoordinates(mPoints)
    #singular value decompostion, with diagS - daigonal entries of autocorrelation matrix, eigenVec - eigenvectors
    eigenVec, eigenVal, u = np.linalg.linalg.svd( mPoints, full_matrices=True, compute_uv = True)
    return sortEigenVectors(eigenVec, eigenVal)

def sortEigenVectors( eigenVec, eigenVal):
    """
    sort eigenVec so largest eigenVal is first, then intermediate and so on
    outout: mPlaneVec
    """
    return eigenVec.T[np.argsort( eigenVal)[::-1]].T


def deMeanCoordinates( matrix):
    #loop over rows: (x,y,z)
    for j in range(matrix.shape[0]):
         matrix[j] -= matrix[j].mean()
    return matrix

def projectPointToPlane( x, y, z, mPlaneVec):
    """
    takes dot product of points(x,y,z) with fault plane vectors ( )
    input: x,y,z,  - point coordinates
           mVecPlane - plane vectors mVecPlane[:,0] - strike, mVecPlane[:,1] - norm, mVecPlane[:,2] - dip
                     = [strike, norm, dip]
    output: projOnStrike, projOnNorm,projOnDip   - x,y,z components of projected points
    """
    mPoints = np.array([x,y,z])
    #normalize plane defining vectors
    # mVecPlane[:,0] = normalizeVector(mVecPlane[:,0] )
    # mVecPlane[:,1] = normalizeVector(mVecPlane[:,1] )
    # mVecPlane[:,2] = normalizeVector(mVecPlane[:,2] )
    projOnStrike = []
    projOnDip = []
    projOnNorm = []
    #loop over all point coordinates
    for i in range( x.shape[0] ):
        #project points into strike - dip plane, or strike - norm plane
        projOnStrike.append(   np.dot(mPoints[:,i], mPlaneVec[:,0]) )
        #take x,y,z of points and x,y,z of plane vectors, take dot product of it
        projOnDip.append(     np.dot(mPoints[:,i], mPlaneVec[:,1]) )
        projOnNorm.append(      np.dot(mPoints[:,i], mPlaneVec[:,2]) )
    projOnStrike = np.array( projOnStrike)
    projOnNorm   = np.array( projOnNorm )
    projOnDip    = np.array( projOnDip)
    return projOnStrike, projOnDip, projOnNorm