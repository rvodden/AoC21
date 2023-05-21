import pytest

from hydrothermal_vent.hydrothermal_vent import (
    Line,
    Point,
    get_number_of_points_which_have_two_or_more_lines_traversing_them,
    smallest_power_of_two_minus_one_greater_than,
    highest_power_of_two_less_than,
    get_sub_regions,
    get_bounds,
    both_endpoints_in_region,
    get_line_segment_in_region,
    get_line_segments_in_region,
    line_intersects_region,
    select_horizontal_and_vertical_lines,
)


@pytest.fixture
def hydrothermal_vents() -> list[Line]:
    return [
        Line.from_coords(0, 9, 5, 9),
        Line.from_coords(8, 0, 0, 8),
        Line.from_coords(9, 4, 3, 4),
        Line.from_coords(2, 2, 2, 1),
        Line.from_coords(7, 0, 7, 4),
        Line.from_coords(6, 4, 2, 0),
        Line.from_coords(0, 9, 2, 9),
        Line.from_coords(3, 4, 1, 4),
        Line.from_coords(0, 0, 8, 8),
        Line.from_coords(5, 5, 8, 2),
    ]


def test_get_number_of_points_which_have_two_or_more_lines_traversing_them(
    hydrothermal_vents,
):
    assert (
        get_number_of_points_which_have_two_or_more_lines_traversing_them(
            select_horizontal_and_vertical_lines(hydrothermal_vents)
        )
        == 5
    )


def test_get_number_of_points_which_have_two_or_more_lines_traversing_them_part_2(
    hydrothermal_vents,
):
    assert (
        get_number_of_points_which_have_two_or_more_lines_traversing_them(
            hydrothermal_vents
        )
        == 12
    )


def test_get_bounds(hydrothermal_vents: list[Line]):
    assert get_bounds(hydrothermal_vents) == (Point(0, 0), Point(15, 15))


@pytest.mark.parametrize("value,expected", [(3, 3), (2, 3), (4, 7), (17, 31)])
def test_smallest_power_of_two_minus_one_greater_than(value, expected) -> None:
    assert smallest_power_of_two_minus_one_greater_than(value) == expected


def test_highest_power_of_two_less_than() -> None:
    assert highest_power_of_two_less_than(4) == 4
    assert highest_power_of_two_less_than(3) == 2


def test_get_sub_regions():
    assert get_sub_regions((Point(0, 0), Point(7, 7))) == [
        (Point(0, 0), Point(3, 3)),
        (Point(0, 4), Point(3, 7)),
        (Point(4, 0), Point(7, 3)),
        (Point(4, 4), Point(7, 7)),
    ]


@pytest.mark.parametrize(
    "region,line,expected",
    [
        ((Point(2, 2), Point(6, 6)), Line(Point(1, 1), Point(3, 3)), False),
        ((Point(2, 2), Point(6, 6)), Line(Point(4, 4), Point(8, 8)), False),
        ((Point(2, 2), Point(6, 6)), Line(Point(2, 2), Point(5, 5)), True),
        ((Point(2, 2), Point(6, 6)), Line(Point(3, 3), Point(5, 5)), True),
        ((Point(2, 2), Point(6, 6)), Line(Point(1, 1), Point(5, 5)), False),
        ((Point(2, 2), Point(6, 6)), Line(Point(6, 6), Point(8, 8)), False),
        ((Point(2, 2), Point(6, 6)), Line(Point(0, 0), Point(9, 9)), False),
        ((Point(0, 0), Point(9, 9)), Line.from_coords(9, 4, 3, 4), True),
    ],
)
def test_both_endpoints_in_region(
    region: tuple[Point, Point], line: Line, expected: bool
):
    assert both_endpoints_in_region(region, line) == expected


@pytest.mark.parametrize(
    "region,line,expected",
    [
        ((Point(2, 2), Point(6, 6)), Line(Point(1, 1), Point(3, 3)), True),
        ((Point(2, 2), Point(6, 6)), Line(Point(4, 4), Point(8, 8)), True),
        ((Point(2, 2), Point(6, 6)), Line(Point(2, 2), Point(5, 5)), True),
        ((Point(2, 2), Point(6, 6)), Line(Point(3, 3), Point(5, 5)), True),
        ((Point(2, 2), Point(6, 6)), Line(Point(1, 1), Point(5, 5)), True),
        ((Point(2, 2), Point(6, 6)), Line(Point(6, 6), Point(8, 8)), True),
        ((Point(2, 2), Point(6, 6)), Line(Point(0, 0), Point(9, 9)), True),
        ((Point(2, 1), Point(2, 1)), Line(Point(2, 1), Point(2, 2)), True),
        ((Point(7, 4), Point(7, 4)), Line.from_coords(9, 4, 3, 4), True),
        ((Point(7, 4), Point(7, 4)), Line.from_coords(3, 4, 9, 4), True),
    ],
)
def test_line_intersects_region(
    region: tuple[Point, Point], line: Line, expected: bool
):
    assert line_intersects_region(region, line) == expected


test_get_line_segment_in_region_data = [
    (
        (Point(2, 2), Point(6, 6)),
        Line(Point(1, 1), Point(3, 3)),
        Line(Point(2, 2), Point(3, 3)),
    ),
    (
        (Point(2, 2), Point(6, 6)),
        Line(Point(4, 4), Point(8, 8)),
        Line(Point(4, 4), Point(6, 6)),
    ),
    (
        (Point(2, 2), Point(6, 6)),
        Line(Point(2, 2), Point(5, 5)),
        Line(Point(2, 2), Point(5, 5)),
    ),
    (
        (Point(2, 2), Point(6, 6)),
        Line(Point(3, 3), Point(5, 5)),
        Line(Point(3, 3), Point(5, 5)),
    ),
    (
        (Point(2, 2), Point(6, 6)),
        Line(Point(1, 1), Point(5, 5)),
        Line(Point(2, 2), Point(5, 5)),
    ),
    (
        (Point(2, 2), Point(6, 6)),
        Line(Point(6, 6), Point(8, 8)),
        Line(Point(6, 6), Point(6, 6)),
    ),
    (
        (Point(2, 2), Point(6, 6)),
        Line(Point(0, 0), Point(9, 9)),
        Line(Point(2, 2), Point(6, 6)),
    ),
    (
        (Point(2, 1), Point(2, 1)),
        Line(Point(2, 1), Point(2, 2)),
        Line(Point(2, 1), Point(2, 1)),
    ),
    (
        (Point(2, 2), Point(6, 6)),
        Line(Point(0, 0), Point(9, 9)),
        Line(Point(2, 2), Point(6, 6)),
    ),
    (
        (Point(2, 2), Point(6, 6)),
        Line(Point(0, 9), Point(9, 0)),
        Line(Point(3, 6), Point(6, 3)),
    ),
    (
        (Point(2, 2), Point(6, 6)),
        Line(Point(5, 0), Point(5, 9)),
        Line(Point(5, 2), Point(5, 6)),
    ),
    (
        (Point(2, 2), Point(6, 6)),
        Line(Point(0, 5), Point(9, 5)),
        Line(Point(2, 5), Point(6, 5)),
    ),
    (
        (Point(0, 0), Point(7, 7)),
        Line(start=Point(x=8, y=0), end=Point(x=0, y=8)),
        Line(start=Point(x=7, y=1), end=Point(x=1, y=7)),
    ),
    (
        (Point(0, 0), Point(3, 3)),
        Line(start=Point(x=6, y=4), end=Point(x=2, y=0)),
        Line(start=Point(x=3, y=1), end=Point(x=2, y=0)),
    ),
    (
        (Point(0, 0), Point(3, 3)),
        Line(start=Point(x=2, y=0), end=Point(x=6, y=4)),
        Line(start=Point(x=2, y=0), end=Point(x=3, y=1)),
    ),
]


@pytest.mark.parametrize("region,line,expected", test_get_line_segment_in_region_data)
def test_get_line_segment_in_region(
    region: tuple[Point, Point], line: Line, expected: Line
):
    assert get_line_segment_in_region(region, line) == expected


@pytest.mark.parametrize(
    "region, lines, expected",
    [
        (
            (Point(2, 2), Point(6, 6)),
            [
                Line(Point(1, 1), Point(3, 3)),
                Line(Point(4, 4), Point(8, 8)),
                Line(Point(2, 2), Point(5, 5)),
                Line(Point(1, 1), Point(5, 5)),
                Line(Point(6, 6), Point(8, 8)),
                Line(Point(0, 0), Point(9, 9)),
                Line(Point(7, 7), Point(10, 10)),
            ],
            [
                Line(Point(2, 2), Point(3, 3)),
                Line(Point(4, 4), Point(6, 6)),
                Line(Point(2, 2), Point(5, 5)),
                Line(Point(2, 2), Point(5, 5)),
                Line(Point(6, 6), Point(6, 6)),
                Line(Point(2, 2), Point(6, 6)),
            ],
        ),
    ],
)
def test_get_line_segments_in_region(region, lines, expected):
    result = get_line_segments_in_region(region, lines)
    assert len(result) == len(expected)
    for r in result:
        assert r in expected
    for e in expected:
        assert e in result
