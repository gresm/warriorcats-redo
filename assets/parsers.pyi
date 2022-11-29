from __future__ import annotations
import pygame as pg
import pygame.freetype


class FontLoader(pg.freetype.Font):
    _name: str
    _is_path: bool
    _font: pygame.freetype.Font

    def __init__(self, font: str, is_path: bool = False): ...


class SpriteSheet:
    img: pg.Surface
    sprite_tile: tuple[int, int]
    index_naming: dict[str, tuple[int, int]] | None
    do_cache: bool
    cache: dict[tuple[int, int], pg.Surface]

    def __init__(self, img: pg.Surface, sprite_tile: tuple[int, int],
                 index_naming: dict[str, tuple[int, int]] | None = None, do_cache: bool = True): ...

    def get(self, at: str | tuple[int, int]) -> pg.Surface: ...
