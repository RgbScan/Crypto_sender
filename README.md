# Send Native Token

## Project Description
This project is designed to send native tokens to multiple addresses. The scripts automatically read addresses from JSON files and send tokens to these addresses at specified time intervals.

## Project Structure
The project consists of the following files:
- read_wallets.py: Script for reading addresses from a JSON file.
- time_wait.py: Script for managing time intervals between token sends.


> Clone the repository:
```git clone https://github.com/RgbScan/Crypto_sender.git```

> Navigate to the project directory:
```cd Crypto_sender```

> Create a virtual environment:
```python -m venv venv```

> Activate the virtual environment:
```.\venv\Scripts\activate```

> Install the dependencies:
```pip install -r requirements.txt```


## Usage
Reading Addresses from a JSON File
1. Ensure your JSON file with addresses has the following structure - wallets.json
```
{
  "networks": {
    "Ethereum Mainnet": {
      "url": "https://1rpc.io/eth",
      "chainId": 1
    },
    "Binance Smart Chain": {
      "url": "https://bsc-pokt.nodies.app",
      "chainId": 56
    },
    ...
    # other chain
  },
  "accounts": {
    "NUM_WALLET1": {
      "address": "ADDRESS_WALLET1",
      "private_key": "SEED_PHRASE_WALLET1"
    },
    "NUM_WALLET2": {
      "address": "ADDRESS_WALLET2",
      "private_key": "SEED_PHRASE_WALLET2"
    },
    ...
    # other wallets
}
```
2. Make sure that your JSON file with the addresses to which you will send has the following structure.
```
{
  "NUM_WALLET1": "ADDRESS_TO_SEND_WALLET1",
  "NUM_WALLET2": "ADDRESS_TO_SEND_WALLET2",
  # other wallets
 }
```

## Additional Information
- Ensure that your wallets and tokens are compatible with the network you are using.
- Configure the time intervals and the amount of tokens to send according to your needs.