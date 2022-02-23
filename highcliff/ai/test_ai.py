import unittest
from ai import AI, InvalidGoal
from highcliff.infrastructure import LocalNetwork


class TestAI(unittest.TestCase):
    def test_invalid_goals(self):
        # invalid goals should throw an exception

        # create an infrastructure and a known world
        network = LocalNetwork.instance()
        world_updates = {"valid_goal": True}
        network.update_the_world(world_updates)

        # create and pursue an invalid goal
        invalid_goal = {"invalid_goal": True}

        # there should be an error when pursuing an invalid goal
        ai_life_span_in_iterations = 1

        try:
            self.assertRaises(InvalidGoal, AI, network, invalid_goal, ai_life_span_in_iterations)
        except InvalidGoal:
            pass


if __name__ == '__main__':
    unittest.main()
