from abc import ABCMeta, abstractmethod


class Strategy(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def handle_tick(self, tick):
        raise NotImplementedError("Method not implemented")
