import simulator
from random import choice
from csp import CSP, backtracking_search, forward_checking
from navigate import *

# #################################################
# In case your "State" is different from the one used in the navigate.py, 
#       you may need to modify this function accordingly.
# #################################################
def get_state(state, robot):
    """
    Get current world state from simulator, and use it as initial state
    :param state: a navigate.State()
    :param robot: a simulator.Robot()
    """
    state.pos['me'] = robot.pos
    state.carry = robot.carry
    state.crossed = []
    for d in robot.map.doors:
        state.doors[d] = robot.map.doors[d][2]
    for b in robot.map.boxes.keys():
        state.pos[b] = robot.map.boxes[b]
    print("Initial state updated:")
    pyhop.print_state(state)


def execute(plan, robot):
    print("Executing plan", plan)
    print("Robot's initial location:", robot.pos)
    for act in plan:
        fun = robot.name + '.' + act[0]
        args = '(*act[1:])'
        cmd = fun + args
        if eval(cmd) is not True:
            return False
    print("Robot's final location:", robot.pos)
    return True


def sense_plan_act(robot, state, task, verbose=1):
    """
    Implements the sense-plan-act loop: read the world state, generate a plan, execute it
    :param robot: a robot
    :param state: an initial state, will be filled in by reading the world state from the simulator
    :param task: a task, passed to the HTN planner
    :param verbose: passed to pyhop to control level of verbosity
    :return: True if task completed, False if failed, None if no plan found
    """
    get_state(state, robot)
    plan = pyhop.pyhop(state, task, verbose)
    if plan:
        result = execute(plan, robot)
        if result:
            print("Execution completed!")
        else:
            print("Execution failed!")
        return result
    else:
        print("No plan found!")
    return None


# #################################################
# Task: develop some codes to perform steps 1,2,3 in task-3
#       as explained in the description (solve CSP, re-arrange the 
#       destination of boxes, generate a list of transportation tasks).    
# #################################################



# #################################################
# TASK: modify top_level() to use the generated list of 
#       transportation tasks and to perform step 4 in task-3. 
# #################################################
def top_level(robot, task, verbose=1):
    """
    Top level execution loop: make a robot perform a task
    :param robot: a robot
    :param task: a task in the HTN format
    :param verbose: verbosity level
    :return: True if task successful, or False
    """
    state = State()
    if verbose > 0:
        robot.print()
    if task == ['rearrange']:
        """
        Put here your solution to Task 3 in Lab 5
        """
    else:
        sense_plan_act(robot, state, task, verbose=verbose)
    if verbose > 0:
        robot.map.print()


# #################################################
# Starting point: initialisation of map and robot objects 
# #################################################
my_map = simulator.Map()
my_map.print()

my_rob = simulator.Robot("my_rob", my_map, 'p1')
my_rob.print()


# #################################################
# Test of calling "MODIFIED" top_level function for 'rearrenge' task 
# NOTE: Run and test the following top_level call with at least 
#       one door (e.g., door1) "closed" (change the status of 
#       the doors in class Map in simulator.py, manually.
# #################################################

simulator.DYNAMIC_WORLD = False 
top_level(my_rob, ['rearrange'], verbose=1)

if simulator.USE_GUI:
    input("Enter <return> here to exit")
