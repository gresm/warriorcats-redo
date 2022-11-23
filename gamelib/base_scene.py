from __future__ import annotations

from typing import Type

import pygame as pg

from .window import Window
from .scene_tools import FrameCounter
from .sound_manager import SoundManager


class SceneException(Exception):
    pass


class Scene:
    _instances_cnt: int = -1
    instances: dict[int, Scene] = {}

    _scenes_cnt = -1
    scenes: dict[int, Type[Scene]] = {}

    class_id: int = -1

    manager: SceneManager | None
    frame_counter: FrameCounter

    def __init__(self, scene_manager: SceneManager):
        self.manager = scene_manager
        Scene._instances_cnt += 1
        Scene.instances[self._instances_cnt] = self
        self.instance_id = self.current_instance_id()
        self._events: list[pg.event.Event] = []
        self.frame_counter = FrameCounter(self.manager.game.max_fps)
        self.initialised = False

    def __init_subclass__(cls, **kwargs):
        Scene._scenes_cnt += 1
        Scene.scenes[Scene._scenes_cnt] = cls
        cls.class_id = cls.current_class_id()

    @classmethod
    def current_instance_id(cls):
        return Scene._instances_cnt

    @classmethod
    def current_class_id(cls):
        return Scene._scenes_cnt

    def init(self, **kwargs):
        pass

    def after_init(self):
        pass

    def call_after_init(self):
        if not self.initialised and self.manager.game.running:
            self.after_init()
            self.initialised = True

    def add_event_to_pool(self, event: pg.event.Event):
        self._events.append(event)

    def on_event(self, event: pg.event.Event):
        pass

    def get_events(self):
        for _ in range(len(self._events)):
            yield self._events.pop()

    def draw(self, surface: pg.Surface):
        pass

    def update(self, delta_time: int):
        pass

    def on_redirect(self, scene: Scene):
        pass

    def on_redirect_from(self, scene: Scene):
        pass


class SceneManager:
    game: Window
    global_counter: FrameCounter
    mixer: SoundManager

    def __init__(self):
        self.current: Scene | None = None
        self.initialised = False

    def init_check(self):
        if not self.initialised:
            raise SceneException("SceneManager not initialised")

    def draw(self, surface: pg.Surface):
        self.init_check()
        if self.current is not None:
            self.current.draw(surface)

    def update(self, delta_time: int):
        self.init_check()
        if self.current:
            self.current.update(delta_time)
            self.current.frame_counter.tick(delta_time)

    def set_active_scene(self, scene_id: int | Scene, silent: bool = False):
        if isinstance(scene_id, Scene):
            if self.current:
                self.current.on_redirect(scene_id)
            old = self.current
            self.current = scene_id
            if not silent:
                self.current.on_redirect_from(old)
        elif scene_id in Scene.instances:
            old = self.current
            new = Scene.instances[scene_id]
            if not silent:
                new.on_redirect_from(old)
            if self.current:
                self.current.on_redirect(new)
            self.current = new

        if self.initialised:
            self.current.call_after_init()

    def spawn_scene(self, scene_id: int | Type[Scene], silent: bool = False, **kwargs):
        if isinstance(scene_id, type) and issubclass(scene_id, Scene):
            return self.spawn_scene(scene_id.class_id, **kwargs)
        elif scene_id in Scene.scenes:
            Scene.scenes[scene_id](self)
            self.set_active_scene(Scene.current_instance_id(), silent)
            self.current.init(**kwargs)
            return Scene.current_instance_id()
        else:
            raise SceneException("Scene not found.")

    def spawn_remove_scene(self, scene_id: int | Type[Scene]):
        self.remove_scene(Scene.current_instance_id())
        self.spawn_scene(scene_id)

    def remove_scene(self, scene_id: int | Scene):
        if isinstance(scene_id, Scene):
            scene_id = scene_id.instance_id
        if scene_id in Scene.instances:
            del Scene.instances[scene_id]
            if self.current and scene_id == self.current.instance_id:
                self.current = None

    def handle_events(self, event: pg.event.Event):
        self.current.add_event_to_pool(event)
        self.current.on_event(event)

    def init(self, game: Window, mixer: SoundManager, **kwargs):
        self.game = game
        self.mixer = mixer
        self.game.on_start = self.after_init
        self.global_counter = FrameCounter(self.game.max_fps)
        self.initialised = True

        if self.current:
            self.current.init(**kwargs)

    def after_init(self):
        if self.current:
            self.current.call_after_init()
