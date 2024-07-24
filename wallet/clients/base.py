from .ethereum import EthereumClient


class Client:
    @staticmethod
    def get(address) -> EthereumClient:
        """
        Get the appropriate blockchain client based on the given address.
        """
        if address.startswith('0x'):  # Example check for Ethereum address
            return EthereumClient()
        else:
            raise ValueError("Unsupported blockchain technology for address")
