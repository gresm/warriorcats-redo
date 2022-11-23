from __future__ import annotations

from typing import Callable, Optional
from abc import ABCMeta, abstractmethod

import pygame as pg


class DisplayError(Exception):
    pass


class AbstractDisplay(metaclass=ABCMeta):
    """
    Abstract class for display objects.
    """

    def __init__(self, fps: int, screen_size: tuple[int, int], flags: int = 0, **kwargs):
        self.max_fps = fps
        self.flags = flags
        self.clock = pg.time.Clock()
        self.running = False
        self._frame: Callable[[pg.Surface, int], ...] | None = None
        self.on_start: Optional[Callable, None] = None
        self.size = screen_size
        self.initialized = False
        self.extra_kwargs = kwargs

    def frame(self, func: Callable[[pg.Surface, int], ...]):
        self._frame = func
        return func

    @property
    @abstractmethod
    def screen(self) -> pg.Surface:
        pass

    @abstractmethod
    def init(self):
        self.initialized = True

    @abstractmethod
    def quit(self):
        pass

    def stop(self):
        self.running = False

    def run(self):
        if not self.initialized:
            raise DisplayError("Display is not initialized")
        if self._frame is None:
            raise DisplayError("Frame function not bind to display")
        if self.on_start is not None:
            self.on_start()

        self.running = True

        while self.running:
            if max_fps != -1:
                ms = self.clock.tick(max_fps)
            else:
                ms = self.clock.tick()
            self._frame(self.screen, ms)  # maybe you are missing "window" and "delta_time" arguments


class Window(AbstractDisplay):
    _screen: pg.Surface = None

    def init(self):
        pg.display.init()
        self._screen = pg.display.set_mode(self.size, self.flags)
        super().init()

    def quit(self):
        pg.display.quit()

    @property
    def screen(self):
        return self._screen


size = (800, 800)
max_fps = 60
game = None


def get_game(game_size: tuple[int, int] | None = None, fps: int | None = None, flags: int = 0):
    global game
    ret = Window(fps or max_fps, game_size or size, flags)
    game = ret
    return ret


__all__ = [
    "size",
    "max_fps",
    "get_game",
    "game",
    "Window"
]
