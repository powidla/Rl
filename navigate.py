import pyhop
import map

class State(pyhop.State):
    def __init__(self):
        self.__name__ = "s1"
        self.pos = {}           # positions of robot and boxes
        self.doors = {}         # doors' status: closed or open
        self.carry = None       # what boxes the robot is carrying
        self.crossed = []       # list of doors tried so far during planning
        self.visited = []       # list of positions tried so far during planning


def some(predicate, candidates):
    for x in candidates:
        if predicate(x):
            return x
    return False


###############################################################################
# OPERATORS
# First argument is current state, others are the operator's parameters.
###############################################################################

def moveto(state, p):
    state.pos['me'] = p
    return state


def cross(state, d, p):
    state.crossed.append(d)
    state.pos['me'] = p
    return state


pyhop.declare_operators(moveto, cross)


# #################################################
# METHODS
# First argument is current state, others are the method's parameters.
# They may call other methods, or executable operators.
# #################################################

# Methods to move inside a room

def move_in_room_same_point(state, p):
    if state.pos['me'] == p:
        return []
    else:
        return False


def move_in_room_another_point(state, p):
    if map.room_of(state.pos['me']) == map.room_of(p):
        return [('moveto', p)]
    else:
        return False


pyhop.declare_methods('move_in_room', move_in_room_same_point, move_in_room_another_point)


# Methods to cross a door

def cross_door_to_p2(state, d):
    p1, p2 = map.doors[d]
    if state.doors[d] == 'open' and state.pos['me'] == p1:
        return [('cross', d, p2)]
    return False


def cross_door_to_p1(state, d):
    p1, p2 = map.doors[d]
    if state.doors[d] == 'open' and state.pos['me'] == p2:
        return [('cross', d, p1)]
    return False


pyhop.declare_methods('cross_door', cross_door_to_p2, cross_door_to_p1)


# Top level navigation methods

def navigate1(state, p):
    if p == state.pos['me']:
        return []
    else:
        return False


def navigate2(state, p):
    if map.room_of(p) == map.room_of(state.pos['me']):
        return [('move_in_room', p)]
    else:
        return False


def navigate3(state, p):
    r = map.room_of(state.pos['me'])
    d = some(lambda x: x not in state.crossed, map.doors_of(r))
    if d:
        state.crossed.append(d)
        p2 = map.side_of(d, r)
        return [('move_in_room', p2), ('cross_door', d), ('navigate_to', p)]
    else:
        return False


def navigate4(state, p):
    if p not in state.visited:
        state.visited.append(p)
        return [('navigate_to', p)]
    else:
        return False


pyhop.declare_methods('navigate_to', navigate1, navigate2, navigate3, navigate4)
