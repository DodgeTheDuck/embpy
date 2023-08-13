
from copy import deepcopy
from typing import TypeVar
import imgui
from asset.asset import Asset


T = TypeVar("T")
__assets = list[Asset]()


def add_asset(asset: Asset) -> Asset:
    __assets.append(asset)
    return asset


def get_asset(name: str) -> Asset:
    for asset in __assets:
        if name == asset.name:
            return asset
    return None


def instantiate_asset(name: str) -> Asset:
    for asset in __assets:
        if name == asset.name:
            return deepcopy(asset)
    return None


def draw_gui() -> None:
    imgui.begin("Asset Manager")
    for asset in __assets:
        if imgui.collapsing_header(asset.name)[0]:
            asset.draw_gui()
    imgui.end()
