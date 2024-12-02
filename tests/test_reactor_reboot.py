import pytest

from reactor_reboot import parse_step, Step, Cuboid, Grid


parse_step_data = [
    ("on x=11..13,y=11..13,z=11..13", Step(True, Cuboid((11, 13), (11, 13), (11, 13)))),
    ("on x=10..12,y=10..12,z=10..12", Step(True, Cuboid((10, 12), (10, 12), (10, 12)))),
    ("on x=-54112..-39298,y=-85059..-49293,z=-27449..7877", None),
]


@pytest.mark.parametrize("text,expected", parse_step_data)
def test_parse_step(text, expected):
    step = parse_step(text)

    assert step == expected


def test_overlap():
    c1 = Cuboid((11, 13), (11, 13), (11, 13))
    c2 = Cuboid((10, 12), (10, 12), (10, 12))

    assert c1.overlap(c2) == Cuboid((11, 12), (11, 12), (11, 12))


volume_data = (
    (Cuboid((11, 13), (11, 13), (11, 13)), 27),
    (Cuboid((10, 12), (10, 12), (10, 12)), 27),
)


@pytest.mark.parametrize("cuboid,volume", volume_data)
def test_volume(cuboid, volume):
    assert cuboid.volume() == volume


class TestGrid:
    def test_add_cuboid(self):
        c1 = Cuboid((11, 13), (11, 13), (11, 13))
        c2 = Cuboid((10, 12), (10, 12), (10, 12))
        c3 = Cuboid((9, 11), (9, 11), (9, 11))
        c4 = Cuboid((10, 10), (10, 10), (10, 10))
        under_test = Grid()
        under_test.add_cuboid(c1)
        under_test.add_cuboid(c2)
        under_test.subtract_cuboid(c3)
        under_test.add_cuboid(c4)
        assert under_test.on_cubes() == 39
