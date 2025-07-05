# Automated Chia Farming Setup

[![Python Version](https://img.shields.io/badge/python-3+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OS: Linux](https://img.shields.io/badge/OS-Linux-blue.svg)](https://www.linux.org)

This repository contains a Python script to automate the setup process for a Chia farmer on a Debian-based Linux system (e.g., Ubuntu). The script will install system dependencies, clone the official Chia blockchain repository, configure it, generate a new wallet key, and start the farmer.

## Prerequisites

- A Debian-based Linux distribution (e.g., Ubuntu).
- Python 3.
- `sudo` privileges. The script will prompt for your password to install system dependencies.
- An active internet connection.

## How to Use

1.  Ensure you have `python3` installed on your system.
2.  Run the script from your terminal:

    ```bash
    python3 farming.py
    ```

The script will then execute all the necessary steps. Follow any on-screen instructions.

## What the Script Does

The script automates the following steps:

1.  **Installs System Dependencies:** Updates `apt` and installs `git`, `python3-venv`, and `python3-pip` if they are not already present.
2.  **Clones Chia-Blockchain Repository:** Clones the official repository from `https://github.com/Chia-Network/chia-blockchain.git` into a `chia-blockchain` directory. If the directory already exists, it skips this step.
3.  **Runs Chia Installer:** Executes the `install.sh` script provided in the Chia repository. This sets up a Python virtual environment and installs all required dependencies.
4.  **Initializes Chia:** Runs `chia init` to create the default configuration files and directory structure under `~/.chia/mainnet`.
5.  **Generates Wallet Key:** Creates a new set of keys for your wallet.
    -   **!!! IMPORTANT !!!**: The script will display a 24-word mnemonic phrase. This is your private key. **You must back it up in a safe and secure location.** It is the only way to recover your wallet.
6.  **Starts the Farmer:** Starts the Chia farmer, full node, and other services in the background.

## After Setup

Once the script is complete, your Chia full node will start syncing with the blockchain. This can take a significant amount of time.

You can manage your Chia farm using the command line. First, navigate to the `chia-blockchain` directory and activate the virtual environment:

```bash
cd chia-blockchain
. ./activate
```

Then you can use standard `chia` commands:

-   **Check farm status:**
    ```bash
    chia farm summary
    ```
-   **Check node and blockchain status:**
    ```bash
    chia show -s
    ```
-   **Stop all services:**
    ```bash
    chia stop all -d
    ```

For more information on plotting and managing your farm, please refer to the [official Chia documentation](https://docs.chia.net/cli/).

## Security Note

-   The script requires `sudo` to install packages. Review the script before running it to ensure you are comfortable with the commands being executed.
-   **Back up your 24-word mnemonic phrase.** Anyone with access to it can control your funds. Do not share it.

## Disclaimer

**DISCLAIMER:** This is an unofficial script and is not affiliated with Chia Network Inc. Use it at your own risk. Always ensure you understand what a script does before running it, especially when it requires `sudo` privileges. 