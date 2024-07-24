# views.py
from django.conf import settings
from rest_framework.request import Request
from rest_framework.views import APIView
from web3 import Web3

from WalletWatcher.utils import send_response, ResponseStatus
from .clients.base import Client


# Test Transaction will be deprecated on prod
class DummyTransaction(APIView):
    def post(self, request: Request, *args, **kwargs):
        from_address = request.data.get('from_address')
        from_pk = request.data.get('from_pk')
        to_address = request.data.get('to_address')
        amount_ether = request.data.get('amount_ether')

        web3 = Web3(Web3.HTTPProvider(settings.RPC_URLS['eth']))
        amount_in_wei = Web3.to_wei(amount_ether, 'ether')
        nonce = web3.eth.get_transaction_count(from_address)
        transaction = {
            'to': to_address,
            'value': amount_in_wei,
            'gas': 21000,
            'gasPrice': web3.to_wei('50', 'gwei'),
            'nonce': nonce,
            'chainId': 1337  # Ganache chain ID
        }
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key=from_pk)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        trx = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(trx)
        tx_details = {
            "block": trx.get("block_num"),
            "transaction_hash": str(trx.get('transactionHash').hex()),
            "from": trx.get('from'),
            "to": trx.get('to'),
            "value": f"{trx.get('value')}",
            "gas": f"{trx.get('gas')}",
            "gasPrice": f"{trx.get('gasPrice')}",
            "input": f"{trx.get('input')}",
        }
        return send_response(data=tx_details, status=ResponseStatus.SUCCESS, message="Dummy Transaction was successful")


class WalletTransactionsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        print(request)
        address = request.query_params.get('address')
        client = Client.get(address)
        transactions = client.get_transactions(address)
        return send_response(data=transactions, status=ResponseStatus.SUCCESS,
                             message="Transaction Fetched Successfully")
