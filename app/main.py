import uvicorn
from fastapi import FastAPI, Request, Response
from jsonrpcserver import Result, Success, dispatch, method

from eth_account.messages import defunct_hash_message
from hexbytes import HexBytes

from web3 import Web3

from dotenv import load_dotenv
import os

from app.utils.ethereum_client import (
    get_paymaster_contract,
    get_ethereum_client,
)

app = FastAPI()
load_dotenv()


@method
def pm_sponsorUserOperation(request, entryPoint, pmData) -> Result:
    # Defaults
    paymaster = get_paymaster_contract()
    w3 = get_ethereum_client()

    # Prepare the data
    valid_until = w3.eth.get_block("latest").timestamp + 180  # Valid Until
    valid_after = w3.eth.get_block("latest").timestamp  # Valid After

    paymaster_data = [
        paymaster.address,
        valid_until,
        valid_after,
        os.getenv("SPONSOR_ADDRESS"),
        b"",
    ]

    paymaster_and_data = (
        str(paymaster_data[0])
        + str("{0:0{1}x}".format(paymaster_data[1], 64))
        + str("{0:0{1}x}".format(paymaster_data[2], 64))
        + str(paymaster_data[3][2:])
    )

    user_op = {
        "sender": Web3.to_checksum_address(request["sender"]),
        "nonce": Web3.to_int(hexstr=request["nonce"]),
        "initCode": Web3.to_bytes(hexstr=request["initCode"]),
        "callData": Web3.to_bytes(hexstr=request["callData"]),
        "callGasLimit": Web3.to_int(hexstr=request["callGasLimit"]),
        "verificationGasLimit": Web3.to_int(hexstr=request["verificationGasLimit"]),
        "preVerificationGas": Web3.to_int(hexstr=request["preVerificationGas"]),
        "maxFeePerGas": Web3.to_int(hexstr=request["maxFeePerGas"]),
        "maxPriorityFeePerGas": Web3.to_int(hexstr=request["maxPriorityFeePerGas"]),
        "paymasterAndData": Web3.to_bytes(hexstr=paymaster_and_data),
        "signature": Web3.to_bytes(hexstr=request["signature"]),
    }

    # Get the hash
    returned_hash = paymaster.functions.getHash(
        user_op, valid_until, valid_after
    ).call()
    returned_hash = defunct_hash_message(returned_hash)
    paymaster_signer = w3.eth.account.from_key(os.getenv("PRIVATE_KEY"))
    sig = paymaster_signer.signHash(returned_hash)
    paymaster_data[-1] = HexBytes(sig.signature.hex())

    # Construct paymaster_and_data
    paymaster_and_data = (
        str(paymaster_data[0])
        + str("{0:0{1}x}".format(paymaster_data[1], 64))
        + str("{0:0{1}x}".format(paymaster_data[2], 64))
        + str(paymaster_data[3][2:])
        + sig.signature.hex()[2:]
    )

    # Construct validatePaymasterUserOp transaction to estimate gas
    user_op["paymasterAndData"] = paymaster_and_data
    transaction = {
        "from": "0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC",
        "to": paymaster.address,
        "data": paymaster.encodeABI(
            fn_name="validatePaymasterUserOp",
            args=[user_op, returned_hash, w3.to_wei(1, "ether")],
        ),
    }
    gas_estimate = w3.eth.estimate_gas(transaction)

    result = {
        "paymasterAndData": paymaster_and_data,
        "preVerificationGas": gas_estimate,
        "verificationGasLimit": gas_estimate,
        "callGasLimit": int(
            (user_op["preVerificationGas"] / user_op["callGasLimit"]) * gas_estimate
        ),
    }

    return Success(result)


@app.post("/")
async def index(request: Request):
    return Response(dispatch(await request.body()))


if __name__ == "__main__":
    PORT = os.getenv("PORT")
    uvicorn.run("main:app", port=8000, reload=True)
