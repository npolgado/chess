import pygame, os
import math
import numpy as np
import eric_AI as eai
import nick_AI as nai


FILE_DIR = os.path.dirname(__file__)

#game constants
IM_BLACK = 'images/Black/'
IM_WHITE = 'images/White/'

IM_QUEEN = 'Queen.png'
IM_KING = 'King.png'
IM_ROOK = 'Rook.png'
IM_BISHOP = 'Bishop.png'
IM_PAWN = 'Pawn.png'

NUM_BLOCKS = 30
SQ_SZ = 25

GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

BLUEGREEN = (71,255,207)
LIGHTBROWN = 200, 200, 150
DARKBROWN = 155, 158, 71

CURSOR = 224, 158, 52

PREVMOVES = 255, 216, 99    # TODO: draw last move loc1 + loc2

LIGHTBROWN_shaded = 150, 150, 75
DARKBROWN_shaded = 125, 121, 56
BLUEGREEN_shaded = (60, 174, 144)
shd = 32
BLACK_shaded = (shd, shd, shd)

PIECES = {
    0: 'Empty',    1: 'Pawn',
    2: 'Bishop',    3: 'Knight',
    5: 'Rook',    6: 'King',
    9: 'Queen'
}
#TODO:  be consistent with team, turn, side (maybe differentiate a pieces side and the current turn)
class Game:
    def __init__(self):

        self.turn = 0   # White Starts

        self.state = -1 # -1: not started, 0: normal game state, 1: check, 2: stalemate, 3: checkmate

        # load pieces array and add them to pieces_arr (for easy access with turn variable)
        self.white_pieces = []
        self.black_pieces = []

        self.board = []

        self.pieces_arr = []

        # load board w/ pieces in pieces arrays for each team
        self.__generate_team_pieces_and_set_starting_board__()

        # a = self.board
        # for i in range (len(a)):
        #     for j in range (len(a[0])):
        #         print (a[i][j], "/", (i, j))

        # column for en passant in respective rows
        self.en_passant_2 = -1
        self.en_passant_5 = -1

        self.material_difference = 0

        self.prev_moves = None      # use this when drawing the board to illuminate the last move made

        self.valids = None
        self.pts = 0

    def __generate_team_pieces_and_set_starting_board__(self):
        self.white_pieces.append(Piece(5, 0))
        self.white_pieces.append(Piece(3, 0))
        self.white_pieces.append(Piece(2, 0))
        self.white_pieces.append(Piece(9, 0))
        self.white_pieces.append(Piece(6, 0))
        self.white_pieces.append(Piece(2, 0))
        self.white_pieces.append(Piece(3, 0))
        self.white_pieces.append(Piece(5, 0))

        self.black_pieces.append(Piece(5, 1))
        self.black_pieces.append(Piece(3, 1))
        self.black_pieces.append(Piece(2, 1))
        self.black_pieces.append(Piece(9, 1))
        self.black_pieces.append(Piece(6, 1))
        self.black_pieces.append(Piece(2, 1))
        self.black_pieces.append(Piece(3, 1))
        self.black_pieces.append(Piece(5, 1))

        for i in range(8):
            self.white_pieces.append(Piece(1, 0))
            self.black_pieces.append(Piece(1, 1))

        self.board.append(self.black_pieces[0:8])
        self.board.append(self.black_pieces[8:])
        self.board.append([Piece(0)] * 8)
        self.board.append([Piece(0)] * 8)
        self.board.append([Piece(0)] * 8)
        self.board.append([Piece(0)] * 8)

        self.board.append(self.white_pieces[8:])
        self.board.append(self.white_pieces[0:8])

        self.pieces_arr = [self.white_pieces, self.black_pieces]  # can be access with self.pieces_arr[turn]

        # put king at beginning
        for i in range (2):
            temp = self.pieces_arr[i][4]
            self.pieces_arr[i][4] = self.pieces_arr[i][0]
            self.pieces_arr[i][0] = temp

    # TODO: get rid of this function
    def __get_r_c_from_piece__(self, piece, arr=None):
        a = self.board
        if arr is not None:
            a = arr

        for i in range (8):
            for j in range (8):
                # print (a[i][j], "...", piece)
                # print ("   ", a[i][j].type == piece.type)
                if a[i][j] == piece:
                    return (i, j)

        return False

    def get_teams_pieces(self, team):
        return self.pieces_arr[team]

    def new_turn (self):
        self.turn = 1 - self.turn
        if self.turn == 0:
            self.en_passant_5 = -1
        else:
            self.en_passant_2 = -1

        self.state, self.material_difference = self.__get_game_state_and_points__()

    def move(self, loc1, loc2):
        # loc1: location to move toward
        # loc2: what is moved
        r1 = loc1[0]
        c1 = loc1[1]

        r2 = loc2[0]
        c2 = loc2[1]

        p = self.board[r1][c1]

        # skip to main logic in most cases (marked HERE)

        # castling logic  (overwrites move)
        if p.type == 'Rook':
            p.moved = True
        if p.type == 'King':
            p.moved = True
            # short castle!
            dist = c2 - c1
            if dist >= 2:
                self.board[r1][6] = self.board[r1][4]
                self.board[r1][4] = Piece(0)    # king done
                self.board[r1][5] = self.board[r1][7]
                self.board[r1][7] = Piece(0)
                return
            # long castle!
            if dist <= -2:
                self.board[r1][2] = self.board[r1][4]
                self.board[r1][4] = Piece(0)    # king
                self.board[r1][3] = self.board[r1][0]
                self.board[r1][0] = Piece(0)
                return

        # HERE
        # main logic of function
        removed_piece = self.board[r2][c2]
        self.board[r2][c2] = p
        self.board[r1][c1] = Piece(0)

        if removed_piece.type != 'Empty':
            # print ("removing", removed_piece)
            self.pieces_arr[removed_piece.side].remove(removed_piece)

        self.prev_moves = (loc1, loc2)      # Delete this if possible and use all_moves list

        if p.type == 'Pawn':
            # en passant logic
            dist = r1 - r2
            if abs(dist) == 2:
                if self.turn == 0:
                    self.en_passant_5 = c1
                else:
                    self.en_passant_2 = c1

            if (r2, c2) == (2, self.en_passant_2):
                removed_piece = self.board[r2 + 1][c2]
                self.board[r2 + 1][c2] = Piece(0)
                self.pieces_arr[removed_piece.side].remove(removed_piece)
            if (r1, c1) == (5, self.en_passant_5):
                removed_piece = self.board[r2 - 1][c2]
                self.board[r2 - 1][c2] = Piece(0)
                self.pieces_arr[removed_piece.side].remove(removed_piece)

            # Queening Logic
            if self.turn == 0 and r2 == 0:
                self.pieces_arr[0].append(Piece(9, 0))
                self.pieces_arr[0].remove(self.board[r2][c2])
                self.board[r2][c2] = self.pieces_arr[0][-1]
            if self.turn == 1 and r2 == 7:
                self.pieces_arr[1].append(Piece(9, 1))
                self.pieces_arr[1].remove(self.board[r2][c2])
                self.board[r2][c2] = self.pieces_arr[1][-1]

    def get_valid_moves(self, piece, arr=None):
        my_arr = self.board
        if arr is not None:
            my_arr = arr

        a = self.__get_r_c_from_piece__(piece)
        (r, c) = a

        moves = []

        # PAWN
        if piece.type == 'Pawn':
            # WHITE
            if piece.side == 0:
                # diagonal attacks
                if (r - 1 >= 0) and (c - 1 >= 0):
                    if my_arr[r - 1][c - 1].id != 0:
                        if my_arr[r - 1][c - 1].side != piece.side:
                            if self.is_king_safe((r, c), (r - 1, c - 1)):
                                moves.append((r - 1, c - 1))
                    if r - 1 == 2:  # en passant
                        if c - 1 == self.en_passant_2:
                            if self.is_king_safe((r, c), (r - 1, c - 1)):
                                moves.append((r - 1, c - 1))
                if (r - 1 >= 0) and (c + 1 < 8):
                    if my_arr[r - 1][c + 1].id != 0:
                        if my_arr[r - 1][c + 1].side != piece.side:
                            if self.is_king_safe((r, c), (r - 1, c + 1)):
                                moves.append((r - 1, c + 1))
                    if r - 1 == 2:  # en passant
                        if c + 1 == self.en_passant_2:
                            if self.is_king_safe((r, c), (r - 1, c + 1)):
                                moves.append((r - 1, c + 1))
                # forward
                if r - 1 >= 0:
                    if my_arr[r - 1][c].id == 0:
                        if self.is_king_safe((r, c), (r - 1, c)):
                            moves.append((r - 1, c))
                        if r == 6:
                            if my_arr[r - 2][c].id == 0:
                                if self.is_king_safe((r, c), (r - 2, c)):
                                    moves.append((r - 2, c))

            # BLACK
            if piece.side == 1:
                # diagonal attacks
                if (r + 1 < 8) and (c - 1 >= 0):
                    if my_arr[r + 1][c - 1].id != 0:
                        if my_arr[r + 1][c - 1].side != piece.side:
                            if self.is_king_safe((r, c), (r + 1, c - 1)):
                                moves.append((r + 1, c - 1))
                    if r + 1 == 5:  # en passant
                        if c - 1 == self.en_passant_5:
                            if self.is_king_safe((r, c), (r + 1, c - 1)):
                                moves.append((r + 1, c - 1))
                if (r + 1 < 8) and (c + 1 < 8):
                    if my_arr[r + 1][c + 1].id != 0:
                        if my_arr[r + 1][c + 1].side != piece.side:
                            if self.is_king_safe((r, c), (r + 1, c + 1)):
                                moves.append((r + 1, c + 1))
                    if r + 1 == 5:  # en passant
                        if c + 1 == self.en_passant_5:
                            if self.is_king_safe((r, c), (r + 1, c + 1)):
                                moves.append((r + 1, c + 1))

                # forward
                if r + 1 < 8:
                    if my_arr[r + 1][c].id == 0:
                        if self.is_king_safe((r, c), (r + 1, c)):
                            moves.append((r + 1, c))
                        if r == 1:
                            if my_arr[r + 2][c].id == 0:
                                if self.is_king_safe((r, c), (r + 2, c)):
                                    moves.append((r + 2, c))

        # KNIGHT
        if piece.type == 'Knight':
            a = [-2, -2, -1, -1, 1, 1, 2, 2]  # r vectors
            b = [-1, 1, -2, 2, -2, 2, -1, 1]  # c vectors
            for i in range(0, len(a)):
                if (r + a[i] < 8 and r + a[i] >= 0):
                    if (c + b[i] < 8 and c + b[i] >= 0):
                        # a piece is here
                        # if not same team, add as valid move
                        if my_arr[r + a[i]][c + b[i]].side != piece.side:
                            if self.is_king_safe((r, c), (r + a[i], c + b[i])):
                                moves.append((r + a[i], c + b[i]))

        # BISHOP
        if piece.type == 'Bishop':
            v1 = (-1, -1)  # top-left
            v2 = (-1, 1)  # top-right
            v3 = (1, 1)  # bot-right
            v4 = (1, -1)  # bot-left
            vectors = [v1, v2, v3, v4]

            for i in range(0, 4):
                locX = r
                locY = c
                while True:
                    v = vectors[i]
                    locX += v[0]
                    locY += v[1]
                    if locX > 7 or locX < 0 or locY > 7 or locY < 0:
                        break
                    if my_arr[locX][locY].id == 0:
                        if self.is_king_safe((r, c), (locX, locY)):
                            moves.append((locX, locY))

                    else:
                        # a piece is here
                        # if not same team, add as valid move
                        if my_arr[locX][locY].side != piece.side:
                            if self.is_king_safe((r, c), (locX, locY)):
                                moves.append((locX, locY))
                        break

        # ROOK
        if piece.type == 'Rook':
            v1 = (-1, 0)  # top
            v2 = (0, 1)  # right
            v3 = (0, -1)  # bot
            v4 = (1, 0)  # left
            vectors = [v1, v2, v3, v4]

            for i in range(0, 4):
                locX = r
                locY = c
                while True:
                    v = vectors[i]
                    locX += v[0]
                    locY += v[1]
                    if locX > 7 or locX < 0 or locY > 7 or locY < 0:
                        break
                    if my_arr[locX][locY].id == 0:
                        if self.is_king_safe((r, c), (locX, locY)):
                            moves.append((locX, locY))

                    else:
                        # a piece is here
                        # if not same team, add as valid move
                        if my_arr[locX][locY].side != piece.side:
                            if self.is_king_safe((r, c), (locX, locY)):
                                moves.append((locX, locY))
                        break

        # QUEEN
        if piece.type == 'Queen':
            v1 = (-1, 0)  # top
            v2 = (0, 1)  # right
            v3 = (0, -1)  # bot
            v4 = (1, 0)  # left
            v5 = (-1, -1)  # top-left
            v6 = (-1, 1)  # top-right
            v7 = (1, 1)  # bot-right
            v8 = (1, -1)  # bot-left
            vectors = [v1, v2, v3, v4, v5, v6, v7, v8]

            for i in range(0, 8):
                locX = r
                locY = c
                while True:
                    v = vectors[i]
                    locX += v[0]
                    locY += v[1]
                    if locX > 7 or locX < 0 or locY > 7 or locY < 0:
                        break
                    if my_arr[locX][locY].id == 0:
                        if self.is_king_safe((r, c), (locX, locY)):
                            moves.append((locX, locY))
                    else:
                        # a piece is here
                        # if not same team, add as valid move
                        if my_arr[locX][locY].side != piece.side:
                            if self.is_king_safe((r, c), (locX, locY)):
                                moves.append((locX, locY))
                        break

        if piece.type == "King":
            a = [-1, 0, 1, -1, 1, -1, 0, 1]  # r vectors
            b = [-1, -1, -1, 0, 0, 1, 1, 1]  # c vectors
            for i in range(0, len(a)):
                if 0 <= r + a[i] < 8:
                    if 0 <= c + b[i] < 8:
                        # a piece is here
                        # if not same team, add as valid move
                        if my_arr[r + a[i]][c + b[i]].side != piece.side:
                            if self.is_king_safe((r, c), (r + a[i], c + b[i])):
                                moves.append((r + a[i], c + b[i]))

            # castling rules: kings and rooks have extra variable, moved, which is False only when the piece hasn't moved
            if not piece.moved:  # king hasnt moved
                if self.is_king_safe():     # king can't castle in check
                    # Short Castle
                    if my_arr[r][c + 1].id == 0 and self.is_king_safe((r, c), (r, c+1)):        # space and king safe (1)
                        if my_arr[r][c + 2].id == 0 and self.is_king_safe((r, c), (r, c+2)):    # space and king safe (2)
                            rCornerPiece = my_arr[r][c + 3]
                            if rCornerPiece.type == 'Rook':
                                if not rCornerPiece.moved:
                                    moves.append((r, c + 2))
                                    moves.append((r, c + 3))

                    # Long Castle
                    if my_arr[r][c - 1].id == 0 and self.is_king_safe((r, c), (r, c-1)):        # space and king safe (1)
                        if my_arr[r][c - 2].id == 0 and self.is_king_safe((r, c), (r, c-2)):    # space and king safe (2)
                            if my_arr[r][c-3].id == 0 and self.is_king_safe((r, c), (r, c-3)):  # space and king safe (3)
                                rCornerPiece = my_arr[r][c - 4]
                                if rCornerPiece.type == 'Rook':
                                    if not rCornerPiece.moved:
                                        moves.append((r, c - 2))
                                        moves.append((r, c - 3))
                                        moves.append((r, c - 4))
                                        # can click all 3 locations to castle

        '''Given a piece and location (er: rook (4, 5), return a list of valid moves'''
        return moves

    def print_board(self, alt_arr = None):
        a = self.board
        if alt_arr != None:
            a = alt_arr

        print("-----")
        for i in range(8):
            for j in range(8):
                print("", a[i][j].id, end=" ")
            print()

    def draw_board(self, valid_moves=None, clicked=None):  # , locs=None):
        global screen
        pygame.font.init()

        a = 8

        # Draw each tile. If there is a piece, draw it too
        for i in range(a):
            for j in range(a):
                len = (side / a)
                valid_color = DARKBROWN
                valid_color_shaded = DARKBROWN_shaded
                if (i + j) % 2 == 0:  # if a lightsquare
                    valid_color = LIGHTBROWN
                    # valid_color_shaded = LIGHTBROWN_shaded        # different color when shaded (valid moves)

                # last moves (2 xy) highlighted orange
                if self.prev_moves is not None and (j, i) in self.prev_moves:
                    pygame.draw.rect(screen, CURSOR, (i * len, j * len, len, len))

                # unit we clicked
                elif clicked is not None and (j, i) == clicked:
                    pygame.draw.rect(screen, CURSOR, (i * len, j * len, len, len))
                else:
                    pygame.draw.rect(screen, valid_color, (i * len, j * len, len, len))

                # valid color
                if valid_moves is not None and (j, i) in valid_moves:
                    pygame.draw.circle(screen, valid_color_shaded,
                                       (int(i * len) + int(len / 2), int(j * len) + int(len / 2)), int(len / 2 * 3 / 4))

                myfont = pygame.font.SysFont('Comic Sans MS', 50)
                ele = self.board[j][i]
                if ele.side != -1:
                    image = pygame.image.load(ele.im_path)
                    r = image.get_rect().size
                    screen.blit(image, (int (i*len + len/2 - r[0]/2), int (j*len + len/2 - r[1]/2)))

        pygame.display.update()

    def get_state(self):
        return self.state

    def get_mat_diff(self):
        return self.material_difference

    def __get_game_state_and_points__(self):
        #   Returns State, Points
        # States:
        #   0 : nothing special
        #   1 : checkmate on board (for other turn)
        #   2 : stalemate
        #   3 : check
        if_valids, pts = self.__get_if_valid_moves_and_points_diff__()

        check = not self.is_king_safe()
        if if_valids:   # if there are any valid moves for current team
            if check:
                return 3, pts
            return 0, pts

        if check:
            return 1, pts
        else:
            return 2, pts

    def __get_if_valid_moves_and_points_diff__(self):
        any_valids = False
        white_points = 0
        w_pieces = self.pieces_arr[0]

        for i in range (len(w_pieces)):
            p = w_pieces[i]

            # Check valid moves
            if self.turn == 0 and not any_valids:
                if self.get_valid_moves(p) != []:
                    any_valids = True

            white_points += p.get_points()

        black_points = 0
        b_pieces = self.pieces_arr[1]
        for i in range (len(b_pieces)):
            p = b_pieces[i]
            # Check valid moves
            if self.turn == 1 and not any_valids:
                if self.get_valid_moves(p) != []:
                    any_valids = True

            black_points += p.get_points()

        w_b_diff = white_points-black_points

        self.material_difference = w_b_diff

        return any_valids, w_b_diff

    def is_king_safe(self, loc1=None, loc2=None):
        # return if King is safe in current position.
        # loc1/2:  move loc1 -> loc2  before checking (optional used for checking if a potential valid move is valid)

        pseudo_board = [row[:] for row in self.board]  # use a fake version of the board for potential moves
        if loc1 is not None and loc2 is not None:
            r1 = loc1[0]
            c1 = loc1[1]
            r2 = loc2[0]
            c2 = loc2[1]
            pseudo_board[r2][c2] = pseudo_board[r1][c1]
            pseudo_board[r1][c1] = Piece(0)

        # pseudo board represents the board state (after a potential valid move has been made or not)
        k = self.get_king_location(pseudo_board)
        rk = k[0]
        ck = k[1]
        # king = pseudo_board[rk][ck]

        # King <- KNIGHT?
        a = [-2, -2, -1, -1, 1, 1, 2, 2]  # r vectors
        b = [-1, 1, -2, 2, -2, 2, -1, 1]  # c vectors
        for i in range(0, len(a)):
            r_pos = rk + a[i]
            c_pos = ck + b[i]
            if 0 <= r_pos < 8:
                if 0 <= c_pos < 8:
                    if pseudo_board[r_pos][c_pos].side != self.turn and pseudo_board[r_pos][c_pos].type == 'Knight':
                        return False

        # King <- BISHOP/ QUEEN?
        v1 = (-1, -1)  # top-left
        v2 = (-1, 1)  # top-right
        v3 = (1, 1)  # bot-right
        v4 = (1, -1)  # bot-left
        vectors = [v1, v2, v3, v4]
        for i in range(0, 4):
            locX = rk
            locY = ck
            while True:
                v = vectors[i]
                locX += v[0]
                locY += v[1]
                if locX > 7 or locX < 0 or locY > 7 or locY < 0:
                    break

                p = pseudo_board[locX][locY]
                if p.id != 0:
                    if p.side == self.turn:  # friendly piece
                        break
                    else:  # enemy piece
                        if p.type == 'Bishop' or p.type == 'Queen':
                            return False
                        break

        # King <- ROOK/ QUEEN?
        v1 = (-1, 0)  # top
        v2 = (0, 1)  # right
        v3 = (0, -1)  # bot
        v4 = (1, 0)  # left
        vectors = [v1, v2, v3, v4]

        for i in range(0, 4):
            locX = rk
            locY = ck
            while True:
                v = vectors[i]
                locX += v[0]
                locY += v[1]
                if locX > 7 or locX < 0 or locY > 7 or locY < 0:
                    break

                p = pseudo_board[locX][locY]
                if p.id != 0:
                    if p.side == self.turn:  # friendly piece
                        break
                    else:  # enemy piece
                        if p.type == 'Rook' or p.type == 'Queen':
                            return False
                        break

        # King <- PAWN?
        n = 1  # pawns can attack (row) in negative direction for white, positive for black
        if self.turn == 0:
            n = -1

        if 0 <= rk + n < 8:
            if 0 <= ck - 1 < 8:
                p = pseudo_board[rk + n][ck - 1]
                if p.side != self.turn and p.type == 'Pawn':
                    return False
            if 0 <= ck + 1 < 8:
                p = pseudo_board[rk + n][ck + 1]
                if p.side != self.turn and p.type == 'Pawn':
                    return False
        return True

    def get_king_location(self, arr=None):
        a = self.__get_r_c_from_piece__(self.pieces_arr[self.turn][0], arr)  # if arr is None, it uses self.board
        return a

class Piece:
    '''
    Side = True means WHITE, False means BLACK
    Num = ID of piece, based on PIECES global
    Im_path = string path to image, based on type
    '''
    def __init__(self, num, side=-1):
        self.side = side    # 0-->WHITE, 1-->BLACK (Bool)
        self.id = num       # ID/KEY of PIECES global (Int)
        self.type = PIECES[self.id]     # from enum, use type number (String)

        if self.type == 'Empty':
            return

        elif self.type == 'Pawn':
            self.points = 1

        elif self.type == 'Bishop' or self.type == 'Knight':
            self.points = 3

        elif self.type == 'Queen':
            self.points = 9

        elif self.type == 'Rook':
            self.points = 5
            self.moved = False  # bool to determine if castling is possible

        elif self.type == 'King':
            self.points = 1000
            self.moved = False  # bool to determine if castling is possible

        else:
            print("uhh..? type=", self.type)
            self.moved = None

        s = "images/"
        if self.side == 0:
            s += 'White/'
        else:
            s += 'Black/'
        s += str(self.type)
        s += '.png'
        self.im_path = os.path.join(FILE_DIR, s)    # string path to piece image (String)

    def __str__(self):
        s = ""
        s += str(self.type)
        s += " "
        s += str(self.side)
        return s

    def get_points(self):
        return self.points


def init():
    global screen
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption('Chess')
    screen.fill(WHITE)

    pygame.display.flip()

def is_3_repititions(): # TODO
    return False

def is_insufficient_material(): # TODO
    return False

if __name__ == '__main__':

    GAME = Game()
    
    chess_ai = eai.AI(GAME, 1)
    chess_ai2 = eai.AI(GAME, 0)

    # game state globals (not constant)

    side = SQ_SZ * NUM_BLOCKS
    size = (side, side)

    init()
    GAME.draw_board()
    running = True

    valids = []

    clicked = False

    first_click_loc = None

    while running:
        if GAME.turn == 0:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 3:   #   right click
                        clicked = False
                        GAME.draw_board()
                        break
                    pos = pygame.mouse.get_pos()
                    c = int(pos[0] / (side/8))
                    r = int(pos[1] / (side/8))

                    # SECOND Click
                    if clicked:
                        if (r, c) in valids:
                            GAME.move(first_click_loc, (r,c))

                            clicked = False

                            GAME.new_turn()

                            GAME.draw_board()

                            st = GAME.get_state()
                            if st != 0:
                                print ("State:", st)
                            if st == 1:  # checkmate
                                running = False
                                break
                            elif st == 2:    # stalemate
                                running = False
                                break
                            break
                        else:
                            clicked = False
                            GAME.draw_board()
                            if GAME.board[r][c].id == 0:
                                break

                    # FIRST CLICK
                    p = GAME.board[r][c]
                    piece = p.type

                    if p.side != GAME.turn:
                        break
                    if piece == 'Empty':
                        break

                    first_click_loc = (r, c)

                    valids = GAME.get_valid_moves (p)
                    GAME.draw_board(valids, (r, c))

                    clicked = True

                if event.type == pygame.QUIT:
                    running = False

        if GAME.turn == 0:
            a = chess_ai2.get_move()
            GAME.move(a[0], a[1])
            GAME.new_turn()
            GAME.draw_board()
        else:
            a = chess_ai.get_move()
            # print("a=", a)
            GAME.move(a[0], a[1])
            GAME.new_turn()
            GAME.draw_board()

print ("GAME OVER WITH STATE", GAME.get_state())

pygame.time.wait(30000)

if GAME.state == 1:
    print ("CHECKMATE")

if GAME.state == 2:
    print ("STALEMATE")

pygame.time.wait(3000)