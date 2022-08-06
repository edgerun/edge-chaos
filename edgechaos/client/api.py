import abc

from edgechaos.executor.api import ChaosCommand


class ChaosClient(abc.ABC):

    def send(self, cmd: ChaosCommand): ...

    @staticmethod
    def from_env(): ...
