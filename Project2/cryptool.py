import time
import os
import urllib.request
from datetime import datetime
import sys

class ReturnToMenu(Exception):
    """Custom exception to handle returning to the main menu (Ctrl+B)."""
    pass

def get_input(prompt_text: str) -> str:
    """
    Safely captures user input. 
    Listens for Ctrl+B (\x02) to trigger a return to the main menu.
    """
    try:
        user_in = input(prompt_text)
        # Check for Ctrl+B (STX) character or EOF
        if '\x02' in user_in:
            raise ReturnToMenu()
        return user_in
    except EOFError:
        raise ReturnToMenu()

class CryptographicEngine:
    """Handles mathematical data obfuscation, decryption, and network i/o."""
    
    def __init__(self, log_path="compromised_data.txt"):
        self.log_path = log_path
        self.dictionary = self._load_online_dictionary()
        
    def _load_online_dictionary(self) -> set:
        """Fetches a 10,000-word English dictionary dynamically from GitHub."""
        url = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt"
        print(f"[*] Fetching online dictionary from {url}...")
        try:
            # Adding a 5-second timeout to prevent infinite hanging
            with urllib.request.urlopen(url, timeout=5) as response:
                text = response.read().decode('utf-8')
                words = set(text.splitlines())
            print(f"[+] Successfully loaded {len(words)} English words into memory.")
            time.sleep(1)
            return words
        except Exception as e:
            print(f"[!] Network error: {e}")
            print("[*] Falling back to offline micro-dictionary.")
            time.sleep(2)
            return {"the", "be", "to", "of", "and", "a", "in", "that", "have", "i", 
                    "it", "for", "not", "on", "with", "test", "data", "admin", "password"}

    def _log_finding(self, shift: int, plaintext: str) -> None:
        """Writes identified payloads to an external log file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.log_path, 'a', encoding='utf-8') as log_file:
                log_file.write(f"[{timestamp}] SHIFT: -{shift:02d} | PAYLOAD: {plaintext}\n")
            print(f"[+] Successfully logged finding to '{self.log_path}'")
        except Exception as e:
            print(f"[!] Failed to write log: {e}")

    def caesar_cipher(self, text: str, shift: int, decrypt: bool = False) -> str:
        """Applies mathematical shift to text data."""
        if decrypt:
            shift = -shift
            
        result = []
        for char in text:
            if char.isupper():
                result.append(chr((ord(char) - 65 + shift) % 26 + 65))
            elif char.islower():
                result.append(chr((ord(char) - 97 + shift) % 26 + 97))
            else:
                result.append(char)
        return "".join(result)

    def vigenere_cipher(self, text: str, key: str, decrypt: bool = False) -> str:
        """Applies polyalphabetic substitution to text data."""
        result = []
        key_index = 0
        key = key.upper()
        
        for char in text:
            if char.isalpha():
                shift = ord(key[key_index % len(key)]) - 65
                if decrypt:
                    shift = -shift
                    
                if char.isupper():
                    result.append(chr((ord(char) - 65 + shift) % 26 + 65))
                else:
                    result.append(chr((ord(char) - 97 + shift) % 26 + 97))
                key_index += 1
            else:
                result.append(char)
        return "".join(result)

    def vulnerability_scanner(self, ciphertext: str) -> None:
        """Brute forces ciphertext and evaluates results against the dictionary."""
        print("\n[*] Initializing automated brute force scan...")
        time.sleep(1)
                        
        best_match = ""
        best_shift = 0
        max_word_count = 0
        
        for key in range(1, 26):
            decrypted = self.caesar_cipher(ciphertext, key, decrypt=True)
            print(f"[-] Attempting shift -{key:02d}: {decrypted}")
            
            cleaned_text = ''.join(char.lower() if char.isalpha() or char.isspace() else ' ' for char in decrypted)
            words = cleaned_text.split()
            
            score = sum(1 for word in words if word in self.dictionary)
            
            if score > max_word_count:
                max_word_count = score
                best_match = decrypted
                best_shift = key
                
            time.sleep(0.05)
            
        print("\n" + "="*45)
        if max_word_count > 0:
            print("[!] Identified plain text payload:")
            print(f">>> Shift -{best_shift:02d}: {best_match}")
            self._log_finding(best_shift, best_match)
        else:
            print("[?] Scan complete: Could not confidently verify text against dictionary. Manually check it")
            print(">>> Payload may be gibberish, too short, or use advanced encryption.")
        print("="*45)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = """
======================================================================
   ____                 _____           _ 
  / ___|_ __ _   _ _ __|_   _|__   ___ | |
 | |   | '__| | | | '_ \ | |/ _ \ / _ \| |
 | |___| |  | |_| | |_) || | (_) | (_) | |
  \____|_|   \__, | .__/ |_|\___/ \___/|_|
             |___/|_|                     
                                        
CrypTool by Ali Burhan | https://github.com/ab-ratul/
======================================================================
    """
    print(banner)

def main_loop():
    clear_screen()
    print(">>> Booting cryptographic engine...")
    engine = CryptographicEngine()
    
    while True:
        try:
            clear_screen()
            print_banner()
            print("Global Shortcuts: [Ctrl+C] Exit | [Ctrl+B + Enter] Main Menu\n")
            print("1. Secure Data (Caesar Cipher)")
            print("2. Reverse Data (Caesar Decrypt)")
            print("3. Secure Data (Vigenere Evolution)")
            print("4. Reverse Data (Vigenere Decrypt)")
            print("5. Run Caesar Cipher Vulnerability Scanner (Brute Force Decrypt)")
            print("6. Exit System")
            
            choice = get_input("\nSelect an execution mode (1-6): ").strip()
            
            if choice == "1":
                text = get_input("Enter raw plaintext: ")
                shift_input = get_input("Enter integer shift key: ")
                try:
                    shift = int(shift_input)
                    encrypted = engine.caesar_cipher(text, shift)
                    print(f"\n[+] Ciphertext output: {encrypted}")
                except ValueError:
                    print("\n[!] Error: Shift key must be a valid integer.")
                    
            elif choice == "2":
                text = get_input("Enter ciphertext: ")
                shift_input = get_input("Enter integer shift key: ")
                try:
                    shift = int(shift_input)
                    decrypted = engine.caesar_cipher(text, shift, decrypt=True)
                    print(f"\n[+] Decrypted plaintext: {decrypted}")
                except ValueError:
                    print("\n[!] Error: Shift key must be a valid integer.")
                    
            elif choice == "3":
                text = get_input("Enter raw plaintext: ")
                keyword = get_input("Enter string keyword: ")
                if not keyword.isalpha():
                    print("\n[!] Error: Keyword must contain only letters.")
                else:
                    encrypted = engine.vigenere_cipher(text, keyword)
                    print(f"\n[+] Ciphertext output: {encrypted}")
                
            elif choice == "4":
                text = get_input("Enter ciphertext: ")
                keyword = get_input("Enter string keyword: ")
                if not keyword.isalpha():
                    print("\n[!] Error: Keyword must contain only letters.")
                else:
                    decrypted = engine.vigenere_cipher(text, decrypt=True, key=keyword)
                    print(f"\n[+] Decrypted plaintext: {decrypted}")
                
            elif choice == "5":
                text = get_input("Enter isolated ciphertext for analysis: ")
                engine.vulnerability_scanner(text)
                
            elif choice == "6":
                print("\n[*] Terminating session. Goodbye.")
                sys.exit(0)
                
            else:
                print("\n[!] Invalid selection. Please enter a number between 1 and 6.")
                
            get_input("\nPress Enter to continue...")

        except ReturnToMenu:
            # Catches Ctrl+B and cycles back to the start of the while loop
            print("\n[*] Returning to main menu...")
            time.sleep(0.5)
            continue

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        # Catches Ctrl+C at any point during execution to cleanly exit
        print("\n\n[!] Interrupt signal received (Ctrl+C).")
        print("[*] Terminating application safely. Goodbye.")
        sys.exit(0)
