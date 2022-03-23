__author__ = "Jerry Overton"
__copyright__ = "Copyright (C) 2020 appliedAIstudio"
__version__ = "0.1"

# needed to run the ai
from highcliff.ai import AI

# needed to run the ai as a remote service
import rpyc

# needed to start the server in its own thread
from rpyc.utils.server import ThreadedServer


class AIServer(rpyc.Service):
    _ai_instance = AI.instance()

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
