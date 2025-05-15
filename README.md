These projects are intended solely for educational purposes to help individuals understand the principles of cryptography and blockchain technology. It is important to recognize that attempting to generate Bitcoin wallets in the hope of randomly finding one with a balance is not a feasible strategy. This same logic applies to any tool that tries to work in any way the same as this.

The number of possible Bitcoin wallet combinations exceeds 76 trillion, making the odds of discovering an active wallet astronomically low. To put it into perspective, you are statistically far more likely to win the lottery every day for the rest of your life than to recover even a single wallet with funds—even over the course of a decade.


![image](https://github.com/user-attachments/assets/11265c24-41b9-4251-92f6-391338b8bc50)



# Satoshi Sweeper

Satoshi Sweeper is a Bitcoin wallet generator and balance checker. 
It generates mnemonic phrases, derives Bitcoin addresses (Legacy, Nested SegWit, and Native SegWit), and checks their balances using the Blockstream API.


## Assembly
- Generate 12-word or 24-word mnemonics
- Derive Bitcoin addresses (Legacy, Nested SegWit, Native SegWit)
- Check wallet balances automatically
- Save wallets with a positive balance


## Requirements

- python3
```
pip install requests colorama bip-utils
```


## Disclaimer
> This script is for educational and research purposes only. The author is not responsible for any misuse or unethical activities performed using this tool.
