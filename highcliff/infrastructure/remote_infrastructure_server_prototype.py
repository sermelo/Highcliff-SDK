import rpyc


class RemoteAI(rpyc.Service):
    def on_connect(self, conn):
        pass

    def on_disconnect(self, conn):
        pass

    def exposed_get_ai(self):
        return "foobar"


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    thread = ThreadedServer(RemoteAI, port=18861)
    thread.start()
