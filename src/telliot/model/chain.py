from telliot.utils.base import Base
from telliot.apps.config import ConfigOptions
from telliot.apps.config import ConfigFile
from typing import List, Optional
from pydantic import Field


class EVMCurrency(Base):
    name: str
    symbol: str
    decimals: int


class Chain(Base):
    name: str
    chain: str
    network: str
    chain_id: int
    currency: EVMCurrency


default_chain_list = [
    Chain(chain_id=1,
          name='Ethereum Mainnet',
          chain='ETH',
          network='mainnet',
          currency=EVMCurrency(name='Ether',
                               symbol='ETH',
                               decimals=18)
          ),

    Chain(chain_id=3,
          name='Ethereum Testnet Ropsten',
          chain='ETH',
          network='ropsten',
          currency=EVMCurrency(name='Ropsten Ether',
                               symbol='ROP',
                               decimals=18)
          ),

    Chain(chain_id=4,
          name='Ethereum Testnet Rinkeby',
          chain='ETH',
          network='rinkeby',
          currency=EVMCurrency(name='Rinkeby Ether',
                               symbol='RIN',
                               decimals=18)
          ),

    Chain(chain_id=137,
          name='Matic(Polygon) Mainnet',
          chain='Matic(Polygon)',
          network='mainnet',
          currency=EVMCurrency(name='Matic',
                               symbol='MATIC',
                               decimals=18)
          ),

    Chain(chain_id=137,
          name='Matic(Polygon) Testnet Mumbai',
          chain='Matic(Polygon)',
          network='testnet',
          currency=EVMCurrency(name='Matic',
                               symbol='tMATIC',
                               decimals=18)
          ),

]


class ChainList(ConfigOptions):
    chains: List[Chain] = Field(default=default_chain_list)

    def get_chain(self, chain: str = 'ETH', network: str = 'rinkeby') -> Optional[Chain]:

        for ch in self.chains:
            if ch.chain == chain:
                if ch.network == network:
                    return ch

        return None
