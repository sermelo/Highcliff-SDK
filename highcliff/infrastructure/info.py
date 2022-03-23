from collections import namedtuple
Message = namedtuple('Message', 'event_type event_tags event_source timestamp device_info application_info user_info environment context effects data')

class Info():
    def __init__(self, topic, **message_entries): #event_type, event_tags, event_source, timestamp, device_info, application_info, user_info, environment, context, effects, data):
        self.topic = topic
        try:
            self.message = Message(**message_entries)
        except TypeError:
            raise TypeError(
                'Missing arguments while creating Info object. '
                f'Expected {Message._fields}. but received {list(message_entries.keys())}'
            ) from None

    def __str__(self):
        return str(self.get_summary)

    @property
    def id(self):
        return self.message.event_source

    def get_summary(self):
        raise NotImplemented

    @property
    def location(self):
        if self.message.event_tags and 'location' in self.message.event_tags:
            return self.message.event_tags['location']
        return None

class DeviceData(Info):
    def get_summary(self):
        return {self.id: {
            'topic': self.topic,
            'time': self.message.timestamp,
            'event_type': self.message.event_type,
            'location': self.location,
            'data': self.message.data,
        }}


class Effect(Info):
    @property
    def id(self):
        return self.message.effects

    def get_summary(self):
        return {self.id: self.message.data}

