from __future__ import annotations

from typing import Optional
import pygame as pg


class AssetError(Exception):
    pass


class Asset:
    """
    Asset object.
    Tree:
        Asset:
            name : string
            children : dict[string, Asset]
            data : AssetData:
                image : Optional[pg.Surface]
                font : Optional[FontLoader]
                sound : Optional[pg.Sound]
                sprite_sheet : Optional[SpriteSheet]
    """

    def __init__(self, name: str, children: dict[str, "Asset"], data: "AssetData"):
        self.name = name
        self.children = children
        self.data = data

    @property
    def image(self):
        return self.data.image

    @image.setter
    def image(self, value: Optional[pg.Surface]):
        self.data.image = value

    @property
    def font(self):
        return self.data.font

    @font.setter
    def font(self, value: Optional[FontLoader]):
        self.data.font = value

    @property
    def sound(self):
        return self.data.sound

    @sound.setter
    def sound(self, value: Optional[pg.Sound]):
        self.data.sound = value

    @property
    def sprite_sheet(self):
        return self.data.sprite_sheet

    @sprite_sheet.setter
    def sprite_sheet(self, value: Optional[SpriteSheet]):
        self.data.sprite_sheet = value

    def add(self, asset: Asset):
        self.children[asset.name] = asset

    def remove(self, asset: Asset | str):
        if isinstance(asset, Asset):
            asset = asset.name
        del self.children[asset]

    def _get(self, name: str):
        if name == "":
            return self
        if name in self.children:
            return self.children[name]
        if name.startswith("$"):
            return self.data
        return None

    def get(self, name: str, __from: Optional[str] = None):
        __from = __from or f"{self.name}.{name}"

        if name == "":
            return self

        vals = name.split(".", 1)
        cur = vals[0]

        ret = self._get(cur)
        if ret is not None:
            if isinstance(ret, AssetData):
                ret = ret.get(name[1:], __from)
            elif len(vals) != 1:
                ret = ret.get(vals[1], __from)

        if ret is None:
            raise AssetError(f"Query \"{cur}\" not found. \"(from {__from})\"")
        return ret


class AssetData:
    """
    AssetData object.
    Tree:
        AssetData:
            image : Optional[pg.Surface]
            font : Optional[FontLoader]
            sound : Optional[pg.Sound]
            sprite_sheet : Optional[SpriteSheet]
    """

    def __init__(
            self, image: Optional[pg.Surface] = None, font: Optional[FontLoader] = None,
            sound: Optional[pg.Sound] = None, sprite_sheet: Optional[SpriteSheet] = None
    ):
        self.image = image
        self.font = font
        self.sound = sound
        self.sprite_sheet = sprite_sheet

    def _get(self, name: str):
        if name == "":
            return self
        if name == "image":
            return self.image
        if name == "font":
            return self.font
        if name == "sound":
            return self.sound
        if name in {"sprite_sheet", "sprite", "sheet"}:
            return self.sprite_sheet
        return None

    def get(self, name: str, __from: Optional[str] = None) -> AssetData | pg.Surface | FontLoader | SpriteSheet:
        __from = __from or name
        ret = self._get(name)
        if ret is None:
            raise AssetError(f"Property \"{name}\" not found. (from \"{__from}\")")
        return ret


class FontLoader:
    pass


class SpriteSheet:
    pass
