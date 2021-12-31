# python 3.7
"""
    - preform PCA an 3D locations
      and use largest 2 eigenvalues and
      eigenvectors to project seismicity
      into new fault-coordinate system
    - Dimensionally is reduced by 1

"""
import numpy as np
import matplotlib.pyplot as plt

import plane_utils as utils
#====================1======================
#               parameters
#===========================================
# N and alpha used in data file name
N     = 1000
alpha = 2.4 #fault normal decay exponent
file_in = f"faultEqs_N_{N}_alpha_{alpha}.txt"
# for plotting purposes
ymin, ymax = -5, 5# fault normal distance
#====================2======================
#          load data and find PCAs
#===========================================
mXYZ = np.loadtxt( f"data/{file_in}")

#====================3======================
#     project into new coordinate system
#===========================================
mPlaneVec  = utils.fitPlane( mXYZ[:,0], mXYZ[:,1], mXYZ[:,2])
aX, aZ, aY = utils.projectPointToPlane( mXYZ[:,0], mXYZ[:,1], mXYZ[:,2],
                                        mPlaneVec)

#====================4======================
#          plots
#===========================================
fig = plt.figure( 1)
ax = plt.subplot( 311)
ax2= plt.subplot( 312)
ax3= plt.subplot( 313)
ax.plot( mXYZ[:,0], mXYZ[:,2], 'k.')
ax2.plot( aX-aX.min(), aZ-aZ.min(), 'r.')
ax3.plot( aX-aX.min(), aY-aY.mean(), 'r.')
ax.set_xlabel( 'X (km)'), ax.set_ylabel(  'Y (km)')
ax2.set_xlabel( 'Strike (km)'), ax2.set_ylabel( 'Dip (km)')
ax3.set_xlabel( 'Strike (km)'), ax2.set_ylabel( 'Normal (km)')
ax3.set_ylim( ymin, ymax)
fig.savefig( f"plots/{file_in.replace('.txt', 'proj.png')}")
plt.show()