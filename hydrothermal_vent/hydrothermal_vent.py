from dataclasses import dataclass
from math import log2, floor


@dataclass
class Point:
    x: int
    y: int

    def coords(self) -> tuple[int, int]:
        return (self.x, self.y)


@dataclass
class Line:
    start: Point
    end: Point

    @staticmethod
    def from_coords(x1, y1, x2, y2):
        return Line(Point(x1, y1), Point(x2, y2))

    @property
    def points(self) -> list[Point]:
        return [self.start, self.end]


@dataclass
class Region:
    top_left: Point
    bottom_right: Point


def get_number_of_points_which_have_two_or_more_lines_traversing_them(
    lines: list[Line],
) -> int:
    region = get_bounds(lines)
    return get_number_of_overlaps_in_region(region, lines)


def get_number_of_overlaps_in_region(
    region: tuple[Point, Point], lines: list[Line]
) -> int:
    if len(lines) <= 1:
        return 0

    if is_degenerate_region(region):
        value = 0 if len(lines) <= 1 else 1
        return value

    total = 0
    sub_regions = get_sub_regions(region)
    for sub_region in sub_regions:
        sub_lines = get_line_segments_in_region(sub_region, lines)
        total += get_number_of_overlaps_in_region(sub_region, sub_lines)
    return total


def is_degenerate_region(region: tuple[Point, Point]):
    return region[1].x == region[0].x and region[1].y == region[0].y


def get_bounds(lines: list[Line]) -> tuple[Point, Point]:
    """Returns the smallest rectange with edges which are powers of two that entirely contains the lines."""
    points = []
    for line in lines:
        points.extend(line.points)

    x_min, y_min = 0, 0
    x_max, y_max = 0, 0

    for point in points:
        x_min = point.x if point.x < x_min else x_min
        y_min = point.y if point.y < y_min else y_min
        x_max = point.x if point.x > x_max else x_max
        y_max = point.y if point.y > y_max else y_max

    return (
        Point(
            highest_power_of_two_less_than(x_min), highest_power_of_two_less_than(y_min)
        ),
        Point(
            smallest_power_of_two_minus_one_greater_than(x_max),
            smallest_power_of_two_minus_one_greater_than(y_max),
        ),
    )


def smallest_power_of_two_minus_one_greater_than(a):
    # Find the position of the leftmost set bit
    position = 0
    temp = a
    while temp > 0:
        temp >>= 1
        position += 1

    # Generate the smallest integer using bitwise operations
    return (1 << position) - 1


def highest_power_of_two_less_than(n: int) -> int:
    return 0 if n == 0 else 2 ** floor(log2(n))


def get_sub_regions(region: tuple[Point, Point]) -> list[tuple[Point, Point]]:
    bottom_left, top_right = region
    width = top_right.x - bottom_left.x
    height = top_right.y - bottom_left.y

    sub_width = (width + 1) // 2
    sub_height = (height + 1) // 2

    region_center = Point(bottom_left.x + sub_width, bottom_left.y + sub_height)
    region_center_minus_one = Point(region_center.x - 1, region_center.y - 1)
    return [
        (bottom_left, region_center_minus_one),
        (
            Point(bottom_left.x, region_center.y),
            Point(region_center_minus_one.x, top_right.y),
        ),
        (
            Point(region_center.x, bottom_left.y),
            Point(top_right.x, region_center_minus_one.y),
        ),
        (region_center, top_right),
    ]


def select_horizontal_and_vertical_lines(lines: list[Line]) -> list[Line]:
    return list(filter(lambda l: is_horizontal(l) or is_vertical(l), lines))


def is_horizontal(line: Line) -> bool:
    return line.start.x == line.end.x


def is_vertical(line: Line) -> bool:
    return line.start.y == line.end.y


def get_line_segments_in_region(region, lines):
    return [
        subline
        for line in lines
        if (subline := get_line_segment_in_region(region, line)) is not None
    ]


def get_line_segment_in_region(region: tuple[Point, Point], line: Line) -> Line | None:
    region_bottom_left, region_top_right = region

    if both_endpoints_in_region(region, line):
        return line

    if not line_intersects_region(region, line):
        return None

    if is_horizontal(line) or is_vertical(line):
        # Find intersection points
        x1, y1 = max(region_bottom_left.x, line.start.x), max(
            region_bottom_left.y, line.start.y
        )
        x2, y2 = min(region_top_right.x, line.end.x), min(
            region_top_right.y, line.end.y
        )

        # Create line segment from intersection points
        return Line(Point(x1, y1), Point(x2, y2))
    else:
        delta_x = -1 if line.start.x > line.end.x else 1
        x_range = range(
            line.start.x, line.end.x + delta_x, delta_x
        )

        delta_y = -1 if line.start.y > line.end.y else 1
        y_range = range(
            line.start.y, line.end.y + delta_y, delta_y
        )

        points = [
            Point(x, y)
            for x, y in zip(x_range, y_range)
            if region_bottom_left.x <= x <= region_top_right.x
            and region_bottom_left.y <= y <= region_top_right.y
        ]
        return Line(points[0], points[-1]) if points else None



def both_endpoints_in_region(region, line) -> bool:
    bottom_left, top_right = region
    return (
        bottom_left.x <= line.start.x <= top_right.x
        and bottom_left.y <= line.start.y <= top_right.y
        and bottom_left.x <= line.end.x <= top_right.x
        and bottom_left.y <= line.end.y <= top_right.y
    )


def line_intersects_region(region: tuple[Point, Point], line: Line) -> bool:
    region_bottom_left, region_top_right = region

    # If one end of the line is in the region then we're guaranteed an intersection
    for point in line.points:
        if (
            region_bottom_left.x <= point.x <= region_top_right.x
            and region_bottom_left.y <= point.y <= region_top_right.y
        ):
            return True

    # horizontal and vertical lines:
    if (
        region_bottom_left.y <= line.start.y
        and line.end.y <= region_top_right.y
        and line.start.x <= region_bottom_left.x
        and line.end.x >= region_top_right.x
    ):
        return True

    if (
        region_bottom_left.y <= line.start.y
        and line.end.y <= region_top_right.y
        and line.end.x <= region_bottom_left.x
        and line.start.x >= region_top_right.x
    ):
        return True

    if (
        region_bottom_left.x <= line.start.x
        and line.end.x <= region_top_right.x
        and line.start.y <= region_bottom_left.y
        and line.end.y >= region_top_right.y
    ):
        return True

    if (
        region_bottom_left.x <= line.start.x
        and line.end.x <= region_top_right.x
        and line.end.y <= region_bottom_left.y
        and line.start.y >= region_top_right.y
    ):
        return True

    edges = [
        Line(region_bottom_left, Point(region_bottom_left.x, region_top_right.y)),
        Line(Point(region_bottom_left.x, region_top_right.y), region_top_right),
        Line(region_bottom_left, Point(region_top_right.x, region_bottom_left.y)),
        Line(Point(region_top_right.x, region_bottom_left.y), region_top_right),
    ]

    for edge in edges:
        if line_crosses_edge(edge, line):
            return True

    return False


def line_crosses_edge(edge: Line, line: Line) -> bool:
    # edge will either be horizontal or vertical, line will be at 45 degrees

    x_range = range(line.start.x, line.end.x, -1 if line.start.x > line.end.x else 1)
    y_range = range(line.start.y, line.end.y, -1 if line.start.y > line.end.y else 1)

    points = [Point(p[0], p[1]) for p in zip(x_range, y_range)]

    for point in points:
        if point_is_on_line(point, edge):
            return True

    return False


def point_is_on_line(point: Point, line: Line):
    # line must be horizontal or vertical
    if is_horizontal(line):
        if point.y != line.start.y:
            return False
        return line.start.x <= point.x <= line.end.x

    if is_vertical(line):
        if point.x != line.start.x:
            return False
        return line.start.y <= point.y <= line.end.x

    raise ValueError("Line is not horizontal or vertical.")
