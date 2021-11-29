import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict
from typing import Optional

from clamfig import deserialize

from telliot_core.model.base import Base
from telliot_core.model.tokens import BlockChainAsset
from telliot_core.utils.home import TELLIOT_CORE_ROOT


@dataclass
class AssetRegistry(Base):
    assets: Dict[str, BlockChainAsset]

    def register(self, asset: BlockChainAsset) -> None:
        if asset.id in self.assets:
            raise ValueError(f"Asset {asset.id} already registered")
        self.assets[asset.id] = asset

    @classmethod
    def from_file(cls, filepath: Path) -> "AssetRegistry":

        with open(filepath) as f:
            state = json.load(f)

        asset_list = deserialize(state)

        obj = cls(assets={})

        for asset in asset_list:
            obj.register(asset)

        return obj

    def get(self, asset_id: str) -> Optional[BlockChainAsset]:

        return self.assets.get(asset_id)


asset_registry = AssetRegistry.from_file(TELLIOT_CORE_ROOT / "data/assets.json")
