# ================================================================================
# +
# + import
# +
# ================================================================================
import pygame as pg
import numpy as np
import sys
import random
import copy

import time
import datetime

import math

from enum import Enum, unique

# ================================================================================
# +
# + constant
# +
# ================================================================================
# columns & rows of main area
ROW = 20
COL = 10

COL_MID = COL/2

# pixels of each cell
CELL_SIZE = 25

SOLID_BOX_SIZE = CELL_SIZE - 1

# columns of right hand side
RHS = 6


@unique
class MoveDir(Enum):
    Unknown = 0
    Left = 1
    Up = 2
    Right = 3
    Down = 4


COLOR_BG = '#1e1e1e'
COLOR_NONE = '#3c3c3c'

COLOR_FIXED = '#3c0000'

DEBUG_MODE = True


# ================================================================================
# +
# + constant
# +
# ================================================================================

FPS = 30


zeros_2_1 = np.zeros((2, 1), dtype=int)


# ================================================================================
# +
# + Class
# +
# ================================================================================


class Board():
    # ============================================================
    # + xxxxxx
    # ============================================================
    def __init__(self, surf=None) -> None:
        super().__init__()
        self._surf = surf

        self._matrix = np.zeros((ROW, COL), dtype=int)
        self._color = [['' for _ in range(0, COL)] for _ in range(0, ROW)]

    # ============================================================
    # + xxxxxx
    # ============================================================
    def draw_bg(self):
        print('board bg draw')
        for i in range(0, ROW):
            for j in range(0, COL):
                pg.draw.rect(surface=self._surf, color=COLOR_NONE, rect=(
                    j*CELL_SIZE, i*CELL_SIZE, SOLID_BOX_SIZE, SOLID_BOX_SIZE))

    # ============================================================
    # + xxxxxx
    # ============================================================
    def record_shape_to_matrix(self, board_coords_rc):
        for i in range(0, len(board_coords_rc[0])):
            tmp_r = board_coords_rc[0, i]
            tmp_c = board_coords_rc[1, i]
            self._matrix[tmp_r, tmp_c] = 1
        self.delete_lines()

    # ============================================================
    # + xxxxxx
    # ============================================================
    def delete_lines(self):
        for i in range(0, ROW):
            
            tmp_line = self._matrix[i, :]
            if all(tmp_line):
                if i == 0:
                    # special for top line, just reset top line
                    self._matrix[0, :] = 0
                else:
                    # delete current line & move rest lines one step down
                    self._matrix[1:i, :] = self._matrix[:(i - 1), :]
                    self._matrix[0, :] = 0

    # ============================================================
    # + xxxxxx
    # ============================================================

    def get_board_matrix(self):
        return self._matrix

    # ============================================================
    # + xxxxxx
    # ============================================================
    def draw_cells(self):
        print('board cells draw')
        # print(self._matrix)
        for i in range(0, ROW):
            for j in range(0, COL):
                if self._matrix[i, j] == 1:
                    pg.draw.rect(surface=self._surf, color=COLOR_FIXED, rect=(
                        j*CELL_SIZE, i*CELL_SIZE, SOLID_BOX_SIZE, SOLID_BOX_SIZE))


# ================================================================================
# +
# + Class
# +
# ================================================================================


class Shape():
    # ============================================================
    # + __init__
    # ============================================================
    def __init__(self, surf=None, board=None, name='', pos=zeros_2_1, rc=zeros_2_1, data: np.ndarray = None):
        super().__init__()

        self._surf = surf
        self._board: Board = board
        self._name = name

        # shape will be fixed if it can't move down
        self._fixed = False

        self._erased = True

        # direction to move right
        self._dir: int = 0

        # refer to game board
        # x to right
        # y to bottom
        self._pos_x: int = pos[0]
        self._pos_y: int = pos[1]

        # position of shape [x, y]' refer to game board
        # 2*1
        self._pos = zeros_2_1

        self._speed: int = 5
        self._accumulated_steps_info: float = 0

        # shape date, ref to local cs
        # [x1, x2, x3, ...
        #  y1, y2, y3, ...]
        # 2*N
        self._data = data

        # local cs
        # rotate center[x, y]'
        # 2*1
        self._rc = rc

        self._data_len = len(self._data[0])

        self._board_coords_pixel = np.zeros((2, self._data_len), dtype=int)

        # use for board matrix updating
        self._board_coords_rc = np.zeros((2, self._data_len), dtype=int)

        # use for collision checking
        self._board_coords_rc_preview = np.zeros(
            (2, self._data_len), dtype=int)

        # [x1, x2, x3, ...
        #  y1, y2, y3, ...]
        # 2*N
        self._rc_tiled = None

        # rot transform matrix
        self._rot = np.array([[0, -1], [1, 0]], dtype=int)

        # update the depend pop
        self._update_rc_tiled()
        self._update_pos()

    # ============================================================
    # + _update_pos
    # ============================================================

    def _update_pos(self):
        self._pos[0] = self._pos_x
        self._pos[1] = self._pos_y

    # ============================================================
    # + _update_rc_tiled
    # ============================================================

    def _update_rc_tiled(self):
        cols = self._data_len
        self._rc_tiled = np.tile(self._rc, (1, cols))
        # print('===============')
        # print(self._rc)
        # print(self._rc_tiled)
        # print('===============')
        # print(self._data)

    # ============================================================
    # + _check_left_bound
    # ============================================================
    def _check_left_bound(self, pos_x, data=None) -> bool:
        """check if the giving pos_x will let the shape exceed bound

        Args:
            pos_x (_type_): _description_
        """

        if data is None:
            data = self._data

        rst = (pos_x + min(data[0, :]) < 0)
        print('_check_left_bound >> {}'.format(rst))

        return pos_x + min(data[0, :]) < 0

    # ============================================================
    # + _check_right_bound
    # ============================================================
    def _check_right_bound(self, pos_x, data=None) -> bool:
        """check if the giving pos_x will let the shape exceed bound

        Args:
            pos_x (_type_): _description_
        """

        if data is None:
            data = self._data

        rst = (pos_x + max(data[0, :]) >= COL)
        print('_check_right_bound >> {}'.format(rst))

        return pos_x + max(data[0, :]) >= COL

    # ============================================================
    # + _check_upper_bound
    # ============================================================
    def _check_upper_bound(self, pos_y, data=None) -> bool:
        """check if the giving pos_x will let the shape exceed bound

        Args:
            pos_x (_type_): _description_
        """

        if data is None:
            data = self._data

        rst = (pos_y + max(data[1, :]) < -1)
        print('_check_upper_bound >> {}'.format(rst))

        return pos_y + max(data[1, :]) < -1

    # ============================================================
    # + _check_lower_bound
    # ============================================================
    def _check_lower_bound(self, pos_y, data=None) -> bool:
        """check if the giving pos_x will let the shape exceed bound

        Args:
            pos_x (_type_): _description_
        """

        if data is None:
            data = self._data

        rst = (pos_y + max(data[1, :]) >= ROW)
        print('_check_lower_bound >> {}'.format(rst))

        return pos_y + max(data[1, :]) >= ROW

    # ============================================================
    # + _get_minimum_y_cords
    # ============================================================

    def get_minimum_y_cords(self) -> int:
        """compute the minimum y shape can put

        Args:
            pos_x (_type_): _description_
        """

        return -1 - (self._pos_y + max(self._data[1, :]))

    # ============================================================
    # + set_min_y_cords
    # ============================================================
    def set_min_y_cords(self) -> int:
        """compute the minimum y shape can put

        Args:
            pos_x (_type_): _description_
        """
        uy = self.get_minimum_y_cords()
        self.pos_y = uy

    # ============================================================
    # + set_init_x_cords
    # ============================================================
    def set_init_x_cords(self) -> int:
        """compute the minimum y shape can put

        Args:
            pos_x (_type_): _description_
        """
        self.pos_x = COL_MID

    # ============================================================
    # + _check_collision
    # ============================================================

    def _check_collision(self, pos_x=None, pos_y=None, data=None) -> bool:
        """check if the giving pos will collide the board's fixed cells

        Args:
            pos_x (_type_, optional): _description_. Defaults to None.
            pos_y (_type_, optional): _description_. Defaults to None.
            data (_type_, optional): _description_. Defaults to None.

        Returns:
            bool: _description_
        """

        print('_check_collision')
        if pos_x is None:
            pos_x = self.pos_x
        if pos_y is None:
            pos_y = self.pos_y
        if data is None:
            data = self._data

        tmp_matrix = self._board.get_board_matrix()
        self.update_preview_coords_ref_to_board_cs_in_rc(
            pos_x=pos_x, pos_y=pos_y, data=data)

        # check each cell of current shape one by one
        for i in range(0, self._data_len):

            tmp_r = self._board_coords_rc_preview[0][i]
            tmp_c = self._board_coords_rc_preview[1][i]

            if tmp_r < 0 or tmp_r >= ROW or tmp_c < 0 or tmp_c >= COL:
                # ignore the cells of shape which exceed the region of board
                continue
            elif tmp_matrix[tmp_r][tmp_c] == 1:
                print('_check_collision   >> {}'.format(True))
                return True

        # if none of cells are 1, no collistion found, return false
        print('_check_collision   >> {}'.format(False))
        return False

    # ============================================================
    # + one step move
    # ============================================================

    def move_left(self) -> bool:
        self.erase()
        self._dir = MoveDir.Left
        self.pos_x -= 1

    def move_right(self):
        self.erase()
        self._dir = MoveDir.Right
        self.pos_x += 1

    def move_up(self):
        self.erase()
        self._dir = MoveDir.Up
        self.pos_y -= 1

    def move_down(self):
        self.erase()
        self._dir = MoveDir.Down
        self.pos_y += 1

    def move_down_till_fixed(self):
        while not self.fixed:
            self.erase()
            self.pos_y += 1

    def move_down_by_speed(self):

        # compute the accumulated delta y which shape will be moved

        delta_uy = self.speed*(1/FPS)
        self._accumulated_steps_info += delta_uy

        steps = math.floor(self._accumulated_steps_info)
        print('steps steps steps')
        print(self._accumulated_steps_info)
        if steps >= 1.0:
            self.erase()
            self._accumulated_steps_info -= steps
            self._dir = MoveDir.Down
            for i in range(steps):
                self.move_down()
                # self.pos_y += 1

    def freeze(self):
        self.update_final_coords_ref_to_board_cs_in_rc()
        self._board.record_shape_to_matrix(
            board_coords_rc=self._board_coords_rc)

    # ============================================================
    # + rot_acw
    # ============================================================

    def rot_acw(self):
        """_summary_
            rot shape on anti-clockwise
            please note the pygame coordinate system: 
            x: right ward
            y: down  ward
            so when it rotate anti-clockwise in shape cs, 
            it looks like rotate clockwise in pygame cs.
        """
        if self._name == 'box':
            # don't rotate box
            return

        tmp_data = np.matmul(self._rot, self._data -
                             self._rc_tiled) + self._rc_tiled

        # 1st compute if the target position[post-rotated] will get collision
        # if not, do shape rotation
        delta_x = 0
        delta_y = 0
        if self._check_left_bound(pos_x=self.pos_x, data=tmp_data):
            delta_x = -(self._pos_x + min(tmp_data[0, :]))
        if self._check_right_bound(pos_x=self.pos_x, data=tmp_data):
            delta_x = -((self._pos_x + max(tmp_data[0, :]) - COL) + 1)

        if self._check_upper_bound(pos_y=self.pos_y, data=tmp_data):
            delta_y = -(self._pos_y + min(tmp_data[1, :]))
        if self._check_lower_bound(pos_y=self.pos_y, data=tmp_data):
            delta_y = -((self._pos_y + max(tmp_data[1, :]) - ROW) + 1)

        # print(delta_x)
        # print(delta_y)
        target_pos_x = self.pos_x + delta_x
        target_pos_y = self.pos_y + delta_y

        print(' collision rot')
        is_overlapped = self._check_collision(
            pos_x=target_pos_x, pos_y=target_pos_y, data=tmp_data)
        if is_overlapped:
            # do nothing if rotation get collide
            return
        else:
            # do rotation here
            print('pos x y')
            print(self.pos_x)
            print(self.pos_y)
            print('delta x y')
            print(delta_x)
            print(delta_y)
            print('final x y')
            print(target_pos_x)
            print(target_pos_y)
            print('matrix before')
            print(self._data)
            print('matrix after')
            print(tmp_data)
            self._data = tmp_data
            # self.pos_x += delta_x
            # self.pos_y += delta_y
            self._pos_x = target_pos_x
            self._pos_y = target_pos_y
            self._update_pos()

        # # adjust the position if exceed the boundary
        # if self._check_left_bound(pos_x=self.pos_x):
        #     print('<----')
        #     delta_x = - (self._pos_x + min(self._data[0, :]))
        #     print(delta_x)
        #     self.pos_x += delta_x
        # if self._check_right_bound(pos_x=self.pos_x):
        #     print('---->')
        #     delta_x = (self._pos_x + max(self._data[0, :]) - COL) + 1
        #     print(delta_x)
        #     self.pos_x -= delta_x

    # ============================================================
    # + xxx
    # ============================================================

    def update_coords_ref_to_board_cs_in_pixel(self):
        for i in range(0, self._data_len):
            # coord x
            self._board_coords_pixel[0][i] = int(
                (self._data[0][i] + self._pos[0])*CELL_SIZE)
            # coord y
            self._board_coords_pixel[1][i] = int(
                (self._data[1][i] + self._pos[1])*CELL_SIZE)

    # ============================================================
    # + xxx
    # ============================================================
    def update_preview_coords_ref_to_board_cs_in_rc(self, pos_x, pos_y, data=None):
        print('update_preview_coords_ref_to_board_cs_in_rc')
        if data is None:
            data = self._data
        # col & row id
        for i in range(0, self._data_len):
            # col
            self._board_coords_rc_preview[1][i] = int(
                (data[0][i] + pos_x))
            # row
            self._board_coords_rc_preview[0][i] = int(
                (data[1][i] + pos_y))

        print('---shape cords---')
        print(self._board_coords_rc_preview)
        print('---shape cords---')

    # ============================================================
    # + xxx
    # ============================================================
    def update_final_coords_ref_to_board_cs_in_rc(self):
        # col & row id
        for i in range(0, self._data_len):
            # col
            self._board_coords_rc[1][i] = int(
                (self._data[0][i] + self._pos[0]))
            # row
            self._board_coords_rc[0][i] = int(
                (self._data[1][i] + self._pos[1]))

    # ============================================================
    # + erase
    # ============================================================

    def erase(self):
        """erase shape on target surface

        Args:
            surf (_type_): _description_
            shape (_type_, optional): _description_. Defaults to None.
        """
        if self._data is None:
            print('no shape data to draw')

        if not self._erased:
            print('shape erased')
            self.update_coords_ref_to_board_cs_in_pixel()
            for i in range(0, self._data_len):
                tmp_x = self._board_coords_pixel[0][i]
                tmp_y = self._board_coords_pixel[1][i]
                pg.draw.rect(surface=self._surf, color=COLOR_NONE, rect=(
                    tmp_x, tmp_y, SOLID_BOX_SIZE, SOLID_BOX_SIZE))

            self._erased = True

    # ============================================================
    # + draw
    # ============================================================

    def draw(self):
        """draw shape on target surface

        Args:
            surf (_type_): _description_
            shape (_type_, optional): _description_. Defaults to None.
        """
        if self._data is None:
            print('no shape data to draw')

        print('shape draw')
        self.update_coords_ref_to_board_cs_in_pixel()
        for i in range(0, self._data_len):
            tmp_x = self._board_coords_pixel[0][i]
            tmp_y = self._board_coords_pixel[1][i]
            pg.draw.rect(surface=self._surf, color='red', rect=(
                tmp_x, tmp_y, SOLID_BOX_SIZE, SOLID_BOX_SIZE))

        self._erased = False

    # ============================================================
    # + get/set
    # ============================================================

    # ========================================
    # ========================================

    @property
    def pos_x(self):
        return self._pos_x

    @pos_x.setter
    def pos_x(self, pos_x):
        print('************************************')
        print('')
        print('try to changing pos x')
        print('')
        # print(self._board.get_board_matrix())
        if not self._fixed:
            # print('changing position')
            # print(min(self._data[0, :]))
            # print(max(self._data[0, :]))
            # print(pos_x)

            is_exceed_left_bound = self._check_left_bound(pos_x=pos_x)
            is_exceed_right_bound = self._check_right_bound(pos_x=pos_x)

            if is_exceed_left_bound or is_exceed_right_bound:
                # return for no action
                return

            # no need over lap cheching when move to left or right
            # is_overlapped = self._check_collision(pos_x=pos_x)
            # if is_overlapped:
            #     return

            if (not is_exceed_left_bound) and (not is_exceed_right_bound):

                self._pos_x = pos_x
                self._update_pos()
            # print(self._pos_x)

    # ========================================
    # ========================================
    @property
    def pos_y(self):
        return self._pos_y

    @pos_y.setter
    def pos_y(self, pos_y):
        print('************************************')
        print('')
        print('try to changing pos y')
        print('')
        # print(self._board.get_board_matrix())
        if not self._fixed:

            # print('changing position')
            # print(min(self._data[1, :]))
            # print(max(self._data[1, :]))
            # print(pos_y)
            is_exceed_upper_bound = self._check_upper_bound(pos_y=pos_y)
            is_exceed_lower_bound = self._check_lower_bound(pos_y=pos_y)
            if is_exceed_lower_bound:
                # fix current shape
                self.fixed = True
                return

            if is_exceed_upper_bound:
                # return for no action
                return

            is_overlapped = self._check_collision(pos_y=pos_y)
            if is_overlapped:
                self.fixed = True
                return

            if (not is_exceed_upper_bound) and (not is_exceed_lower_bound):
                self._pos_y = pos_y
                self._update_pos()
                return
            # print(self._pos_y)

    # ========================================
    # ========================================
    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        self._speed = speed

    # ========================================
    # ========================================
    @property
    def rc(self):
        return self._rc

    @rc.setter
    def rc(self, rc):
        # update
        self._rc = rc
        # update _rc_tiled here
        self._update_rc_tiled()

    # ========================================
    # ========================================
    @property
    def fixed(self):
        return self._fixed

    @fixed.setter
    def fixed(self, fixed):
        self._fixed = fixed
        if fixed:
            self.freeze()


# ================================================================================
# +
# + Class
# +
# ================================================================================
class TetrisShapes():

    # ============================================================
    # + __init__
    # ============================================================
    def __init__(self, surf=None, board=None) -> None:
        self._surf = surf
        self._board = board

        self._shape_func_list = []

        self._collect_shape_func_list()

    # ============================================================
    # + _collect_shape_func_list
    # ============================================================
    def _collect_shape_func_list(self) -> list:
        self._shape_func_list.append(self._create_shape_I)
        self._shape_func_list.append(self._create_shape_L1)
        self._shape_func_list.append(self._create_shape_L2)
        self._shape_func_list.append(self._create_shape_Z1)
        self._shape_func_list.append(self._create_shape_Z2)
        self._shape_func_list.append(self._create_shape_B)
        self._shape_func_list.append(self._create_shape_A)

    # ============================================================
    # + _create_shape_L1
    # ============================================================

    def _create_shape_L1(self) -> Shape:
        # x: right ward
        # y: up    ward

        # ------
        #  *
        #  *
        #  * *
        # ------
        data = np.array([[0, 0, 0, 1], [2, 1, 0, 0]])
        rc = np.array([[0], [1]])
        tmp_shape = Shape(surf=self._surf, board=self._board,
                          pos=[COL_MID-1, 0], rc=rc, data=data)
        tmp_shape.set_min_y_cords()
        return tmp_shape

    # ============================================================
    # + _create_shape_L2
    # ============================================================

    def _create_shape_L2(self) -> Shape:
        # x: right ward
        # y: up    ward

        # ------
        #    *
        #    *
        #  * *
        # ------
        data = np.array([[0, 1, 1, 1], [0, 0, 1, 2]])
        rc = np.array([[1], [1]])
        tmp_shape = Shape(surf=self._surf, board=self._board,
                          pos=[COL_MID-1, 0], rc=rc, data=data)
        tmp_shape.set_min_y_cords()
        return tmp_shape

    # ============================================================
    # + _create_shape_I
    # ============================================================
    def _create_shape_I(self) -> Shape:
        # x: right ward
        # y: up    ward
        # ------
        #  *
        #  *
        #  *
        #  *
        # ------
        data = np.array([[0, 0, 0, 0], [3, 2, 1, 0]])
        rc = np.array([[0], [1]])
        tmp_shape = Shape(surf=self._surf, board=self._board,
                          pos=[COL_MID, 0], rc=rc, data=data)
        tmp_shape.set_min_y_cords()
        return tmp_shape

    # ============================================================
    # + _create_shape_Z1
    # ============================================================
    def _create_shape_Z1(self) -> Shape:
        # x: right ward
        # y: up    ward
        # ------
        #  * *
        #    * *
        # ------
        data = np.array([[-1, 0, 0, 1], [1, 1, 0, 0]])
        rc = np.array([[0], [0]])
        tmp_shape = Shape(surf=self._surf, board=self._board,
                          pos=[COL_MID, 0], rc=rc, data=data)
        tmp_shape.set_min_y_cords()
        return tmp_shape

    # ============================================================
    # + _create_shape_Z2
    # ============================================================
    def _create_shape_Z2(self) -> Shape:
        # x: right ward
        # y: up    ward
        # ------
        #    * *
        #  * *
        # ------
        data = np.array([[-1, 0, 0, 1], [0, 0, 1, 1]])
        rc = np.array([[0], [0]])

        tmp_shape = Shape(surf=self._surf, board=self._board,
                          pos=[COL_MID, 0], rc=rc, data=data)
        tmp_shape.set_min_y_cords()
        return tmp_shape

    # ============================================================
    # + _create_shape_B
    # ============================================================
    def _create_shape_B(self) -> Shape:
        # x: right ward
        # y: up    ward
        # ------
        #  * *
        #  * *
        # ------
        data = np.array([[0, 0, 1, 1], [1, 0, 0, 1]])
        rc = np.array([[1], [1]])
        name = 'box'
        tmp_shape = Shape(surf=self._surf, board=self._board,
                          name=name, pos=[COL_MID-1, 0], rc=rc, data=data)
        tmp_shape.set_min_y_cords()
        return tmp_shape

    # ============================================================
    # + _create_shape_A
    # ============================================================
    def _create_shape_A(self) -> Shape:
        # x: right ward
        # y: up    ward
        # ------
        #    *
        #  * * *
        # ------
        data = np.array([[0, 1, 2, 1], [0, 0, 0, 1]])
        rc = np.array([[1], [0]])
        tmp_shape = Shape(surf=self._surf, board=self._board,
                          pos=[COL_MID-1, 0], rc=rc, data=data)
        tmp_shape.set_min_y_cords()
        return tmp_shape

    # ============================================================
    # + random_shape
    # ============================================================
    def random_shape(self) -> Shape:
        tmp_shape_func = random.choice(self._shape_func_list)
        return tmp_shape_func()

# ================================================================================
# +
# + methods
# +
# ================================================================================

def game_procedure(cur_shape:Shape, game_board:Board, tetris_shapes:TetrisShapes):
    print('  ------ main while loop ------')
    # while_counter += 1
    # print(' >> while_counter >> {} time: {}'.format(while_counter, datetime.datetime.now()))
    if cur_shape.fixed:
        # create a new shape
        cur_shape = tetris_shapes.random_shape()

    # enforced one step move down in each step
    cur_shape.move_down_by_speed()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.K_ESCAPE:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                # move left
                cur_shape.move_left()
            elif event.key == pg.K_RIGHT:
                # move right
                cur_shape.move_right()
            elif event.key == pg.K_UP:
                # move up
                cur_shape.move_up()
            elif event.key == pg.K_DOWN:
                # move down
                cur_shape.move_down()
            elif event.key == pg.K_SPACE:
                # move down till fixed
                cur_shape.move_down_till_fixed()
            elif event.key == pg.K_r:
                # move down
                cur_shape.rot_acw()

    game_board.draw_bg()
    game_board.draw_cells()
    cur_shape.draw()

    pg.display.update()



def main():

    win_wide = (COL + RHS)*CELL_SIZE
    win_height = ROW*CELL_SIZE

    pg.init()
    pg.display.set_caption('Tetris')

    clock = pg.time.Clock()

    # init main window
    surf = pg.display.set_mode((win_wide, win_height))

    # set bg color
    # pg.display.set_icon()
    surf.fill(color=COLOR_BG)
    # pg.display.flip()

    game_board = Board(surf=surf)
    tetris_shapes = TetrisShapes(surf=surf, board=game_board)

    # init the 1st one
    cur_shape = tetris_shapes.random_shape()
    print(' cur_shape id: {}'.format(id(cur_shape)))
    

    while_counter = 0
    while True:

        print('  ------ main while loop ------')
        # while_counter += 1
        # print(' >> while_counter >> {} time: {}'.format(while_counter, datetime.datetime.now()))
        if cur_shape.fixed:
            # create a new shape
            cur_shape = tetris_shapes.random_shape()
            print(' cur_shape id: {}'.format(id(cur_shape)))

        # enforced one step move down in each step
        cur_shape.move_down_by_speed()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.K_ESCAPE:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    # move left
                    cur_shape.move_left()
                elif event.key == pg.K_RIGHT:
                    # move right
                    cur_shape.move_right()
                elif event.key == pg.K_UP:
                    # move up
                    cur_shape.move_up()
                elif event.key == pg.K_DOWN:
                    # move down
                    cur_shape.move_down()
                elif event.key == pg.K_SPACE:
                    # move down till fixed
                    cur_shape.move_down_till_fixed()
                elif event.key == pg.K_r:
                    # move down
                    cur_shape.rot_acw()

        game_board.draw_bg()
        game_board.draw_cells()
        cur_shape.draw()

        pg.display.update()
        clock.tick(FPS)


# ================================================================================
# +
# + Test
# +
# ================================================================================

if __name__ == '__main__':
    print("About to Launch GUI")
    main()

    # ============================================================
    # index test
    # ============================================================
    # r = 6
    # c = 8
    # a = np.zeros((r, c))
    # for i in range(r):
    #     for j in range(c):
    #         a[i, j] = (i+1)*100+(j+1)

    # print(a)
    # print('xxx')
    # print(a[:1, :])
    # print('yyy')
    # print(a[1:2, :])

    # a[1:2, :] = a[:1, :]
    # a[0, :] = 0
    # print('zzz')
    # print(a)
    # print(a[-1, :])

    # n = 8
    # np_b = np.zeros((n))
    # for i in range(n):
    #     np_b[i] = i

    # print('np array slice')
    # print(np_b)
    # print(np_b[:-2:])

    # print('list slice')
    # list_b = list(np_b)
    # print(list_b)
    # print(list_b[::-1])

    # ============================================================
    # 2d cords transform plot test
    # ============================================================

    # import matplotlib.pyplot as plt
    # import numpy as np

    # import matplotlib
    # matplotlib.use('TkAgg')

    # a = np.array([[0, 0, 0, 1], [2, 1, 0, 0]])
    # rc = np.array([[0], [1]])

    # fig, ax = plt.subplots()

    # x = a[0, :]
    # y = a[1, :]
    # ax.plot(x, y, linewidth=2.0)

    # p = np.array([[0, -1], [1, 0]])

    # print('------ a')
    # print(a)
    # print('------ repmat')
    # print(np.tile(rc, (1, 4)))

    # # b = rot(a, 90deg)
    # b = np.matmul(p, a - np.tile(rc, (1, 4))) + np.tile(rc, (1, 4))

    # x = b[0, :]
    # y = b[1, :]
    # ax.plot(x, y, linewidth=2.0)

    # # c = rot(b, 90deg)
    # c = np.add(np.matmul(p, np.subtract(b, np.tile(rc, (1, 4)))),
    #            np.tile(rc, (1, 4)))

    # x = c[0, :]
    # y = c[1, :]
    # ax.plot(x, y, linewidth=2.0)

    # #
    # ax.set_xlabel('xxx')
    # ax.set_ylabel('yyy')
    # ax.grid(axis='both')
    # ax.axis('equal')

    # plt.show()

    # ============================================================
