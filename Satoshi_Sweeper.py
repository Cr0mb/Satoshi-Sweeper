import os
import subprocess
import tarfile
import random
import time
import requests
from colorama import Fore, Style, init
from bip_utils import (
    Bip39MnemonicGenerator,
    Bip39SeedGenerator,
    Bip84,
    Bip84Coins,
    Bip49,
    Bip49Coins,
    Bip44,
    Bip44Coins,
    Bip44Changes
)

init(autoreset=True)


def generate_mnemonic(num_words=12):
    if num_words == 12:
        return Bip39MnemonicGenerator().FromWordsNumber(12)
    elif num_words == 24:
        return Bip39MnemonicGenerator().FromWordsNumber(24)
    else:
        raise ValueError(f"{Fore.RED}Error: Choose 12 or 24 words only{Style.RESET_ALL}")


def derive_addresses(mnemonic):
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()

    bip44_btc = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
    btc_legacy_address = bip44_btc.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PublicKey().ToAddress()

    bip49_btc = Bip49.FromSeed(seed_bytes, Bip49Coins.BITCOIN)
    btc_nested_segwit_address = bip49_btc.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PublicKey().ToAddress()

    bip84_btc = Bip84.FromSeed(seed_bytes, Bip84Coins.BITCOIN)
    btc_native_segwit_address = bip84_btc.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PublicKey().ToAddress()

    return btc_legacy_address, btc_nested_segwit_address, btc_native_segwit_address, mnemonic.ToStr()


def check_btc_info(address):
    url = f"https://blockstream.info/api/address/{address}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        funded_satoshis = data.get("chain_stats", {}).get("funded_txo_sum", 0)
        spent_satoshis = data.get("chain_stats", {}).get("spent_txo_sum", 0)
        balance_satoshis = funded_satoshis - spent_satoshis
        balance_btc = balance_satoshis / 1e8
        return balance_btc, balance_satoshis
    except Exception:
        return None, None


def save_wallet(mnemonic, address, balance_btc):
    with open("wallets.txt", "a") as f:
        f.write(f"Mnemonic: {mnemonic}\nAddress: {address}\nBalance: {balance_btc:.8f} BTC\n\n")


def generate_wallets(option):
    try:
        while True:
            num_words = 12 if option == "12" else 24 if option == "24" else random.choice([12, 24])
            btc_legacy, btc_nested, btc_native, mnemonic = derive_addresses(generate_mnemonic(num_words))

            print(f"\n{Fore.CYAN}{'=' * 40}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Generated {num_words}-word Wallet:{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Mnemonic: {Style.BRIGHT}{mnemonic}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}BTC Legacy Address: {Fore.WHITE}{btc_legacy}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}BTC Nested SegWit Address: {Fore.WHITE}{btc_nested}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}BTC Native SegWit Address: {Fore.WHITE}{btc_native}{Style.RESET_ALL}")

            for address in [btc_legacy, btc_nested, btc_native]:
                print(f"{Fore.BLUE}Checking balance for {address}...{Style.RESET_ALL}")
                balance_btc, balance_satoshis = check_btc_info(address)
                
                if balance_btc is not None:
                    balance_msg = f"{Fore.GREEN}{balance_btc:.8f} BTC ({balance_satoshis} satoshis){Style.RESET_ALL}"
                    if balance_btc > 0:
                        save_wallet(mnemonic, address, balance_btc)
                        print(f"{Fore.LIGHTGREEN_EX}[SAVED] {address} - {balance_msg}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.YELLOW}{address}: {balance_msg}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}{address}: Balance check failed{Style.RESET_ALL}")

            print(f"{Fore.CYAN}{'=' * 40}{Style.RESET_ALL}\n")
            time.sleep(2)
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Process stopped by user. Exiting...{Style.RESET_ALL}")


if __name__ == "__main__":
    print(f"{Fore.GREEN}{' ' * 10}Satoshi Sweeper{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{' ' * 10}Made by Cr0mb{Style.RESET_ALL}")
    print(f"\n{Fore.CYAN}{'=' * 30}{Style.RESET_ALL}\n")
    
    print(f"{Fore.MAGENTA}Choose an option:{Style.RESET_ALL}")
    print(f"{Fore.BLUE}1. Generate 12-word wallets{Style.RESET_ALL}")
    print(f"{Fore.BLUE}2. Generate 24-word wallets{Style.RESET_ALL}")
    print(f"{Fore.BLUE}3. Generate both randomly{Style.RESET_ALL}")
    print(f"\n{Fore.CYAN}{'=' * 30}{Style.RESET_ALL}\n")

    choice = input(f"{Fore.YELLOW}Enter your choice (12/24/both): {Style.RESET_ALL}").strip().lower()
    generate_wallets(choice)
