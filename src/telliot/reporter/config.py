from telliot.utils.config import ConfigOptions


class ReporterConfig(ConfigOptions):
    private_key: str
    node_url: str
    contract_address: str
    provider: str
    network: str
    chain_id: int
    gasprice_speed: str
