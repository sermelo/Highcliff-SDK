# needed to run a local version Highcliff
from highcliff.ai import AI

# needed to run and access the infrastructure needed to communicate and coordinate
from highcliff.infrastructure import LocalNetwork

# the Highcliff action you wish to implement
from highcliff.exampleactions import AuthorizeRoomTemperatureChange

# needed to pretty-print the AI's execution logs
from pprint import pprint

# define the infrastructure that provides the message queue functionality
network = LocalNetwork.instance()


# build functionality by writing custom behavior for your selected actions
class SimulatedUserInterface(AuthorizeRoomTemperatureChange):
    def behavior(self):
        print("Ask Peter if he's okay with raising the temperature in the room")
        print("Peter gave the okay to raise the room's temperature")
        return self.effects


# launch functionality by instantiating the action
SimulatedUserInterface(network)

# start the world with the necessary state
world_update = {"is_room_temperature_comfortable": False, "is_room_temperature_change_authorized": False}
network.update_the_world(world_update)

# run a local version of Highcliff
ai_life_span_in_iterations = 1
goals = {"is_room_temperature_change_authorized": True}
highcliff = AI(network, goals, ai_life_span_in_iterations)

# check the execution logs
print()
pprint(highcliff.diary())
