import unittest

import highcliff.infrastructure.test_infrastructure as test_infrastructure
import highcliff.actions.test_actions as test_actions
import highcliff.ai.test_ai as test_ai
import highcliff.exampleactions.test_exampleactions as test_example_actions


# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_infrastructure))
suite.addTests(loader.loadTestsFromModule(test_actions))
suite.addTests(loader.loadTestsFromModule(test_ai))
suite.addTests(loader.loadTestsFromModule(test_example_actions))

# initialize runner, pass runner the suite, run the tests
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
