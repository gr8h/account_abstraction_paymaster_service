# Paymaster RCP Service

This is a project built using FastAPI, Uvicorn, and JSON-RPC Server.

## Installation

1. Run `python3 -m venv .venv` to create a virtual environment
2. Run `source .venv/bin/activate` to activate the virtual environment
3. Run `make install` to install the dependencies
4. Run `make run` to run the server

## Usage

The server will be running at `http://localhost:8000`.

### Environment Variables

```
CHAIN_ID=123
CHAIN_RPC=https://rpc.fusespark.io
PAYMASTER_CONTRACT_ADDRESS=
PRIVATE_KEY=
SPONSOR_ADDRESS=
```

### JSON-RPC Endpoints

- `/pm_sponsorUserOperation`: JSON-RPC endpoint for performing mathematical and string operations

```
{
  "method": "pm_sponsorUserOperation",
  "params": [
    {
      "sender": "0x",
      "nonce": "0x5",
      "initCode": "0x",
      "callData": "",
      "callGasLimit": "0x88b8",
      "verificationGasLimit": "0x33450",
      "preVerificationGas": "0x5208",
      "maxFeePerGas": "0x2e4e2bf80",
      "maxPriorityFeePerGas": "0x2e4e2bf80",
      "paymasterAndData": "0x",
      "signature": "0x"
    },
    "0x5FF137D4b0FDCD49DcA30c7CF57E578a026d2789",
    {}
  ],
  "id": 42,
  "jsonrpc": "2.0"
}


```
