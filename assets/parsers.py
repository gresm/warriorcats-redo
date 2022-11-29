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
    def __init__(self, img: pg.Surface, sprite_tile: tuple[int, int],
                 index_naming: dict[str, tuple[int, int]] | None = None, do_cache: bool = True):
        self.img = img
        self.sprite_tile = sprite_tile
        self.index_naming = index_naming
        self.do_cache = do_cache
        self.cache: dict[tuple[int, int], pg.Surface] = {}

    def get(self, at: str | tuple[int, int]) -> pg.Surface:
        if at in self.index_naming:
            at = self.index_naming[at]
        if at in self.cache:
            return self.cache[at]
        ret = self.img.subsurface(
            at[0] * self.sprite_tile[0], at[1] * self.sprite_tile[1],
            (at[0] + 1) * self.sprite_tile[0], (at[1] + 1) * self.sprite_tile[1]
        )
        if self.do_cache:
            self.cache[at] = ret
        return ret
