# opt/anaconda/envs/obspy - python 3.7
"""
    - create random 3D locations that mimic
        natural earthquake distribution along a
        single fault
    Workflow:
    - random uniform in X and Z
    - random power law in Y (direction normal to fault)
    - rotate to make things more interesting
    @author tgoebel University of Memphis
"""
import numpy as np
import matplotlib.pyplot as plt
np.random.seed( 123456)
#------------my modules------------------
from my_stats.src import plfit
from my_stats.src import random_distr
import plane_utils as utils
#====================1======================
#               parameters
#===========================================
N  = 1000
# spatial loc. limits
xmin, xmax = 1, 50#in km
zmin, zmax = 1, 10
ymin  = .1
#power law exponent
alpha = 2.4
# rotation to make things more realistic
rotAng = 25#*np.pi/180.

file_out = f"faultEQs_N_{N}_alpha_{alpha}.txt"
fig_out  = file_out.replace('txt', 'png')
#====================2======================
#          create random locations
#===========================================
# 1 #random uniform
a_X = np.random.uniform( xmin, xmax, N)
a_Z = np.random.uniform( zmin, zmax, N)
# 2 #random PL or random pareto
a_Y = random_distr.inversePowerlaw( N, alpha, ymin)
#a_Y = random_distr.inversePareto( N, alpha, ymin, ymax)
# to a random 50% sign flip
a_ID = np.random.randint(0, N-1, int(.5*N))
a_Y[a_ID] *= -1

dRes = plfit.plfit( np.array( sorted(a_Y)), xmin=ymin)
print(f"true -gamma: {alpha}, ML-fit gamma: {round(dRes['alpha'], 2)}")
# 3 #rotate by rotAng
a_Y, a_Z = utils.rotate( a_Y, a_Z, alpha)
a_X, a_Y = utils.rotate( a_X, a_Y, rotAng)
#====================3======================
#           save to file, 3D plot
#===========================================
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter( a_X, a_Y, a_Z, marker = 'o', s = 1, c = 'k')
ax.set_xlabel( 'X')
ax.set_ylabel( 'Y')
ax.set_zlabel( 'Z')
ax.set_ylim( ax.get_xlim())
ax.set_zlim( ax.get_xlim())
fig.savefig( f"plots/{fig_out}")
plt.show()

# save
np.savetxt( f"data/{file_out}", np.array([a_X, a_Y, a_Z]).T,
            header = "X   Y    Z",
            fmt    = "%8.2f%8.2f%8.2f")

