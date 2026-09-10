```text
======================================================================
   ____                 _____           _
  / ___|_ __ _   _ _ __|_   _|__   ___ | |
 | |   | '__| | | | '_ \ | |/ _ \ / _ \| |
 | |___| |  | |_| | |_) || | (_) | (_) | |
  \____|_|   \__, | .__/ |_|\___/ \___/|_|      v1.0
             |___/|_|

CrypTool by Ali Burhan | https://github.com/ab-ratul
======================================================================
```
**An Interactive Cryptographic Engine & Vulnerability Scanner**

Built by **Ali Burhan** | Main project is at [github.com/ab-ratul/cryptool](github.com/ab-ratul/cryptoo)

CrypTool is a Python-based command-line interface (CLI) application designed to demonstrate the fundamental mechanics of data confidentiality. Developed as part of the DecodeLabs Industrial Training Kit (Project 2: Basic Encryption & Decryption), this tool transforms static text into secure ciphertext using mathematical obfuscation and actively audits its own security through automated brute-force scanning.

---

## 📑 Table of Contents
1. [Features](#-features)
2. [Cryptographic Architecture](#-cryptographic-architecture)
3. [For Recruiters: Technical Highlights](#-for-recruiters-technical-highlights)
4. [Getting Started (Beginner Guide)](#-getting-started)
5. [Usage & Shortcuts](#-usage--shortcuts)

---

## ✨ Features
* **Caesar Cipher Engine:** Implements mono-alphabetic substitution using a user-defined integer shift key.
* **Vigenère Cipher Evolution:** Upgrades static defense to polyalphabetic substitution using a dynamic string keyword, mitigating standard frequency analysis attacks.
* **Automated Vulnerability Scanner:** Simulates a penetration testing environment by brute-forcing ciphertext (Caesar) to expose the "single point of failure" in basic ciphers.
* **Dynamic Network I/O:** Fetches a 10,000-word English dictionary directly from GitHub at runtime to perform intelligent plaintext identification.
* **Audit Logging:** Automatically records successful dictionary-attack breaches (timestamp, shift key, and payload) to a local `compromised_data.txt` file.
* **Resilient CLI:** Features global keyboard shortcuts, strict input validation, and network timeout fallbacks to ensure an error-free user experience.

---

## 🧮 Cryptographic Architecture
This tool operates on the Input-Process-Output (IPO) model, converting standard raw ASCII text into integers before applying modular arithmetic. 

The core mathematical transformation for the Caesar Cipher relies on a symmetric key $n$ and character position $x$:
* **Encryption:** $E_n(x) = (x + n) \pmod{26}$
* **Decryption:** $D_n(x) = (x - n) \pmod{26}$

By preserving non-alphabetic characters (spaces, punctuation) and seamlessly wrapping the alphabet using the modulo operator (`% 26`), the engine prevents mathematical overflow and maintains data integrity during the encryption lifecycle.

---

## 🎯 Technical Highlights
If you are reviewing this code, here is what this project demonstrates:

* **Object-Oriented Programming (OOP):** The core logic is encapsulated within a `CryptographicEngine` class, making the code modular, reusable, and easy to integrate into larger security frameworks.
* **Offensive Security Tooling:** The vulnerability scanner mimics real-world password cracking tools (like Hashcat). It sanitizes raw data, splits strings, and scores potential plaintexts against a loaded dictionary to automate the identification of compromised data.
* **Exception Handling & Fault Tolerance:** The script is fortified with `try-except` blocks. If the external dictionary URL goes offline, the tool silently falls back to a hardcoded micro-dictionary without crashing. Invalid user inputs are caught and handled gracefully.
* **Custom Interrupt Signals:** Implements a custom exception (`ReturnToMenu`) bound to `Ctrl+B`, showcasing advanced control flow manipulation within Python's standard `while` loops.

---

## 🚀 Getting Started

### Prerequisites
You only need **Python 3.x** installed on your system. No external pip libraries are required; the script relies entirely on standard built-in Python libraries (`os`, `time`, `urllib`, `datetime`, `sys`).

### Installation
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/ab-ratul/cryptool.git
   ```

 5. Navigate into the project directory:

```bash
cd cryptool
```
3. Run the application:

```bash
python cryptool.py
```

### 💻 Usage & Shortcuts
Upon launching, you will be greeted by the CrypTool interactive terminal. Enter a number between 1 and 6 to select your desired cryptographic module.

### Global Keyboard Shortcuts
To make navigation fast and professional, the following shortcuts are hardcoded into the input listener:

Ctrl + C: Instantly safely terminate the application from anywhere.

Ctrl + B + Enter: Abort the current operation and immediately return to the main menu banner.

### Example Workflow: Testing the Scanner
Select Option 1 and encrypt the phrase: Security architecture is critical with a shift of 5.

Copy the resulting ciphertext.

Select Option 5 and paste the ciphertext.

Watch as the tool brute-forces 25 keys, identifies the english words, isolates the correct payload, and writes the compromise to your local log file.

