from __future__ import annotations

import pygame as pg
import pygame.freetype


if not pg.freetype.get_init():
    pg.freetype.init()


class FontLoader:
    def __init__(self, font: str, is_path: bool = False):
        self._name = font
        self._is_path = is_path
        self._font = pygame.freetype.Font(font) if is_path else pg.freetype.SysFont(font, 0)

    def __dir__(self):
        ret = list(super().__dir__())
        ret.extend(self._font.__dir__())
        return ret

    def __getattr__(self, item):
        return getattr(self._font, item)

    def __repr__(self):
        return f"FontLoader({repr(self._name)}, {self._is_path})"

    def __setattr__(self, key, value):
        if key.startswith('__') or key in {"_name", "_is_path", "_font"}:
            super().__setattr__(key, value)
        else:
            setattr(self.font, key, value)


class SpriteSheet:
    pass
