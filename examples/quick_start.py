# needed to run a local version Highcliff
from highcliff.ai import AI

# the Highcliff action you wish to implement
from highcliff.exampleactions import AuthorizeRoomTemperatureChange

# define the state of the world and the ai capabilities.
# when running a local version of Highcliff, use global variables to simulate underlying infrastructure
# these global variables will be replaced with urls in the production version
the_world_GLOBAL_VARIABLE = {"is_room_temperature_change_authorized": False, "is_room_temperature_comfortable": False}
capabilities_GLOBAL_VARIABLE = []


# build functionality by writing custom behavior for your selected actions
class SimulatedUserInterface(AuthorizeRoomTemperatureChange):
    def behavior(self):
        print("Ask Peter if he's okay with raising the temperature in the room")
        print("Peter gave the okay to raise the room's temperature")
        return self.effects


# launch functionality by instantiating the action
SimulatedUserInterface(the_world_GLOBAL_VARIABLE, capabilities_GLOBAL_VARIABLE)


# run a local version of Highcliff
ai_life_span_in_iterations = 1
goals = {"is_room_temperature_change_authorized": True}
AI(the_world_GLOBAL_VARIABLE, capabilities_GLOBAL_VARIABLE, goals, ai_life_span_in_iterations)
