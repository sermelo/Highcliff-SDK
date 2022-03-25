__author__ = "Jerry Overton"
__copyright__ = "Copyright (C) 2020 appliedAIstudio"
__version__ = "0.1"

# needed to run the ai
from highcliff.ai import AI

# needed to run the ai as a remote service
import rpyc

# needed to start the server in its own thread
from rpyc.utils.server import ThreadedServer

# needed to reference the json ai goal file
import json

# needed to start ai server execution in its own thread
from threading import Thread


class AIServer(rpyc.Service):
    def __init__(self):
        self._ai_instance = AI.instance()

        # get a reference to the centralized infrastructure
        network = self._ai_instance.network()

        # reset the world state
        network.update_the_world({})

        # determine the goals for the AI using the goals file
        with open('ai_goals.json') as json_file:
            ai_goals = json.load(json_file)
        self._ai_instance.set_goals(ai_goals)

        # set the AI to run indefinitely (-1) and asynchronously in its own thread
        ai_execution_thread = Thread(target=self._ai_instance.run, kwargs={'life_span_in_iterations': -1})
        ai_execution_thread.start()

    def on_connect(self, conn):
        pass

    def on_disconnect(self, conn):
        pass

    def exposed_get_ai_instance(self):
        return self._ai_instance


def start_ai_server():
    # TODO: change the port to an environment variable
    thread = ThreadedServer(AIServer, port=18861)
    thread.start()


if __name__ == "__main__":
    start_ai_server()
