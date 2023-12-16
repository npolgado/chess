import random
import copy
import math
# Agent that plays chess

class AI :

    

    def __init__(self, game, col):
        self.game = game    # game object to get information about the game
        self.color = col    # color the ai is playing (0 white, 1 black)

        # poss moves is an array of tuples: (piece, valid moves of that piece)
        return random.choice(poss_moves)

    def get_move(self) -> tuple:
        # create tree and set root value to current mat diff
        self.tree = Tree(self.game.get_mat_diff())

        # layer 1
        self.tree.add_children(self.tree.root, self.game)

        # layer 2
        for ch in self.tree.root.children:
            p_game = copy.deepcopy(self.game)    # get the board corresponding to the root
            # then follow the 'path' to get to the board state of the new node being added
            for i in range (len(ch.path)):
                p_game.move(ch.path[i][0], ch.path[i][1])
                p_game.new_turn()

            self.tree.add_children(ch, p_game)
        # layer 3

        # minimax
        for i in range(1, -1, -1):
            layer_arr = self.tree.get_nodes_at_layer(i)
            n = (i + self.color) % 2
            nud = None
            for el in layer_arr:
                if n == 0:  # maximize
                    nud = None
                    for ch in el.children:
                        if nud is None:
                            nud = [ch]
                        else:
                            if ch.value > nud[0].value:
                                nud = [ch]
                            elif ch.value == nud[0].value:
                                nud.append(ch)

                elif n == 1:  # minimize
                    nud = None
                    for ch in el.children:
                        if nud is None:
                            nud = [ch]
                        else:
                            if ch.value < nud[0].value:
                                nud = [ch]
                            elif ch.value == nud[0].value:
                                nud.append(ch)
                if nud is None:
                    print ("par=", el.value, el.path)
                else:
                    el.value = nud[0].value

        # self.tree.print_tree()
        # for a in nud:
        #     print (a.value, end=", ")
        # print()
        return random.choice(nud).path[0]

class Tree:
    def __init__(self, v):
        self.root = self.Node(v)
        self.depth = 0

    def print_tree (self):
        print (self.__print_tree_helper__(self.root))

    def __print_tree_helper__(self, n, level=0):
        s = "\t"*level + str(n.value) + "  " + str(n.path) + "\n"
        for c in n.children:
            s += self.__print_tree_helper__(c, level+1)
        return s

    def print_all_leaves(self):
        self.__print_leaf_helper__(self.root)

    def __print_leaf_helper__(self, n):
        if n.children is []:
            print(n.value, n.path)
        else:
            for ch in n.children:
                self.__print_leaf_helper__(ch)

    def get_nodes_at_layer(self, d):
        a = [self.root]
        while d > 0:
            b = []
            for el in a:
                for ch in el.children:
                    b.append(ch)
            a = b

            d -= 1

        return a

    def add_children(self, parent, cur_game):
        # copy current game state, to follow different lines
        pseudo_game = copy.deepcopy(cur_game)

        # poss_moves <- get all valid moves
        pieces = pseudo_game.get_teams_pieces(pseudo_game.turn)
        poss_moves = []
        for i in range(len(pieces)):
            p = pieces[i]
            val_moves = pseudo_game.get_valid_moves(p)
            for i in range(len(val_moves)):
                poss_moves.append((pseudo_game.__get_r_c_from_piece__(p), val_moves[i]))

        # for each possible move, record the material difference of each position
        for i in range (len(poss_moves)):
            pseudo_game = copy.deepcopy(cur_game)
            a = poss_moves[i]
            pseudo_game.move(a[0], a[1])
            pseudo_game.new_turn()

            # evaluation of position (currently just material difference)
            dif = pseudo_game.get_mat_diff()
            st = pseudo_game.get_state()
            trn = pseudo_game.turn
            if st == 1 or st == 2:
                if trn==0:
                    l = -1
                elif trn==1:
                    l = 1
                n = self.Node(l*1000, parent, a)
            else:
                n = self.Node(dif, parent, a)
            parent.children.append(n)

    class Node:
        def __init__(self, val, par=None, last_move=None):
            self.value = val

            # parents path plus last move
            if par is None:     # root
                self.parent = None
                self.path = []
            else:
                self.parent = par
                self.path = copy.deepcopy(self.parent.path)
                self.path.append(last_move)
            self.children = []

        def __str__(self):
            return str(self.value)
