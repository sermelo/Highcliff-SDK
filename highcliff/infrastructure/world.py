from .info import Effect, Info

class World():
    def __init__(self):
        self.information = {}

    def __str__(self):
        return str(self.get_all_info())

    def update(self, topic, message):
        try:
            info = None
            if 'effects' not in message:
                print(f'Unable to proccess message from topic {topic}: {message}')
            elif message['effects'] is None:
                info = DeviceData(topic, **message)
            else:
                info = Effect(topic, **message)
            if info is not None:
                self.information[info.id] = info
        except TypeError:
            print(f'Unable to proccess message from topic {topic}: {message}')

    def get_all_info(self):
        world = {}
        for info_id, info in self.information.items():
            world.update(info.get_summary())
        return world

    def get_current_effects(self):
        effects = []
        for _, info in self.information.items():
            if info.effects is not None:
                effects.extend(info.effects)
        return effects
