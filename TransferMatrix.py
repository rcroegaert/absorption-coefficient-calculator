import numpy as np

class LayerProperties:
    def __init__(self, thickness, flow_res, smth_else):
        self.thickness = thickness
        self.flow_res = flow_res
        self.smth_else = smth_else

class TransferMatrix:
    # which data type does numpy take to calculate with matrices?

    @property
    def TransferMatrix(self, layer_properties, **args):
        # ndmin = 2, Transfer Matrices should always be 2x2 Matrices
        tm = np.mat(np.array([[0.+0.j,0.+0.j],[0.+0.j,0.+0.j]]), dtype=complex, ndmin=2)
        if ((not layer_properties) or (not args)):
            # if no arguments are given, create an empty mat in the right shape
            return tm
        else:
            # get Impedance 
            return # check values and apply them
        
    @property
    def Impedance(self):
        # get Acoustic Impedance
        # 4.16

        # here for rigidly backed system
        # with sonic speed c, porousity epsilon, density roh
        # z = roh * c/(1 - epsilon) 
        
        return NotImplementedError

    def multiply_transfer_matrices(tm1, tm2):
        # make > 2 input matrices available
        # check that all these are transfer matrices
        return np.matmul(tm1, tm2)