import unittest
from highcliff.exampleactions import MonitorBodyTemperature, AuthorizeRoomTemperatureChange, ChangeRoomTemperature
from highcliff.ai import AI, intent_is_real


class MyTestCase(unittest.TestCase):
    def setUp(self):
        # get a reference to the ai and its network
        self.highcliff = AI.instance()
        self.network = self.highcliff.network()

    def tearDown(self):
        # reset the ai
        self.highcliff.reset()

    def test_end_to_end_scenario(self):
        # test that the ai can create a two-step plan to execute multiple actions to reach a goal

        class TestBodyTemperatureMonitor(MonitorBodyTemperature):
            def behavior(self):
                pass

        TestBodyTemperatureMonitor(self.highcliff)

        class TestAuthorizeRoomTemperatureChange(AuthorizeRoomTemperatureChange):
            def behavior(self):
                pass

        TestAuthorizeRoomTemperatureChange(self.highcliff)

        class TestChangeRoomTemperature(ChangeRoomTemperature):
            def behavior(self):
                pass

        TestChangeRoomTemperature(self.highcliff)

        # define the test world state and goals
        self.network.update_the_world({})
        self.highcliff.set_goals({"is_room_temperature_comfortable": True})

        # run a local version of Highcliff
        self.highcliff.run(life_span_in_iterations=3)

        # the plan should have started with two steps, then progress to a single step
        self.assertEqual(3, len(self.highcliff.diary()[0]['my_plan']))
        self.assertEqual(2, len(self.highcliff.diary()[1]['my_plan']))
        self.assertEqual(1, len(self.highcliff.diary()[2]['my_plan']))

        # in the third iteration, the ai should have reached it's goal
        highcliff_reached_its_goal = intent_is_real({"is_room_temperature_comfortable": True},
                                                    self.highcliff.diary()[2]['the_world_state_after'])
        self.assertTrue(highcliff_reached_its_goal)


if __name__ == '__main__':
    unittest.main()
