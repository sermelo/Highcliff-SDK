# needed to run a local version of the AI
from highcliff.ai import AI

# the Highcliff action you wish to implement
from highcliff.exampleactions import MonitorBodyTemperature, ChangeRoomTemperature, AuthorizeRoomTemperatureChange, \
    AlertCareProvider, LogBodyTemperatureData

# needed to pretty-print the AI's execution logs
from pprint import pprint

# define the state of the world and the ai capabilities.
# when running a local version of Highcliff, use global variables to simulate underlying infrastructure
# these global variables will be replaced with urls in the production version
the_world_GLOBAL_VARIABLE = {"is_body_temperature_monitored": False, "is_room_temperature_comfortable": False}
capabilities_GLOBAL_VARIABLE = []


# build functionality by writing custom behavior for your selected actions
class SimulatedMessagingApp(AlertCareProvider):
    def behavior(self):
        print("Tell Francis that the room temperature will be raised because Peter is cold")
        return self.effects


SimulatedMessagingApp(the_world_GLOBAL_VARIABLE, capabilities_GLOBAL_VARIABLE)


class SimulatedSmartThermometer(ChangeRoomTemperature):
    def behavior(self):
        print("Turn up the heat and make the room a bit warmer")
        return self.effects


SimulatedSmartThermometer(the_world_GLOBAL_VARIABLE, capabilities_GLOBAL_VARIABLE)


class SimulatedUserInterface(AuthorizeRoomTemperatureChange):
    def behavior(self):
        print("Ask Peter if he's okay with raising the temperature in the room")
        print("Peter gave the okay to raise the room's temperature")
        return self.effects


SimulatedUserInterface(the_world_GLOBAL_VARIABLE, capabilities_GLOBAL_VARIABLE)


class SimulatedDataLogger(LogBodyTemperatureData):
    def behavior(self):
        print("In the data lake, make a place to store the history of Peter's body temperature")
        return self.effects


SimulatedDataLogger(the_world_GLOBAL_VARIABLE, capabilities_GLOBAL_VARIABLE)


class AcmeTemperatureMonitor(MonitorBodyTemperature):
    def behavior(self):
        print("The ACME temperature sensor is active on Peter's wrist")
        print("The ACME temperature sensor is keeping track of Peter's body temperature")
        return self.effects


AcmeTemperatureMonitor(the_world_GLOBAL_VARIABLE, capabilities_GLOBAL_VARIABLE)


# run a local version of Highcliff
ai_life_span_in_iterations = 2
goals = {"is_room_temperature_comfortable": True}
highcliff = AI(the_world_GLOBAL_VARIABLE, capabilities_GLOBAL_VARIABLE, goals, ai_life_span_in_iterations)


# check the execution logs
print()
pprint(highcliff.diary())
