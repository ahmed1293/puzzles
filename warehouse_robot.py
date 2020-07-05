from dataclasses import dataclass
from typing import List

# EXERCISE: https://github.com/guardian/coding-exercises/tree/master/warehouse-robot

GRID_SIZE = 10


@dataclass
class GridItem:
    x: int
    y: int
    robot_is_here: bool = False
    crate_is_here: bool = False

    def __repr__(self):
        if not self.robot_is_here and not self.crate_is_here:
            return f'({self.x}, {self.y})'
        elif self.robot_is_here and not self.crate_is_here:
            return 'ROBOT'
        elif not self.robot_is_here and self.crate_is_here:
            return 'CRATE'
        else:
            return 'ROBOT_CRATE'


class Grid:

    def __init__(self):
        self._items = [GridItem(x, y) for x in range(0, GRID_SIZE) for y in range(0, GRID_SIZE)]
        self.get_item(4, 4).crate_is_here = True
        self.get_item(GRID_SIZE-1, GRID_SIZE-1).crate_is_here = True

    def get_item(self, x: int, y: int):
        # not ideal, but meh
        return [item for item in self if item.x == x and item.y == y][0]

    def __getitem__(self, item):
        return self._items[item]

    def print(self):
        rows = []
        row = ''
        for y in range(0, GRID_SIZE):
            for x in range(0, GRID_SIZE):
                row += f' {self.get_item(x, y)}'
            rows.append(row)
            row = ''

        for row in rows[::-1]:
            print(row)


class Robot:

    def __init__(self, grid: Grid, carrying_crate=False):
        self.grid = grid
        self.position = self.grid.get_item(0, 0)
        self.grid.get_item(0, 0).robot_is_here = True
        self.carrying_crate = carrying_crate

    def _move(self, x, y):
        try:
            new_position = self.grid.get_item(x=x, y=y)
        except IndexError:
            print('Keep the robot on the board!')
            return
        new_position.robot_is_here = True
        if self.carrying_crate:
            new_position.crate_is_here = True
        self.position.robot_is_here = False

        if self.carrying_crate:
            self.position.crate_is_here = False
        self.position = new_position

    def grab_crate(self):
        if self.carrying_crate:
            print('Robot cannot carry more than 1 crate')
        if not self.position.crate_is_here:
            print('Robot cannot lift crate if he is not on the same grid item')
        self.carrying_crate = True

    def drop_crate(self):
        self.carrying_crate = False

    def move_north(self):
        self._move(self.position.x, self.position.y+1)

    def move_south(self):
        self._move(x=self.position.x, y=self.position.y - 1)

    def move_east(self):
        self._move(x=self.position.x + 1, y=self.position.y)

    def move_west(self):
        self._move(x=self.position.x - 1, y=self.position.y)


class RobotController:

    commands = {
        'N': lambda robot: robot.move_north(),
        'S': lambda robot: robot.move_south(),
        'E': lambda robot: robot.move_east(),
        'W': lambda robot: robot.move_west(),
        'G': lambda robot: robot.grab_crate(),
        'D': lambda robot: robot.drop_crate()
    }

    def __init__(self, robot: Robot):
        self.robot = robot

    def get_command(self) -> List[str]:
        command = input('Where would you like the robot to move? ')
        # todo: validate entry
        return command.split()

    def execute_command(self, commands):
        for command in commands:
            func = self.commands.get(command)
            if not func:
                raise ValueError(f'Command {command} is not recognised')
            func(self.robot)


if __name__ == '__main__':
    _grid = Grid()
    _robot = Robot(grid=_grid)
    _controller = RobotController(robot=_robot)
    _grid.print()
    while True:
        _command = _controller.get_command()
        _controller.execute_command(_command)
        _grid.print()
