import os
import getpass
import base64
import json
from datetime import datetime, timedelta
from utils.colors import *

class TerminalMenu:
    def __init__(self, user_manager, logger):
        self.user_manager = user_manager
        self.logger = logger

    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def print_header(self):
        print(f"{HEADER}Multi-Protocol Tunneling Server - User Management{ENDC}")
        print("=" * 50)

    def print_menu(self):
        self.clear_screen()
        self.print_header()
        print(f"\n{BOLD}Available Options:{ENDC}")
        print("1. Create SSH User")
        print("2. Create VMESS User")
        print("3. Create VLESS User")
        print("4. Create Trojan User")
        print("5. List Users")
        print("6. Delete User")
        print("0. Exit")
        print("\n" + "=" * 50)

    def get_input(self, prompt):
        return input(f"{OKBLUE}{prompt}: {ENDC}")

    def create_ssh_user(self):
        print(f"\n{BOLD}Create SSH User{ENDC}")
        username = self.get_input("Enter username")
        password = getpass.getpass(f"{OKBLUE}Enter password: {ENDC}")
        ip_limit = self.get_input("Enter IP limit (number of devices)")
        days_valid = self.get_input("Enter account validity in days")

        try:
            ip_limit = int(ip_limit)
            days_valid = int(days_valid)
        except ValueError:
            print(f"{FAIL}Invalid input. Using defaults: 1 device, 1 day{ENDC}")
            ip_limit = 1
            days_valid = 1

        # Calculate expiry date based on user input
        expiry_date = (datetime.now() + timedelta(days=days_valid)).strftime("%d %b, %Y")

        user = self.user_manager.create_ssh_user(username, password, ip_limit, days_valid)

        # Print formatted output
        print("\n" + "═" * 56)
        print("                [ SSH OPENVPN ]")
        print("═" * 56)
        print(f" Username      : {username}")
        print(f" Password    : {password}")
        print(f" Limit Ip    : {ip_limit} Device")
        print(f" Domain      : sg1prem.kedaivpn.cloud")
        print(f" ISP         : DigitalOcean, LLC")
        print(f" OpenSSH     : 443, 80, 22")
        print(f" Port UDP    : 1-65535")
        print(f" SSH WS      : 80,8080,8880,2082")
        print(f" SSL/TLS     : 443")
        print("─" * 56)
        print(f" SSH WS Non TLS : sg1prem.kedaivpn.cloud:80@{username}:{password}")
        print(f" WS SSL/TLS    : sg1prem.kedaivpn.cloud:443@{username}:{password}")
        print(f" Udp Custom  : sg1prem.kedaivpn.cloud:1-65535@{username}:{password}")
        print("─" * 56)
        print(" Payload WS  : GET / HTTP/1.1[crlf]Host: [host][crlf]Connection: Upgrade[crlf]User-Agent: [ua][crlf]Upgrade: websocket[crlf][crlf]")
        print("─" * 56)
        print(" Payload TLS : GET wss://sg1prem.kedaivpn.cloud/ HTTP/1.1[crlf]Host: [host][crlf]Connection: Upgrade[crlf]User-Agent: [ua][crlf]Upgrade: websocket[crlf][crlf]")
        print("─" * 56)
        print(" Payload ENCD: HEAD / HTTP/1.1[crlf]Host: Masukan_Bug[crlf][crlf]PATCH / HTTP/1.1[crlf]Host: [host][crlf]Upgrade: websocket[crlf][crlf][split]HTTP/ 1[crlf][crlf]")
        print("─" * 56)
        print(f" Days in : {days_valid} Day{'s' if days_valid > 1 else ''}")
        print(f" Expiry in : {expiry_date}")
        print("═" * 56)
        print("                SCRIPT BY KedaiVPN")
        print("═" * 56)

        input("\nPress Enter to continue...")

    def create_vmess_user(self):
        print(f"\n{BOLD}Create VMESS User{ENDC}")
        username = self.get_input("Enter username")
        user = self.user_manager.create_vmess_user(username)

        # Base configurations
        base_config = {
            "v": "2",
            "ps": username,
            "add": "sg1prem.kedaivpn.cloud",
            "id": user['id'],
            "aid": "0",
            "net": "ws",
            "type": "none",
            "host": "sg1prem.kedaivpn.cloud"
        }

        # Create configurations for different ports and protocols
        configs = {
            "WS Non TLS": {**base_config, "port": "80", "path": "/vmess", "tls": "none"},
            "WS TLS": {**base_config, "port": "443", "path": "/vmess", "tls": "tls"},
            "gRPC": {**base_config, "port": "443", "net": "grpc", "path": "/vmessgrpc", "type": "gun", "tls": "tls"}
        }

        # Generate base64 links
        links = {name: 'vmess://' + base64.b64encode(json.dumps(config).encode()).decode()
                for name, config in configs.items()}

        print("\n" + "═" * 56)
        print("                [ VMESS ACCOUNT ]")
        print("═" * 56)
        print(f" Username      : {username}")
        print(f" Domain       : sg1prem.kedaivpn.cloud")
        print(f" Port WS      : 80")
        print(f" Port TLS     : 443")
        print(f" Port gRPC    : 443")
        print(f" ID           : {user['id']}")
        print(f" Security     : auto")
        print("─" * 56)
        print(" Link WS      : " + links["WS Non TLS"])
        print("─" * 56)
        print(" Link TLS     : " + links["WS TLS"])
        print("─" * 56)
        print(" Link gRPC    : " + links["gRPC"])
        print("═" * 56)
        print("                SCRIPT BY KedaiVPN")
        print("═" * 56)

        input("\nPress Enter to continue...")

    def create_vless_user(self):
        print(f"\n{BOLD}Create VLESS User{ENDC}")
        username = self.get_input("Enter username")
        user = self.user_manager.create_vless_user(username)

        # Create configuration strings for different protocols
        configs = {
            "WS Non TLS": f"{user['id']}@sg1prem.kedaivpn.cloud:80?security=none&encryption=none&headerType=none&type=ws&path=/vless#{username}",
            "WS TLS": f"{user['id']}@sg1prem.kedaivpn.cloud:443?security=tls&encryption=none&headerType=none&type=ws&path=/vless#{username}",
            "gRPC": f"{user['id']}@sg1prem.kedaivpn.cloud:443?security=tls&encryption=none&headerType=none&type=grpc&serviceName=vlessgrpc&mode=gun#{username}"
        }

        # Convert to base64
        links = {name: 'vless://' + base64.b64encode(config.encode()).decode()
                for name, config in configs.items()}

        print("\n" + "═" * 56)
        print("                [ VLESS ACCOUNT ]")
        print("═" * 56)
        print(f" Username      : {username}")
        print(f" Domain       : sg1prem.kedaivpn.cloud")
        print(f" Port WS      : 80")
        print(f" Port TLS     : 443")
        print(f" Port gRPC    : 443")
        print(f" ID           : {user['id']}")
        print(f" Security     : tls")
        print("─" * 56)
        print(" Link WS      : " + links["WS Non TLS"])
        print("─" * 56)
        print(" Link TLS     : " + links["WS TLS"])
        print("─" * 56)
        print(" Link gRPC    : " + links["gRPC"])
        print("═" * 56)
        print("                SCRIPT BY KedaiVPN")
        print("═" * 56)

        input("\nPress Enter to continue...")

    def create_trojan_user(self):
        print(f"\n{BOLD}Create Trojan User{ENDC}")
        username = self.get_input("Enter username")
        user = self.user_manager.create_trojan_user(username)

        # Create configuration strings for different protocols
        configs = {
            "WS Non TLS": f"trojan://{user['password']}@sg1prem.kedaivpn.cloud:80?path=/trojan-ws&security=none&host=sg1prem.kedaivpn.cloud&type=ws&sni=sg1prem.kedaivpn.cloud#{username}",
            "WS TLS": f"trojan://{user['password']}@sg1prem.kedaivpn.cloud:443?path=/trojan-ws&security=tls&host=sg1prem.kedaivpn.cloud&type=ws&sni=sg1prem.kedaivpn.cloud#{username}",
            "gRPC": f"trojan://{user['password']}@sg1prem.kedaivpn.cloud:443?mode=gun&security=tls&type=grpc&serviceName=trojan-grpc&sni=sg1prem.kedaivpn.cloud#{username}"
        }

        print("\n" + "═" * 56)
        print("                [ TROJAN ACCOUNT ]")
        print("═" * 56)
        print(f" Username      : {username}")
        print(f" Domain       : sg1prem.kedaivpn.cloud")
        print(f" Port WS      : 80")
        print(f" Port TLS     : 443")
        print(f" Port gRPC    : 443")
        print(f" Password     : {user['password']}")
        print(f" Security     : tls")
        print("─" * 56)
        print(" Link WS      : " + configs["WS Non TLS"])
        print("─" * 56)
        print(" Link TLS     : " + configs["WS TLS"])
        print("─" * 56)
        print(" Link gRPC    : " + configs["gRPC"])
        print("═" * 56)
        print("                SCRIPT BY KedaiVPN")
        print("═" * 56)

        input("\nPress Enter to continue...")

    def list_users(self):
        print(f"\n{BOLD}List Users{ENDC}")
        print("1. SSH Users")
        print("2. VMESS Users")
        print("3. VLESS Users")
        print("4. Trojan Users")
        print("0. Back")

        choice = self.get_input("\nSelect protocol")

        protocols = {
            '1': 'ssh',
            '2': 'vmess',
            '3': 'vless',
            '4': 'trojan'
        }

        if choice in protocols:
            protocol = protocols[choice]
            users = self.user_manager.list_users(protocol)
            print(f"\n{BOLD}{protocol.upper()} Users:{ENDC}")
            for user in users:
                print("\n---")
                for key, value in user.items():
                    if key != 'password':  # Don't show passwords
                        print(f"{key}: {value}")
        input("\nPress Enter to continue...")

    def delete_user(self):
        print(f"\n{BOLD}Delete User{ENDC}")
        print("1. SSH User")
        print("2. VMESS User")
        print("3. VLESS User")
        print("4. Trojan User")
        print("0. Back")

        choice = self.get_input("\nSelect protocol")

        protocols = {
            '1': 'ssh',
            '2': 'vmess',
            '3': 'vless',
            '4': 'trojan'
        }

        if choice in protocols:
            protocol = protocols[choice]
            identifier = self.get_input("Enter username/email to delete")
            self.user_manager.delete_user(protocol, identifier)
            print(f"\n{OKGREEN}User deleted successfully{ENDC}")
        input("\nPress Enter to continue...")

    def run(self):
        while True:
            self.print_menu()
            choice = self.get_input("\nSelect an option")

            if choice == '0':
                break
            elif choice == '1':
                self.create_ssh_user()
            elif choice == '2':
                self.create_vmess_user()
            elif choice == '3':
                self.create_vless_user()
            elif choice == '4':
                self.create_trojan_user()
            elif choice == '5':
                self.list_users()
            elif choice == '6':
                self.delete_user()