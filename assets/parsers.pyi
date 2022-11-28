import pygame as pg
import pygame.freetype


class FontLoader(pg.freetype.Font):
    _name: str
    _is_path: bool
    _font: pygame.freetype.Font


class SpriteSheet:
    ...
