from reactor_reboot import Grid, parse_step

if __name__ == "__main__":
    with open("input/day22.txt") as input_text:
        lines = input_text.readlines()

    steps = []
    for line in lines:
        step = parse_step(line)
        if step is not None:
            steps.append(step)

    grid = Grid()

    for step in steps:
        if step.state:
            grid.add_cuboid(step.cuboid)
        else:
            grid.subtract_cuboid(step.cuboid)

    print(grid.on_cubes())

    steps = []
    for line in lines:
        step = parse_step(line, part1=False)
        if step is not None:
            steps.append(step)

    grid = Grid()

    for step in steps:
        if step.state:
            grid.add_cuboid(step.cuboid)
        else:
            grid.subtract_cuboid(step.cuboid)

    print(grid.on_cubes())
