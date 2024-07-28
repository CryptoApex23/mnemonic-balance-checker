# Mnemonic Balance Checker

<img width="1182" alt="image" src="https://github.com/user-attachments/assets/56b49527-aaa2-4522-9715-9aa3388fada4">


This script generates random mnemonics, validates them, and checks the Ethereum balance for the generated addresses. If an address with a non-zero balance is found, the details are sent to a specified Telegram chat.

## Features

- Generate random 12-word mnemonics from a given wordlist.
- Validate the generated mnemonics using BIP-39 standards.
- Check the Ethereum balance for addresses derived from the mnemonics.
- Send notifications to a Telegram chat when an address with a non-zero balance is found.
- Multi-threaded processing for faster checks.

## Prerequisites

- Python 3.8+
- pip (Python package installer)
- An Infura API key or equivalent Ethereum provider URL.
- A Telegram bot token and chat ID for notifications.

## Installation

1. **Clone the repository**:

   ```sh
   git clone https://github.com/CryptoApex23/mnemonic-balance-checker.git
   cd mnemonic-balance-checker
   ```

2. **Create a virtual environment and activate it**:

   ```sh
   python -m venv venv
   source venv/bin/activate # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies**:

   ```sh
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in the root directory with the following content:

   ```env
   INFURA_URL=https://eth-mainnet.g.alchemy.com/v2/your_infura_api_key
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   TELEGRAM_CHAT_ID=your_telegram_chat_id
   ```

## Usage

Run the script with the path to your wordlist file:

```sh
python mnemonic_balance_checker.py <wordlist_file>
```

Replace <wordlist_file> with the path to your wordlist file.

## Example

```sh
python mnemonic_balance_checker.py wordlist.txt
```

## Logging

The script logs all activities to a file named app.log in the same directory. This includes info messages for successful operations and error messages for any issues encountered during execution.

## Environment Variables

- INFURA_URL: Your Ethereum provider URL (e.g., Infura, Alchemy).
- TELEGRAM_BOT_TOKEN: Your Telegram bot token.
- TELEGRAM_CHAT_ID: The chat ID where notifications will be sent.

## Contributing

1. Fork the repository.
2. Create your feature branch (git checkout -b feature/AmazingFeature).
3. Commit your changes (git commit -m 'Add some AmazingFeature').
4. Push to the branch (git push origin feature/AmazingFeature).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

If you have any questions or issues, feel free to open an issue on GitHub or contact me on telegram @cryptoapex_hub.
