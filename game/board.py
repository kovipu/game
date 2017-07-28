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
        return('r({})'.format(self.val))


class Game:
    """Handle storing the board and clipping"""
    def __init__(self, board=[[None] * 5 for _ in range(5)], inputpos=[(2, 'in')], 
                 outputpos=[(2, 'out')]):
        self.board = board
        self.inputpos = inputpos
        self.outputpos = outputpos
        
        # Initialize the robot in the southwest corner of the board
        self.robot = Robot()
        self.board[0][0] = self.robot

    """Helper functions"""

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
                if x < 0 or y < 0: # disable Python's negative index hacks
                    raise indexError
                item = self.board[y][x]
            except IndexError: # check if there's an output we can push into
                if direction == Cardinal.EAST and y in (n for n, _ in self.outputpos):
                    self._output(y, items_to_move.pop())
                    break
                else:
                    return(False)
            items_to_move.append(item)
    
        # move the items
        x, y = self.robot.x, self.robot.y
        for item in items_to_move[:-1]:
            x += direction.value[0]
            y += direction.value[1]
            self.board[y][x] = item
        return(True)
        
    def _output(self, output, val):
        """output a value"""
        print("outputted {} in output {}".format(val, output))

    def _draw(self):
        """draw the board in console for debugging"""
        
        inputwall = ['##'] * len(self.board[0])
        for pos, name in self.inputpos:
            inputwall[pos] = name
        print(inputwall)
            
        board = [row + ['##'] for row in self.board]
        for pos, name in self.outputpos:
            board[pos][-1] = name
        for row in board:
            print(row)   

    """Actual commands for the players to use"""

    def move(self, direction=None):
        """move the robot. If no direction given, move where the robot is currently 
        facing, return True if succesful"""
        r = self.robot
        if direction is None:
            direction = r.direction
        if self._push(direction):
            self.board[r.y][r.x] = None
            r.x += direction.value[0]
            r.y += direction.value[1]
            self.board[r.y][r.x] = r
            return(True)
        else:
            return(False)

    def grab(self, direction=None):
        """Make the robot grab a value in direction"""
        if direction is None:
            direction = self.robot.direction
        x, y = self.robot.x + direction.value[0], self.robot.y + direction.value[1]
        try:
            if x < 0 or y < 0:
                raise IndexError
            item = self.board[y][x]
            if item is not None:
                self.robot.val = item
                self.board[y][x] = None
                return(True)
            else:
                raise TypeError
        except IndexError or TypeError:
            return(False)