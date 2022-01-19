# AI, GOAP
from goap.action import Action

# defines action status
from enum import Enum


class AIaction(Action):
    # the effect that the action actually had on the world
    actual_effects = {}

    def __init__(self):
        # an action integrates itself with the communication infrastructure
        self.__integrate()

    def __integrate(self):
        # this is where we will put the code to connect with the (AWS) infrastructure
        # as part of integration, an action registers itself as a capability for charlie
        capabilities.append(self)

    @staticmethod
    def __update_the_world(update):
        # an action handles alerting the network of changes that it made
        # this is where we will put code to publish messages to the (AWS) infrastructure
        the_world_GLOBAL_VARIABLE.update(update)

    def act(self):
        # every AI action runs custom behavior, updates the world, and returns a result
        self.actual_effects = self.behavior()
        self.__update_the_world(self.actual_effects)
        return self.actual_effects

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError


class ActionStatus(Enum):
    SUCCESS = 'success'
    FAIL = 'fail'

