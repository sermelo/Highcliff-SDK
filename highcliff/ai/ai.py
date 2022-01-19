# copying the state of the world for reflection
import copy
# the goals the ai is to pursue
import goals

from highcliff.actions.actions import ActionStatus

# AI, GOAP
from goap.planner import RegressivePlanner


# these are the things charlie is capable of doing
capabilities = []

# set the current state of the world
# a global variable is used to simulate a central message queue
the_world_GLOBAL_VARIABLE = {}


# this function returns the current state of the world
# here is where we put code to read from the (AWS) infrastructure
def get_world_state():
    return the_world_GLOBAL_VARIABLE


def select_goal(prioritized_goals):
    # the default is to select an empty goal
    selected_goal = {}

    # go through goals in priority order
    for goal in prioritized_goals:
        # find a goal that is not realized in the world
        the_goal_is_not_met = prioritized_goals[goal] != get_world_state()[goal]
        if the_goal_is_not_met:
            # select the first (highest priority) unrealized goal
            selected_goal = {goal: prioritized_goals[goal]}
            break

    return selected_goal


def perceive():
    goal = select_goal(goals)
    world_state_snapshot = copy.copy(get_world_state())
    return goal, world_state_snapshot


def reason(goal, world_state):
    planner = RegressivePlanner(world_state, capabilities)
    plan = planner.find_plan(goal)
    return plan


def act(plan):
    # we are optimistic and assume the plan will succeed
    action_status = ActionStatus.SUCCESS

    # walk through the plan and execute it
    for action in plan:
        action.action.act()
        # compare intended and actual effects, break if the plan is not working
        plan_is_not_working = action.action.effects != action.action.actual_effects
        if plan_is_not_working:
            action_status = ActionStatus.FAIL
            break

    world_state_after = get_world_state()
    return action_status, world_state_after


def reflect(goal, world_state_before, plan, action_status, world_state_after):
    diary_entry = {
        "my_goal": goal,
        "the_world_state_before": world_state_before,
        "my_plan": plan,
        "action_status": action_status,
        "the_world_state_after": world_state_after
    }
    return diary_entry


def run_charlie(diary):
    # low-level brain function: perception
    goal, world_state_before = perceive()

    # middle-level brain function: reasoning and planning
    plan = reason(goal, world_state_before)

    # high-level brain function: action and introspection
    action_status, world_state_after = act(plan)
    diary_entry = reflect(goal, world_state_before, plan, action_status, world_state_after)
    diary.append(diary_entry)
