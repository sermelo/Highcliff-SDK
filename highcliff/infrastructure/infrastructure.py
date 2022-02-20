from singleton import Singleton


class Infrastructure:
    def __init__(self):
        pass

    def the_world(self):
        raise NotImplementedError

    def update_the_world(self, update):
        raise NotImplementedError

    def capabilities(self):
        raise NotImplementedError

    def add_capability(self, action):
        raise NotImplementedError


@Singleton
class LocalInfrastructure(Infrastructure):
    __the_world = {}
    __capabilities = []

    def the_world(self):
        return self.__the_world

    def update_the_world(self, update):
        self.__the_world.update(update)

    def capabilities(self):
        return self.__capabilities

    def add_capability(self, action):
        self.__capabilities.append(action)
