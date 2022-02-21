from __future__ import absolute_import, division, print_function
import copy, random
from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1 

# Tree node. To be used to construct a game tree. 
class Node: 
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        self.state = (copy.deepcopy(state[0]), state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        return len(self.children) == 0

# AI agent. To be used do determine a promising next move.
class AI:
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3):
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    # recursive function to build a game tree
    def build_tree(self, node=None, depth=0, ec=False):
        if node == None:
            node = self.root
        if depth == self.search_depth: 
            return 

        if node.player_type == MAX_PLAYER:
            present_state = copy.deepcopy(node.state)
            self.simulator.reset(copy.deepcopy(present_state[0]), present_state[1])
            for i in MOVES.keys():
                movement = self.simulator.move(i)
                if(movement):
                    if ec == False:
                        child = Node(copy.deepcopy(self.simulator.get_state()), CHANCE_PLAYER)
                        node.children.append((i,child))
                    else:
                        #print("xxxxxxxx")
                        # I want the tile to be on the edge:
                        m = copy.deepcopy(self.simulator.get_state())[0] # tile matrix
                        s = copy.deepcopy(self.simulator.get_state())[1] # score
                        # For the left and right column
                        for a in range(0, len(m)):
                            for b in [len(m[a])-1, 0]:
                                tile = m[a][b]
                                if tile>1024: s = s + 0.6*tile
                                else: s = s + 0.76*tile
                        # For the up and down row
                        for a in [len(m)-1, 0]:
                            for b in range(0, len(m[a])):
                                if tile>1024: s = s + 0.6*tile
                                else: s = s + 0.76*tile
                        child = Node((copy.deepcopy(self.simulator.get_state())[0], s), CHANCE_PLAYER)
                        node.children.append((i,child))
                self.simulator.reset(copy.deepcopy(present_state[0]), present_state[1])


        elif node.player_type == CHANCE_PLAYER:
            present_state = copy.deepcopy(node.state)
            self.simulator.reset(copy.deepcopy(present_state[0]), present_state[1])
            for tile in self.simulator.get_open_tiles():
                target_state = copy.deepcopy(present_state)
                target_state[0][tile[0]][tile[1]] = 2
                child = Node(copy.deepcopy(target_state), MAX_PLAYER)
                node.children.append((None, child))
                self.simulator.reset(copy.deepcopy(present_state[0]), present_state[1])

        # TODO: build a tree for each child of this node
        for c in node.children:
            self.build_tree(c[1],depth+1,ec=ec)
        

    # expectimax implementation; 
    # returns a (best direction, best value) tuple if node is a MAX_PLAYER
    # and a (None, expected best value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node = None):
        # TODO: delete this random choice but make sure the return type of the function is the same
        #return random.randint(0, 3), 0

        if node == None:
            node = self.root

        if node.is_terminal():
            # TODO: base case
            return None, node.state[1]

        elif node.player_type == MAX_PLAYER:
            # TODO: MAX_PLAYER logic
            result = -float('inf')
            direct = 0
            for d, c in node.children:
                c = self.expectimax(c)[1]
                if c>result:
                    result = c
                    direct = d
            return (direct, result)

        elif node.player_type == CHANCE_PLAYER:
            # TODO: CHANCE_PLAYER logic
            result = 0
            chance = 1/len(node.children)
            for _,c in node.children:
                result += self.expectimax(c)[1]*chance
            return (None, result)
            

    # Do not modify this function
    def compute_decision(self):
        self.build_tree()
        d, _ = self.expectimax(self.root)
        return d

    # Implement expectimax with customized evaluation function here
    def compute_decision_ec(self):
        self.build_tree(ec=True)
        d,_ = self.expectimax(self.root)
        return d
