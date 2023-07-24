import json
from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()

PAYMASTER_ADDRESS = os.getenv("PAYMASTER_CONTRACT_ADDRESS")


def get_ethereum_client() -> Web3:
    url = os.getenv("CHAIN_RPC")

    if not url:
        raise NotImplementedError("Missing CHAIN_RPC environment variable")

    client = Web3(Web3.HTTPProvider(url))
    return client


def get_paymaster_contract():
    client = get_ethereum_client()
    with open("app/abi/paymaster_abi.json") as json_file:
        contract_abi = json.load(json_file)
        contract = client.eth.contract(PAYMASTER_ADDRESS, abi=contract_abi)
        return contract
