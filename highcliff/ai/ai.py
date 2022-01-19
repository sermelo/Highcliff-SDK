# copying the state of the world for reflection
import copy

from highcliff.actions.actions import ActionStatus

# AI, GOAP
from goap.planner import RegressivePlanner


class AI:
    # these are the things the Highcliff AI is capable of doing
    __the_world_GLOBAL_VARIABLE = {}
    __capabilities_GLOBAL_VARIABLE = []
    __goals = {}
    __diary = []

    def __init__(self, the_world_global_variable, capabilities_global_variable, goals, life_span_in_iterations):
        # set the state of the world
        # a global variable is used to simulate a central message queue
        self.__the_world_GLOBAL_VARIABLE = the_world_global_variable

        # set the available capabilities
        # a global variable is used to simulate a central message queue
        self.__capabilities_GLOBAL_VARIABLE = capabilities_global_variable

        self.__goals = goals

        for iteration in range(life_span_in_iterations):
            self.__run_ai()

    def __get_world_state(self):
        # this function returns the current state of the world
        # here is where we put code to read from the (AWS) infrastructure
        return self.__the_world_GLOBAL_VARIABLE

    def __select_goal(self, prioritized_goals):
        # the default is to select an empty goal
        selected_goal = {}

        # go through goals in priority order
        for goal in self.__goals:
            # find a goal that is not realized in the world
            the_goal_is_not_met = self.__goals[goal] != self.__get_world_state()[goal]
            if the_goal_is_not_met:
                # select the first (highest priority) unrealized goal
                selected_goal = {goal: self.__goals[goal]}
                break

        return selected_goal

    def __perceive(self):
        goal = self.__select_goal(self.__goals)
        world_state_snapshot = copy.copy(self.__get_world_state())
        return goal, world_state_snapshot

    def __reason(self, goal, world_state):
        planner = RegressivePlanner(world_state, self.__capabilities_GLOBAL_VARIABLE)
        plan = planner.find_plan(goal)
        return plan

    def __act(self, plan):
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

        world_state_after = self.__get_world_state()
        return action_status, world_state_after

    def __reflect(self, goal, world_state_before, plan, action_status, world_state_after):
        diary_entry = {
            "my_goal": goal,
            "the_world_state_before": world_state_before,
            "my_plan": plan,
            "action_status": action_status,
            "the_world_state_after": world_state_after
        }
        self.__diary.append(diary_entry)

    def __run_ai(self):
        # low-level brain function: perception
        goal, world_state_before = self.__perceive()

        # middle-level brain function: reasoning and planning
        plan = self.__reason(goal, world_state_before)

        # high-level brain function: action and introspection
        action_status, world_state_after = self.__act(plan)
        self.__reflect(goal, world_state_before, plan, action_status, world_state_after)
