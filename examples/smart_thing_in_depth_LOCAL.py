# needed to run a local version of the AI
from highcliff.ai import AI

# needed to run and access the infrastructure needed to communicate and coordinate
from highcliff.infrastructure import LocalNetwork

# the Highcliff action you wish to implement
from highcliff.exampleactions import MonitorBodyTemperature, ChangeRoomTemperature, AuthorizeRoomTemperatureChange

# needed to pretty-print the AI's execution logs
from pprint import pprint

# define the infrastructure that provides the message queue functionality
network = LocalNetwork.instance()


class SimulatedSmartThermometer(ChangeRoomTemperature):
    def behavior(self):
        print("Turn up the heat and make the room a bit warmer")
        return self.effects


SimulatedSmartThermometer(network)


class SimulatedUserInterface(AuthorizeRoomTemperatureChange):
    def behavior(self):
        print("Ask Peter if he's okay with raising the temperature in the room")
        print("Peter gave the okay to raise the room's temperature")
        return self.effects


SimulatedUserInterface(network)


class AcmeTemperatureMonitor(MonitorBodyTemperature):
    def behavior(self):
        print("The ACME temperature sensor is active on Peter's wrist")
        print("The ACME temperature sensor is keeping track of Peter's body temperature")
        return self.effects


AcmeTemperatureMonitor(network)

# start the world with the necessary state
world_update = {"is_body_temperature_monitored": False}
network.update_the_world(world_update)

# run a local version of Highcliff
ai_life_span_in_iterations = 2
goals = {"is_room_temperature_comfortable": True}
highcliff = AI(network, goals, ai_life_span_in_iterations)


# check the execution logs
print()
pprint(highcliff.diary())
