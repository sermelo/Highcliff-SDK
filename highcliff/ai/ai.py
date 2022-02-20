# copying the state of the world for reflection
import copy

from highcliff.actions.actions import ActionStatus

# AI, GOAP
from goap.planner import RegressivePlanner


class AI:
    # these are the things the Highcliff AI is capable of doing
    __the_world_GLOBAL_VARIABLE = None
    __capabilities_GLOBAL_VARIABLE = None
    __goals = None
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
        # select a single goal from the list of goals
        goal = self.__select_goal(self.__goals)

        # create a plan to achieve the selected goal
        planner = RegressivePlanner(self.__get_world_state(), self.__capabilities_GLOBAL_VARIABLE)

        # start by assuming that there is no plan, the action will have no effect and will fail
        plan = None
        effect_of_actions = {}
        action_status = ActionStatus.FAIL

        # take a snapshot of the current world state before taking action that may change it
        world_state_snapshot = copy.copy(self.__get_world_state())

        try:
            # make a plan
            plan = planner.find_plan(goal)
            next_action = plan[0].action

            # execute the first act in the plan. the act will affect the world and get us one step closer to the goal
            # the plan will be updated and actions executed until the goal is reached
            next_action.act()

            # the action is a success if the altered world matches the action's intended effect
            action_had_intended_effect = next_action.effects.items() <= self.__get_world_state().items()
            if action_had_intended_effect:
                action_status = ActionStatus.SUCCESS

        except:
            # no viable plan found. no action to be taken
            pass

        # record the results of this iteration
        self.__reflect(goal, world_state_snapshot, plan, action_status, self.__get_world_state())

    def diary(self):
        return self.__diary
