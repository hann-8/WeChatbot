from dataclasses import dataclass
from importlib import metadata


def inspect_dependency():
    try:
        version = metadata.version('wxauto4')
    except metadata.PackageNotFoundError:
        version = None
    return {'dependency_present': version == '41.1.7', 'production_eligible': False}


@dataclass(frozen=True)
class TrialMessage:
    epoch: str
    ui_id: str
    attr: str
    type: str
    sender: str
    content: str


class Wxauto4Client:
    def __init__(self, factory):
        self._client = factory()

    def current_chat(self):
        info = self._client.ChatInfo()
        return info['chat_name'], info['chat_type']

    def snapshot(self, epoch):
        result = []
        for item in self._client.GetAllMessage():
            identity = item.id
            if identity is None or not isinstance(identity, (str, int)) or not str(identity):
                raise ValueError('invalid_ui_id')
            result.append(TrialMessage(epoch, str(identity), item.attr, item.type,
                                       getattr(item, 'sender', ''), getattr(item, 'content', '')))
        return result

    def send_once(self, text):
        return self._client.SendMsg(msg=text)


def live_factory():
    from wxauto4 import WeChat
    return WeChat(debug=False, resize=False)
