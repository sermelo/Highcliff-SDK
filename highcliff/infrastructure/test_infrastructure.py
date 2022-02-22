import unittest

# needed to test local infrastructure
from network import LocalNetwork


class TestInfrastructure(unittest.TestCase):
    def test_local_infrastructure_reset(self):

        local_network = LocalNetwork.instance()

        # add state to the world and check that the world is not empty
        dummy_state = {'dummy_state': True}
        local_network.update_the_world(dummy_state)
        world_is_not_empty = len(local_network.the_world()) > 0
        self.assertTrue(world_is_not_empty)

        # add capabilities and check that capabilities are not empty
        dummy_action = "dummy action"
        local_network.add_capability(dummy_action)
        capabilities_are_not_empty = len(local_network.capabilities()) > 0
        self.assertTrue(capabilities_are_not_empty)

        # add a topic and check that the topics are not empty
        dummy_topic = "dummy_topic"
        local_network.create_topic(dummy_topic)
        topics_are_not_empty = len(local_network.topics()) > 0
        self.assertTrue(topics_are_not_empty)

        # reset the network infrastructure
        local_network.reset()

        # check that the world state has been reset
        reset_world = {}
        self.assertEqual(reset_world, local_network.the_world())

        # check that the capabilities have been reset
        reset_capabilities = []
        self.assertEqual(reset_capabilities, local_network.capabilities())

        # check that the topics have been reset
        reset_topics = []
        self.assertEqual(reset_capabilities, local_network.topics())

    def test_local_infrastructure(self):
        # TODO: update this to include checking basic pub/sub mechanisms

        # create two instances of local networks
        first_local_network = LocalNetwork.instance()
        second_local_network = LocalNetwork.instance()

        # the network instances should be the same
        self.assertTrue(first_local_network is second_local_network)

        # the world in both networks should initially be empty
        expected_world = {}
        self.assertEqual(expected_world, first_local_network.the_world())
        self.assertEqual(expected_world, second_local_network.the_world())

        # update the world in the first network and check for the same update in the second network
        world_update = {'world_updated': True}
        first_local_network.update_the_world(world_update)
        self.assertEqual(world_update, first_local_network.the_world())
        self.assertEqual(world_update, second_local_network.the_world())

        # the capabilities in both networks should initially be empty
        expected_capabilities = []
        self.assertEqual(expected_capabilities, first_local_network.capabilities())
        self.assertEqual(expected_capabilities, second_local_network.capabilities())

        # update the capabilities in the first network and check for the same update in the second network
        action = "dummy action"
        first_local_network.add_capability(action)
        self.assertEqual(action, first_local_network.capabilities()[0])
        self.assertEqual(action, second_local_network.capabilities()[0])


if __name__ == '__main__':
    unittest.main()
