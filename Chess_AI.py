import random
import copy
import math
# Agent that plays chess
class AI :
    def __init__(self, game, col):
        self.game = game    # game object to get information about the game
        self.color = col    # color the ai is playing (0 white, 1 black)


    def get_move_random(self):
        pieces = self.game.get_teams_pieces(self.color)
        poss_moves = []
        for i in range (len(pieces)):
            p = pieces[i]
            val_moves = self.game.get_valid_moves(p)
            for i in range (len(val_moves)):
                poss_moves.append((p, val_moves[i]))

        # print ("(", len(poss_moves), end =")")
        # for i in range (len(poss_moves)):
        #     print (poss_moves[i][0].type, "/", poss_moves[i][1], end = ". ")
        # print ()

        # poss moves is an array of tuples: (piece, valid moves of that piece)
        return random.choice(poss_moves)

    def get_move(self):

        # create tree and set root value to current mat diff
        self.tree = Tree(self.game.get_mat_diff())

        # layer 1
        self.tree.add_children(self.tree.root, self.game)

        # self.tree.print_tree()

        # layer 2
        for ch in self.tree.root.children:
            p_game = copy.deepcopy(self.game)    # get the board corresponding to the root
            # then follow the 'path' to get to the board state of the new node being added
            for i in range (len(ch.path)):
                p_game.move(ch.path[i][0], ch.path[i][1])
                p_game.new_turn()
            self.tree.add_children(ch, p_game)

        self.tree.print_tree()
        self.tree.print_all_leaves()

        # find minimum value'd node (replace with minimax once more depth is added)
        l = self.tree.root.children
        min_ind = 0
        min_node = l[0]
        node_inds = [min_ind]
        for i in range(len(l)):
            n = l[i]
            if n.value < min_node.value:
                min_node = n
                min_ind = i
                node_inds = [i]

            elif n.value == min_node.value:
                node_inds.append(i)

        ind = random.choice(node_inds)

        return self.tree.root.children[ind].path[0]

        # above is working, but how can we do it for depth d.
        # after getting an entire layer, call this on each child


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
        if n.children == []:
            print(n.value, n.path)
        else:
            for ch in n.children:
                self.__print_leaf_helper__(ch)

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

            # evaluation of position (currently just material difference)
            dif = pseudo_game.__get_game_state_and_points__()
            diff = dif[1]
            # pseudo_game.print_board()
            # print ("   dif =", diff)
            n = self.Node(diff, parent, a)
            parent.children.append(n)

    class Node:
        def __init__(self, val, par=None, last_move=None):
            self.value = val

            # parents path plus last move
            if par is None: # root
                self.parent = None
                self.path = []
            else:
                self.parent = par
                self.path = copy.deepcopy(self.parent.path)
                self.path.append(last_move)
            self.children = []

        def __str__(self):
            return str(self.value)
