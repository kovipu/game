#!/usr/bin/env python3

"""
Prototype for the backend

Handle simulating the board, the robot, inputs, outputs and values
"""

from enum import Enum


class Cardinal(Enum):
    NORTH = (0, 1)
    EAST =  (1, 0)
    SOUTH = (0, -1)
    WEST =  (-1, 0)


class Robot:
    def __init__(self, val=None, x=0, y=0, direction=Cardinal.EAST):
        self.val = val
        self.x, self.y = x, y
        self.direction = direction

    def __repr__(self):
        return 'r({})'.format(self.val)


class Game:
    """Handle storing the board and clipping"""
    def __init__(self, board=[[None] * 5 for _ in range(5)],
                 inputpos={2: 'in'}, outputpos={2: 'out'}):
        self.board = board
        self.inputpos = inputpos
        self.outputpos = outputpos

        # Initialize the robot in the southwest corner of the board
        self.robot = Robot()
        self.board[0][0] = self.robot

    """Helper functions"""

    def _turn(self, direction=None):
        """turn the robot to face direction"""
        if direction is not None:
            self.robot.direction = direction
        return self.robot.direction

    def _push(self, direction):
        """try to push values in direction, return True if success"""
        x, y = self.robot.x, self.robot.y

        # try to find space to push into
        items_to_move = [None]
        item = self.board[y][x]
        while item is not None:
            x += direction.value[0]
            y += direction.value[1]
            try:
                # disable Python's negative index hacks
                if x < 0 or y < 0:
                    raise indexError
                item = self.board[y][x]
            except IndexError:
                # check if there's an output we can push into
                if direction == Cardinal.EAST and y in self.outputpos.keys():
                    self._output(y, items_to_move.pop())
                    break
                return False
            items_to_move.append(item)

        # move the items
        x, y = self.robot.x, self.robot.y
        for item in items_to_move[:-1]:
            x += direction.value[0]
            y += direction.value[1]
            self.board[y][x] = item
        return True

    #TODO
    def _output(self, output, val):
        """output a value"""
        print("outputted {} in output {}".format(val, output))

    def _draw(self):
        """draw a plaintext representation of the board for debugging"""

        inputwall = ['##'] * len(self.board[0])
        for x, name in self.inputpos.items():
            inputwall[x] = name
        print(inputwall)

        board = [row + ['##'] for row in self.board]
        for y, name in self.outputpos.items():
            board[y][-1] = name
        for row in board:
            print(row)

    """Actual commands for the players to use"""

    def move(self, direction=None):
        """move the robot. If no direction given, move where the robot is currently
        facing, return True if succesful"""
        r = self.robot
        direction = self._turn(direction)
        if not self._push(direction):
            return False
        self.board[r.y][r.x] = None
        r.x += direction.value[0]
        r.y += direction.value[1]
        self.board[r.y][r.x] = r
        return True

    def grab(self, direction=None):
        """Make the robot grab a value in neighboring cell in direction"""
        direction = self._turn(direction)
        x = self.robot.x + direction.value[0]
        y = self.robot.y + direction.value[1]
        if self.robot.val is not None or x < 0 or y < 0:
            return False
        try:
            self.robot.val = self.board[y][x]
        except IndexError:
            return False  # trying to grab an item outside of the board
        self.board[y][x] = None
        return True

    def drop(self, direction=None):
        """Make the robot drop the value it's holding in the neighboring cell in direction"""
        direction = self._turn(direction)
        x = self.robot.x + direction.value[0]
        y = self.robot.y + direction.value[1]
        if self.robot.val is None or x < 0 or y < 0:
            return False
        if not self._push(direction):
            return False
        try:
            self.board[y][x] = self.robot.val
        except IndexError:
            return False  # trying to place an item outside of the board
        self.robot.val = None
        return True
