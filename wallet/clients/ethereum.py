from typing import Optional

from django.conf import settings
from web3 import Web3
from web3.exceptions import InvalidAddress

from .connection import Connection


class EthereumClient(Connection):
    def __init__(self, timeout=10, cache_size=100):
        rpc_url = settings.RPC_URLS['eth']
        super().__init__(rpc_url, timeout, cache_size)
        self.web3: Web3 = Optional[None]
        self._value_unit = "ether"
        self._gas_unit = "gwei"
        self._bt = "ETHEREUM"

    def _create_connection(self):
        """
        Create a new Web3 connection to the Ethereum node.
        """
        self.web3 = Web3(Web3.HTTPProvider(self.rpc_url))
        return self.web3

    def _is_valid_address(self, address):
        return self.web3.is_address(address)

    def get_transactions(self, address, start_block=0, end_block=-1):
        """
        Retrieve transactions for a given address.
        """
        self.connect()
        end_block = self.web3.eth.block_number if end_block == -1 else end_block
        if start_block > end_block:
            raise ValueError("End Block should be greater then Start Block")
        if not self._is_valid_address(address):
            raise InvalidAddress(f"Invalid Address: {address}")
        total_trx = self.web3.eth.get_transaction_count(address)
        transactions = {'transaction_detail': [],
                        'total_transaction': total_trx,
                        'total_block': end_block,
                        'current_balance': f"{self.web3.from_wei(self.web3.eth.get_balance(address), unit=self._value_unit)} ETH",
                        'wallet_address': address
                        }
        for block_num in range(start_block, end_block + 1):
            block = self.web3.eth.get_block(block_num, full_transactions=True)
            for trx in block.get('transactions'):
                if address in [trx.get('from'), trx.get('to')]:
                    tx_details = {
                        "block": block_num,
                        "hash": str(trx.hash.hex()),
                        "from": trx.get('from'),
                        "to": trx.get('to'),
                        "value": f"{trx.get('value')}",
                        "gas": f"{trx.get('gas')}",
                        "gasPrice": f"{trx.get('gasPrice')}",
                        "input": f"{trx.get('input')}",
                    }
                    transactions['transaction_detail'].append(tx_details)

        return transactions
