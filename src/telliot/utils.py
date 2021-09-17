from web3 import Web3

class TelliotUtils:

    def to_bytes32(self, request_id:str) -> bytes:
        """Convert request_id to bytes32

        Returns:
            Byte representation of value
        """
        return Web3.toBytes(input)


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
    print(TelliotUtils.to_bytes("really long string:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaqaaaaaaaaaaaa"))