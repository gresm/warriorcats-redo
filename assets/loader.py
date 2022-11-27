from __future__ import annotations
from pathlib import Path
import pygame as pg


try:
    from .asset import Asset, AssetData
except ImportError:
    from asset import Asset, AssetData
