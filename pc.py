import hmac
import hashlib
import requests

def check_real_leaks(password: str) -> bool:
    """
    Prevents usage of known breached passwords using the HIBP API.
    Implements k-Anonymity: only the first 5 chars of the SHA-1 hash are sent.
    """
    # hash the password using SHA-1
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1_password[:5], sha1_password[5:]
    
    try:
        # request all compromised hashes starting with the 5-character prefix
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"\nAPI error: Could not connect to database (status {response.status_code})")
            return False
            
        # check if our hash suffix is in the returned list
        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return True
        return False
        
    except requests.RequestException as e:
        print(f"\nNetwork error: Failed to reach leaked database - {e}")
        return False

def check_password_strength(password: str) -> tuple[bool, str]:
    """
    Evaluates password strength and returns a (Pass/Fail, Classification) tuple.
    Time Complexity: O(n) linear scan.
    """
    # 1. the zero point: length verification (< 8 chars = immediate fail)
    if len(password) < 8:
        return False, "weak"
    if len(password) > 64:
        return False, "oversized payload"
        
    # 2. pythonic approach: short-circuit execution
    has_upper = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_symbol = any(not char.isalnum() and not char.isspace() for char in password)
    
    # 3. mandatory pattern enforcement & risk classification
    if has_upper and has_digit and has_symbol:
        return True, "strong"
    elif has_upper or has_digit or has_symbol:
        return False, "medium"
    else:
        return False, "weak"

def print_banner():
    banner = """
=========================================================
 ____                                     _ 
|  _ \\ __ _ ___ _____      _____  _ __ __| |
| |_) / _` / __/ __\\ \\ /\\ / / _ \\| '__/ _` |
|  __/ (_| \\__ \\__ \\\\ V  V / (_) | | | (_| |
|_|   \\__,_|___/___/ \\_/\\_/ \\___/|_|  \\__,_|
                                            
  ____ _               _             
 / ___| |__   ___  ___| | _____ _ __ 
| |   | '_ \\ / _ \\/ __| |/ / _ \\ '__|
| |___| | | |  __/ (__|   <  __/ |   
 \\____|_| |_|\\___|\\___|_|\\_\\___|_|   v1.0

        by Ali Burhan | https://github.com/ab-ratul
        
---------------------------------------------------------
 PASSWORD REQUIREMENTS:
 - Length: 8 to 64 characters (maximum)
 - Mandatory: A-Z, a-z, 0-9, and Symbols)
 - Status: Must not be found in known data breaches
=========================================================
"""
    print(banner)


if __name__ == "__main__":
    print_banner()
    
    # define ansi color codes
    red = '\033[91m'
    green = '\033[92m'
    yellow = '\033[93m'
    purple = '\033[95m'
    reset = '\033[0m'
    
    try:
        # infinite loop to keep the prompt active
        while True:
            user_input = input("\nPlease enter the password (press ctrl+c to exit): ")
            
            # the zero point: check length immediately
            if len(user_input) < 8:
                print(f"\nWarning: {yellow}Please type more than 8 characters.{reset}")
            
            # 1. calculate strength FIRST, independently of the leak check
            is_valid, classification = check_password_strength(user_input)
            
            # apply colors correctly
            if classification == "weak" or classification == "oversized payload":
                class_color = purple
            elif classification == "medium":
                class_color = yellow
            else:
                class_color = green
                
            # always display password strength result
            print(f"Password strength: {class_color}{classification}{reset}")
            
            # 2. check the live database
            is_leaked_status = check_real_leaks(user_input)
            
            # 3. collect failure reasons to prevent printing "Status: Fail" twice
            failure_reasons = []
            
            if is_leaked_status:
                failure_reasons.append("was found in a leaked database")
            if not is_valid:
                failure_reasons.append("does not meet mandatory pattern requirements")
                
            # 4. print final combined status
            if failure_reasons:
                # joins multiple reasons with ' and ' for a single-line error
                combined_reason = " and ".join(failure_reasons)
                print(f"Status: {red}Fail{reset}. Password {combined_reason}{red}!{reset}")
            else:
                # validation before encryption: filter entropy before argon2id
                print(f"Status: {green}Pass{reset}. Gatekeeper validation successful{green}!{reset} Ready to transfer it to argon2id...")
            
    except (KeyboardInterrupt, EOFError):
        # catches the ctrl+c or ctrl+d command to exit gracefully
        print(f"\n{yellow}Process terminated by user. Exiting terminal...{reset}\n")
    except Exception as e:
        # printing any logic error
        print(f"Logic error detected: {e}")