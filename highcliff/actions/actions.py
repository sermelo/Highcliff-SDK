# AI, GOAP
from goap.action import Action

# defines action status
from enum import Enum


class AIaction(Action):

    # ai that calls the action when needed
    __ai = None

    def __init__(self, ai):
        # set a reference to the artificial intelligence
        self.__ai = ai

        # an action integrates itself with the communication infrastructure
        self.__integrate()

        # the effect that the action actually had on the world
        self.effects = {}

    def __integrate(self):
        # as part of integration, an action registers itself as a capability for highcliff
        self.__ai.add_capability(self)

    def update_the_world(self, update):
        # update the world state of highcliff
        self.__ai.network().update_the_world(update)

    def act(self):
        # every AI action runs custom behavior, updates the world, and returns a result
        self.behavior()
        self.update_the_world(self.effects)

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError


class ActionStatus(Enum):
    SUCCESS = 'success'
    FAIL = 'fail'

