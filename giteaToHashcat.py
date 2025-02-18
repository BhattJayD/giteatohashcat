import sqlite3
import base64
import sys
import argparse
import os
from termcolor import colored

def extract_hashes(db_path):
    if not os.path.exists(db_path):
        print(colored(f"[!] Error: File '{db_path}' not found.", "red"))
        sys.exit(1)
    
    try:
        con = sqlite3.connect(db_path)
        cursor = con.cursor()
        cursor.execute("SELECT name, passwd_hash_algo, salt, passwd FROM user")
        
        users = []
        for row in cursor.fetchall():
            name, algo_info, salt_hex, passwd_hex = row
            
            if 'pbkdf2' in algo_info:
                _, iterations, keylen = algo_info.split("$")
                algo = "sha256"
            else:
                print(colored(f"[!] Unknown algorithm: {algo_info}", "yellow"))
                continue
            
            try:
                salt = bytes.fromhex(salt_hex)
                passwd = bytes.fromhex(passwd_hex)
                salt_b64 = base64.b64encode(salt).decode("utf-8")
                passwd_b64 = base64.b64encode(passwd).decode("utf-8")
                users.append(f"{name}:{algo}:{iterations}:{salt_b64}:{passwd_b64}")
            except ValueError as ve:
                print(colored(f"[!] Error decoding hex values for user {name}: {ve}", "red"))
                continue
        
        return users
    except sqlite3.Error as e:
        print(colored(f"[!] Database error: {e}", "red"))
        sys.exit(1)
    except Exception as e:
        print(colored(f"[!] Unexpected error: {e}", "red"))
        sys.exit(1)
    finally:
        if 'con' in locals():
            con.close()

def main():
    parser = argparse.ArgumentParser(description="Extract PBKDF2 password hashes from Gitea SQLite database for Hashcat")
    parser.add_argument("db_path", help="Path to the Gitea SQLite database")
    args = parser.parse_args()

    print(colored("[+] Extracting password hashes...", "cyan"))
    users = extract_hashes(args.db_path)
    
    if users:
        print(colored("[+] Extraction complete. Output:", "green"))
        for user in users:
            print(colored(user, "blue"))
    else:
        print(colored("[-] No valid hashes found.", "yellow"))

if __name__ == "__main__":
    main()
