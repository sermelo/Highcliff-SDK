import unittest

# needed to test local infrastructure
from infrastructure import LocalInfrastructure


class TestInfrastructure(unittest.TestCase):
    def test_local_infrastructure_reset(self):
        # TODO: implement this

        local_infrastructure = LocalInfrastructure.instance()

        # add state to the world and check that the world is not empty
        dummy_state = {'dummy_state': True}
        local_infrastructure.update_the_world(dummy_state)
        world_is_not_empty = len(local_infrastructure.the_world()) > 0
        self.assertTrue(world_is_not_empty)

        # add capabilities and check that capabilities are not empty
        dummy_action = "dummy action"
        local_infrastructure.add_capability(dummy_action)
        capabilities_are_not_empty = len(local_infrastructure.capabilities()) > 0
        self.assertTrue(capabilities_are_not_empty)

        # reset the infrastructure
        local_infrastructure.reset()

        # check that the world state has been reset
        reset_world = {}
        self.assertEqual(reset_world, local_infrastructure.the_world())

        # check that the capabilities have been reset
        reset_capabilities = []
        self.assertEqual(reset_capabilities, local_infrastructure.capabilities())

        pass

    def test_local_infrastructure(self):

        # create two instances of local infrastructures
        first_local_infrastructure = LocalInfrastructure.instance()
        second_local_infrastructure = LocalInfrastructure.instance()

        # the infrastructure instances should be the same
        self.assertTrue(first_local_infrastructure is second_local_infrastructure)

        # the world in both infrastructures should initially be empty
        expected_world = {}
        self.assertEqual(expected_world, first_local_infrastructure.the_world())
        self.assertEqual(expected_world, second_local_infrastructure.the_world())

        # update the world in the first infrastructure and check for the same update in the second infrastructure
        world_update = {'world_updated': True}
        first_local_infrastructure.update_the_world(world_update)
        self.assertEqual(world_update, first_local_infrastructure.the_world())
        self.assertEqual(world_update, second_local_infrastructure.the_world())

        # the capabilities in both infrastructures should initially be empty
        expected_capabilities = []
        self.assertEqual(expected_capabilities, first_local_infrastructure.capabilities())
        self.assertEqual(expected_capabilities, second_local_infrastructure.capabilities())

        # update the capabilities in the first infrastructure and check for the same update in the second infrastructure
        action = "dummy action"
        first_local_infrastructure.add_capability(action)
        self.assertEqual(action, first_local_infrastructure.capabilities()[0])
        self.assertEqual(action, second_local_infrastructure.capabilities()[0])


if __name__ == '__main__':
    unittest.main()
