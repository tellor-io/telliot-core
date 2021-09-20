from web3 import Web3

class TelliotUtils:

    def to_bytes32(self, request_id:str) -> bytes:
        """Convert request_id to bytes32

        Returns:
            Byte representation of value
        """
        # hex = Web3.toHex(text=request_id)
        # print(len(hex))
        # return Web3.toBytes(hexstr=hex)
        b = bytes(request_id, "ascii")
        print(len(b))
        return b

        raise NotImplementedError

    def to_bytes(self, input):

        pass

    def from_bytes(self, bytesval: bytes) -> str:
        """Convert blockchain bytes to value

        Returns:
            Value
        """

        return Web3.toText(bytesval)

        raise NotImplementedError


if __name__ == "__main__":
    #test really long string...does it clip?
    print(TelliotUtils().to_bytes32("PolygonBridge,mesosphereContract,bytes4(keccack(balanceOf(address)),randomAddress,blockNumber"))