from functools import cache

import numpy as np
import scipy as sp

@cache
def rotation_matrices():
    rot_x = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
    rot_y = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
    rot_z = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])

    matrices = []

    up = np.identity(3)
    for _ in range(4):
        forward = np.identity(3)
        for __ in range(4):
            matrices.append(up @ forward)
            forward = forward @ rot_y
        forward = forward @ rot_z
        matrices.append(up @ forward)
        forward = forward @ rot_z @ rot_z
        matrices.append(up @ forward)

        up = up @ rot_x

    return np.array(matrices)


class BeaconScanner:

    def find_common_beacons(self, readings0, readings1):
        # get the distance vectors between all readings in a nice matrix for scanner0
        scanner0 = readings0[:, None] - readings0[0][None, :]

        # get the distance vectors between all readings for scanner1 and rotate them in every possible way
        scanner1 = (readings1[1][:, None] - readings1[1][None, :]) @ rotation_matrices()[:, None, :, :]

        # compare all the distance vectors, and highlight where all 3 dimensions are zero
        thing = np.argwhere(
            np.count_nonzero(
                (scanner0[:, :, None, None, None, :] - scanner1[None, None, :, :, :, :])
                == 0,
                axis=-1,
            )
            == 3,
        )

        # remove all the elements where we're comparing readings with themselves
        mask = np.logical_and(thing[:, 0] != thing[:, 1], thing[:, 3] != thing[:, 4])
        otherthing = thing[mask, :]

        # get the rotation which appears the most
        rotation = sp.stats.mode(otherthing[:, 2])

        print(f"Shape: {otherthing.shape}")


    def count_beacons(self, inputs):

        assert False
