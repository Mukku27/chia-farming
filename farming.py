import os
import subprocess
import sys
from pathlib import Path

# ANSI color codes for better terminal output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def run_command(command, cwd=None, check=True):
    """
    Executes a shell command in a specified directory and streams its output.
    This provides real-time feedback for long-running processes.
    """
    if cwd:
        print(f"{bcolors.OKBLUE}--- Running command: {' '.join(command)} in {cwd} ---{bcolors.ENDC}")
    else:
        print(f"{bcolors.OKBLUE}--- Running command: {' '.join(command)} ---{bcolors.ENDC}")

    try:
        # Use Popen to capture and stream output in real-time
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=cwd,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )

        # Stream the output line by line
        for line in iter(process.stdout.readline, ''):
            print(line, end='', flush=True)

        process.stdout.close()
        return_code = process.wait()

        # Check for command failure
        if check and return_code != 0:
            print(f"\n{bcolors.FAIL}--- Command failed with exit code {return_code} ---{bcolors.ENDC}")
            raise subprocess.CalledProcessError(return_code, command)

        print(f"\n{bcolors.OKGREEN}--- Command successful ---{bcolors.ENDC}")
        return return_code

    except FileNotFoundError:
        print(f"{bcolors.FAIL}Error: Command not found: {command[0]}{bcolors.ENDC}")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"{bcolors.FAIL}An error occurred while executing command: {' '.join(command)}{bcolors.ENDC}")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"{bcolors.FAIL}An unexpected error occurred: {e}{bcolors.ENDC}")
        sys.exit(1)

def main():
    """
    Main function to orchestrate the Chia setup and farming process.
    """
    print(f"{bcolors.HEADER}=== Starting Automated Chia Farming Setup ==={bcolors.ENDC}")

    # --- Step 1: Install System-level Dependencies ---
    # This assumes a Debian-based Linux (e.g., Ubuntu) and requires sudo access.
    # The script will prompt for a password if sudo requires it.
    print("\n>>> STEP 1: Installing system dependencies (git, python3-venv)...")
    try:
        run_command(["sudo", "apt-get", "update", "-y"])
        run_command(["sudo", "apt-get", "install", "-y", "git", "python3-venv", "python3-pip"])
    except Exception:
        print(f"{bcolors.FAIL}Could not install system dependencies. Please install 'git' and 'python3-venv' manually and re-run the script.{bcolors.ENDC}")
        sys.exit(1)

    # --- Step 2: Clone the Official Chia-Blockchain Repository ---
    print("\n>>> STEP 2: Cloning the official Chia-Blockchain repository...")
    repo_url = "https://github.com/Chia-Network/chia-blockchain.git"
    repo_dir = Path.cwd() / "chia-blockchain"
    if not repo_dir.exists():
        run_command(["git", "clone", repo_url])
    else:
        print(f"{bcolors.OKCYAN}Directory '{repo_dir.name}' already exists. Skipping clone.{bcolors.ENDC}")

    # --- Step 3: Run the Chia Installer Script ---
    print("\n>>> STEP 3: Running the Chia installer script (install.sh)...")
    # The install.sh script sets up the Python virtual environment (.venv)
    # and installs all necessary Python packages using Poetry.
    installer_script = repo_dir / "install.sh"
    run_command(["chmod", "+x", str(installer_script)])
    run_command(["sh", str(installer_script)], cwd=repo_dir)

    # --- Step 4: Initialize Chia Configuration ---
    print("\n>>> STEP 4: Initializing Chia configuration...")
    # This creates the default ~/.chia/mainnet directory structure and config.yaml.
    # We use activated.py to run commands within the correct virtual environment.
    activated_script = repo_dir / "activated.py"
    run_command(["chmod", "+x", str(activated_script)])
    run_command([str(activated_script), "chia", "init"], cwd=repo_dir)

    # --- Step 5: Generate a New Wallet Key ---
    print(f"\n>>> STEP 5: Generating a new wallet key...")
    print(f"{bcolors.BOLD}{bcolors.WARNING}{'=' * 70}")
    print("!!! IMPORTANT: The following 24-word mnemonic is your private key. !!!")
    print("!!! Back it up securely. It is the ONLY way to recover your wallet. !!!")
    print(f"{'=' * 70}{bcolors.ENDC}")
    # This command is non-interactive and will print the new key's mnemonic.
    run_command([str(activated_script), "chia", "keys", "generate"], cwd=repo_dir)
    print(f"{bcolors.BOLD}{bcolors.WARNING}{'=' * 70}")
    print("!!! Mnemonic phrase displayed above. Please write it down and save it securely. !!!")
    print(f"{'=' * 70}{bcolors.ENDC}")

    # --- Step 6: Start the Farmer ---
    print("\n>>> STEP 6: Starting the farmer...")
    # 'chia start farmer' launches the full_node, harvester, farmer, and wallet
    # services in the background as daemon processes.
    run_command([str(activated_script), "chia", "start", "farmer"], cwd=repo_dir)

    # --- Step 7: Final Instructions ---
    print(f"\n{bcolors.HEADER}{'='*60}")
    print(">>> SETUP COMPLETE! <<<")
    print(f"{'='*60}{bcolors.ENDC}")
    print(f"\n{bcolors.OKGREEN}Chia services have been started in the background.{bcolors.ENDC}")
    print("The full node will now start syncing to the blockchain, which may take some time.")
    print("You can add plots via the CLI to start farming.")
    print("\nTo check the status of your farm and node, run the following commands from the 'chia-blockchain' directory:")
    print(f"{bcolors.OKCYAN}  . ./activate")
    print(f"  chia farm summary")
    print(f"  chia show -s{bcolors.ENDC}")
    print("\nTo stop all services, run:")
    print(f"{bcolors.OKCYAN}  . ./activate")
    print(f"  chia stop all -d{bcolors.ENDC}")
    print(f"\n{bcolors.BOLD}{bcolors.WARNING}REMINDER: Ensure you have backed up your 24-word mnemonic phrase!{bcolors.ENDC}")

if __name__ == "__main__":
    main()