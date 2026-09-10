```text
=========================================================
 ____                                     _ 
|  _ \ __ _ ___ _____      _____  _ __ __| |
| |_) / _` / __/ __\ \ /\ / / _ \| '__/ _` |
|  __/ (_| \__ \__ \\ V  V / (_) | | | (_| |
|_|   \__,_|___/___/ \_/\_/ \___/|_|  \__,_|
                                            
  ____ _               _             
 / ___| |__   ___  ___| | _____ _ __ 
| |   | '_ \ / _ \/ __| |/ / _ \ '__|
| |___| | | |  __/ (__|   <  __/ |   
 \____|_| |_|\___|\___|_|\_\___|_|   v1.0

             by Ali Burhan | https://github.com/ab-ratul

---------------------------------------------------------
 GATEKEEPER REQUIREMENTS:
 - Length: 8 to 64 characters
 - Mandatory: A-Z, a-z, 0-9, @%$#&... (Symbols)
 - Status: Must not be found in known data breaches
=========================================================
```

# Enterprise Password Gatekeeper and Breach Checker

## Overview and Purpose

This project is a defensive cybersecurity tool designed to evaluate password strength and securely cross-reference inputs against known data breaches. It was built to fulfill the Project 1 requirements for the DecodeLabs Industrial Training Kit, functioning as a strict validation gatekeeper before cryptographic hashing. Main project with version updates can be found at https://github.com/ab-ratul/password-checker.

* **Validates Entropy:** Enforces mandatory password requirements—including length, uppercase, numbers, and symbols—to establish a strong digital foundation.


* **Prevents Automated Injection:** Blocks the use of compromised credentials to mitigate brute-force risks in enterprise authentication traffic.


* **Demonstrates Security Logic:** Focuses heavily on secure string-handling, programmatic condition checks, and robust risk classification.



## Security Architecture

The codebase is engineered with professional cybersecurity principles, ensuring data privacy and execution efficiency.

* **k-Anonymity Integration:** Hashes inputs via SHA-1 and queries the live Have I Been Pwned (HIBP) API using only a 5-character prefix, guaranteeing that plaintext passwords are never transmitted or exposed over the network.
* **O(n) Linear Scan Complexity:** Utilizes Pythonic short-circuit execution to ensure that processing time grows linearly, avoiding exponential delays during raw byte stream validation.


* **Constant-Time Comparison:** Mitigates advanced timing attacks by employing `hmac.compare_digest` to validate local data secrets without leaking information via process delays.


* **Unicode Entropy Support:** Natively handles expanded character properties, extending the validation search space from standard ASCII out to over 143,000 Unicode variants.



## Installation and Usage Guide

This program requires Python 3.x and the standard `requests` library to interface with the live threat intelligence API.

* **Clone the Repository:** Download the project environment by running `git clone https://github.com/ab-ratul/password-checker.git` in your local terminal.
* **Install Dependencies:** Go to the tool directory by typing `cd password-checker`. Execute `pip install requests` to enable the secure external HTTP calls required for the breach database.
* **Launch the Script:** Run the interactive terminal loop by executing `python pc.py`. Enter strings at the prompt to receive real-time strength classifications and vulnerability alerts.


## Requirements:

Internet connection is required to check for the live data breach. Otherwise it will only check for password strength.


## Disclaimer:

This tool is intended for free and safe use. Only 5 character of SHA1 hash is shared with breached databases at pwnedpasswords.com to check whether the password was leaked in a known data breach.

