import fileinput

from hydrothermal_vent import (
    Line,
    get_number_of_points_which_have_two_or_more_lines_traversing_them,
    select_horizontal_and_vertical_lines,
)


lines = []
for line in fileinput.input("input/day05.txt"):
    new_line = line.replace(" -> ", ",")
    coord = map(int, new_line.strip().split(","))
    lines.append(Line.from_coords(*coord))


result = get_number_of_points_which_have_two_or_more_lines_traversing_them(lines)
print(result)
