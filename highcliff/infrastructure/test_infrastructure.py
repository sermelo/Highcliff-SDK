import unittest

# needed to test local infrastructure
from infrastructure import LocalInfrastructure


class TestInfrastructure(unittest.TestCase):
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
