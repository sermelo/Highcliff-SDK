# AI, GOAP
from goap.action import Action

# defines action status
from enum import Enum


class AIaction(Action):
    # the effect that the action actually had on the world
    effects = {}

    # these references to global variables should be replaced with a url to central infrastructure
    # TODO: retrofit with the new infrastructure
    __the_world_GLOBAL_VARIABLE = None
    __capabilities_GLOBAL_VARIABLE = None

    def __init__(self, the_world_global_variable, capabilities_global_variable):
        # set the state of the world
        # a global variable is used to simulate a central message queue
        self.__the_world_GLOBAL_VARIABLE = the_world_global_variable

        # set the available capabilities
        # a global variable is used to simulate a central message queue
        self.__capabilities_GLOBAL_VARIABLE = capabilities_global_variable

        # an action integrates itself with the communication infrastructure
        self.__integrate()

    def __integrate(self):
        # this is where we will put the code to connect with the (AWS) infrastructure
        # as part of integration, an action registers itself as a capability for charlie
        self.__capabilities_GLOBAL_VARIABLE.append(self)

    def update_the_world(self, update):
        # an action handles alerting the network of changes that it made
        # this is where we will put code to publish messages to the (AWS) infrastructure
        self.__the_world_GLOBAL_VARIABLE.update(update)

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

