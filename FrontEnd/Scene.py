from abc import ABC, abstractmethod


class Scene(ABC):

    @abstractmethod
    def on_update(self, surface, window_scale):
        pass
