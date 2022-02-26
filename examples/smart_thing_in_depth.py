# needed to run a local version of the AI
from highcliff.ai import AI

# the Highcliff actions to be tested
from highcliff.exampleactions import MonitorBodyTemperature, AuthorizeRoomTemperatureChange, ChangeRoomTemperature

# get a reference to the ai and its network
highcliff = AI.instance()
network = highcliff.network()


# execute a single action with a single goal

class TestBodyTemperatureMonitor(MonitorBodyTemperature):
    def behavior(self):
        print("monitoring body temperature")


TestBodyTemperatureMonitor(network)


class TestAuthorizeRoomTemperatureChange(AuthorizeRoomTemperatureChange):
    def behavior(self):
        print("getting permission to change the room temperature")


TestAuthorizeRoomTemperatureChange(network)


class TestChangeRoomTemperature(ChangeRoomTemperature):
    def behavior(self):
        print("changing the room temperature")


TestChangeRoomTemperature(network)


# define the world state, set goals, and run the ai
network.update_the_world({})
highcliff.set_goals({"is_room_temperature_comfortable": True})
highcliff.run(life_span_in_iterations=3)
