from functools import cache, cached_property
from itertools import product

import numpy as np
import scipy

Point = tuple[int, int, int]


# @cache
# def rotation_matrices() -> np.array:
#     rot_x = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]], dtype="int32")
#     rot_y = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]], dtype="int32")
#     rot_z = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype="int32")

#     matrices = []

#     for i, j, k in product(range(4), range(4), range(4)):
#         matrices.append( np.linalg.matrix_power(rot_x, i) @ np.linalg.matrix_power(rot_y, j) @ np.linalg.matrix_power(rot_z, k))

#     return np.unique(np.array(matrices), axis=1)

@cache
def rotation_matrices() -> np.array:
    return scipy.spatial.transform.Rotation.create_group("O").as_matrix().astype("int32")

def _distance(x: tuple[int, int, int], y: tuple[int, int, int]):
    # return sum([abs(x[i] - y[i]) for i in range(3)])
    return np.linalg.norm(y - x)
     


class Scanner:
    def __init__(self, beacons: list[Point]):
        self._beacons = beacons
        self._location = None
        self._rotation = None

    @cached_property
    def number_of_beacons(self):
        return len(self._beacons)

    @cached_property
    def distances(self) -> dict[tuple[int, int], int]:
        retval = {}
        for x in range(self.number_of_beacons):
            for y in range(x + 1, self.number_of_beacons):
                retval[x, y] = _distance(self._beacons[x], self._beacons[y])

        return retval
    
    def beacons(self) -> set[Point]:
        if self.location is None or self.rotation is None:
            raise RuntimeError("Cannot provide list of beacons without knowing scanner location.")
        
        retval = set()
        for beacon in self._beacons:
            retval.add(tuple((map(int, beacon @ self.rotation + self.location))))

        return retval

    @property
    def location(self) -> Point | None:
        return self._location

    @location.setter
    def location(self, location: Point) -> None:
        self._location = location

    @property
    def rotation(self) -> np.ndarray | None:
        return self._rotation

    @rotation.setter
    def rotation(self, rotation: np.ndarray) -> None:
        self._rotation = rotation

    def overlaps(self, scanner: "Scanner") -> set[int]:
        my_distances = set(self.distances.values())
        common_distances = my_distances.intersection(set(scanner.distances.values()))
        return common_distances


class BeaconScanner:
    def __init__(self, scanners: list[Scanner]):
        self._scanners = scanners
        self._scanners[0].location = (0, 0, 0)
        self._scanners[0].rotation = np.identity(3, dtype="int32")

    def __len__(self):
        return len(self._scanners)

    def _overlapping_scanners(self) -> dict[tuple[int, int]]:
        retval = {}

        def already_done(i: int, j: int):
            return (i, j) in retval or (j, i) in retval or i == j

        for i, j in product(range(len(self)), range(len(self))):
            if already_done(i, j):
                continue
            overlaps = self._scanners[i].overlaps(self._scanners[j])
            if len(overlaps) >= 66:
                retval[i, j] = overlaps

        return retval

    @staticmethod
    def _scanner_location(
        reference_pair1: tuple[Point, Point], target_pair: tuple[Point, Point]
    ):
        """Return the location of the scanner which owns beacon_pair2 relative
        to the scanner which owns beacon_pair1

        Let A and B be beacons in reference scanner; C and D for target_scanners.
        The distance between A and B = dist between C and D, as worked
        out in overlapping_scanners(). So we know line AB is line CD.
        We just don't know which ends match and we don't know their
        orientations. This function works out whether beacon A is C or D;
        and similarly whether beacon B is D or C by comparing the differences.
        Below A = referenece_pair[1], B = reference_pair[2]
              C = target_pair[1], D = target_pair[2]

        If after comparing both ways around we find that neither arrangement
        match, then we are not viewing the beacons from the same orientation
        and we should thrown an exception.
        """

        md_ref = _distance(reference_pair1[0], reference_pair1[1]) 
        md_target = _distance(target_pair[0], target_pair[1])

        assert np.isclose(md_ref, md_target)

        loc1 = reference_pair1[0] - target_pair[0]
        loc2 = reference_pair1[1] - target_pair[1]
        if np.isclose(loc1, loc2).all():
            return loc1

        loc1 = reference_pair1[0] - target_pair[1]
        loc2 = reference_pair1[1] - target_pair[0]
        if np.isclose(loc1, loc2).all():
            return loc1

        raise ValueError("These two pairs of points are not equivalent.")

    def _process_scanner(self, reference_scanner: Scanner, target_scanner: Scanner):
        if (reference_scanner.location is None) == (
            target_scanner.location is None
        ):
            raise ValueError(
                "Exactly one of scanner0 and scanner1 should have their location set"
            )

        # we want scanner0 to be the reference scanner, so it needs to have a location
        if reference_scanner.location is None:
            target_scanner, reference_scanner = reference_scanner, target_scanner

        # grab a pair of beacons from each scanner which are the same distance apart
        overlaps = reference_scanner.overlaps(target_scanner)
        distance = next(iter(overlaps))
        reference_pair = [
            pair
            for pair, d in reference_scanner.distances.items()
            if d == distance
        ][0]
        target_pair = [
            pair
            for pair, d in target_scanner.distances.items()
            if d == distance
        ][0]

        # cycle through each possible rotation until the relative positions
        for rotation in rotation_matrices():
            try:
                location = BeaconScanner._scanner_location(
                    (
                        reference_scanner._beacons[reference_pair[0]] @ reference_scanner.rotation,
                        reference_scanner._beacons[reference_pair[1]] @ reference_scanner.rotation,
                    ),
                    (
                        target_scanner._beacons[target_pair[0]] @ rotation,
                        target_scanner._beacons[target_pair[1]] @ rotation,
                    ),
                )
            except ValueError as e:
                continue
            target_scanner.location = location + reference_scanner.location
            target_scanner.rotation = rotation
            break
        else:
            raise ValueError("Failed to find suitable rotation")

    def process_scanners(self):
        overlapping_scanners = self._overlapping_scanners()
        processed_scanners = 1
        while processed_scanners != len(self._scanners):
            for scanner0_id, scanner1_id in overlapping_scanners.keys():
                # print(f"Processing {scanner0_id} and {scanner1_id}...", end="")
                try:
                    self._process_scanner(self._scanners[scanner0_id], self._scanners[scanner1_id])
                    processed_scanners += 1
                    # print("succeeded.")
                except ValueError as v:
                    # print("failed.")
                    continue
                # print(f"Scanner {scanner0_id} location: {self._scanners[scanner0_id].location}")
                # print(f"Scanner {scanner1_id} location: {self._scanners[scanner1_id].location}")

    def beacons(self) -> set[Point]:
        self.process_scanners()
        beacons = set()
        failed = False
        for index, scanner in enumerate(self._scanners):
            beacons = beacons.union(scanner.beacons())
            if (998,-1836,-4215) in beacons and not failed:
                print(f"failure at index {index}")
                print(self._scanners[index].location)
                print(self._scanners[index].rotation)
                failed = True
        return beacons

