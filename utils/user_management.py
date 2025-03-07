import os
import json
import uuid
import base64
from datetime import datetime, timedelta
from pathlib import Path

class UserManager:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.users_dir = Path("data/users")
        self.users_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize protocol-specific user files
        self.user_files = {
            'ssh': self.users_dir / 'ssh_users.json',
            'vmess': self.users_dir / 'vmess_users.json',
            'vless': self.users_dir / 'vless_users.json',
            'trojan': self.users_dir / 'trojan_users.json'
        }
        
        # Create user files if they don't exist
        for file_path in self.user_files.values():
            if not file_path.exists():
                file_path.write_text('[]')

    def _load_users(self, protocol):
        try:
            with open(self.user_files[protocol], 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading {protocol} users: {str(e)}")
            return []

    def _save_users(self, protocol, users):
        try:
            with open(self.user_files[protocol], 'w') as f:
                json.dump(users, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving {protocol} users: {str(e)}")

    def create_ssh_user(self, username, password, ip_limit=1, days_valid=1):
        users = self._load_users('ssh')
        new_user = {
            'username': username,
            'password': password,
            'ip_limit': ip_limit,
            'days_valid': days_valid,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(days=days_valid)).isoformat()
        }
        users.append(new_user)
        self._save_users('ssh', users)
        self.logger.info(f"Created SSH user: {username} (IP limit: {ip_limit}, Valid for: {days_valid} days)")
        return new_user

    def create_vmess_user(self, username):
        users = self._load_users('vmess')
        user_id = str(uuid.uuid4())
        new_user = {
            'username': username,
            'id': user_id,
            'alterId': 0,
            'created_at': datetime.now().isoformat()
        }
        users.append(new_user)
        self._save_users('vmess', users)
        self.logger.info(f"Created VMESS user: {username}")
        return new_user

    def create_vless_user(self, username):
        users = self._load_users('vless')
        user_id = str(uuid.uuid4())
        new_user = {
            'username': username,
            'id': user_id,
            'created_at': datetime.now().isoformat()
        }
        users.append(new_user)
        self._save_users('vless', users)
        self.logger.info(f"Created VLESS user: {username}")
        return new_user

    def create_trojan_user(self, email, password=None):
        users = self._load_users('trojan')
        if password is None:
            password = base64.urlsafe_b64encode(os.urandom(16)).decode('utf-8')
        new_user = {
            'email': email,
            'password': password,
            'created_at': datetime.now().isoformat()
        }
        users.append(new_user)
        self._save_users('trojan', users)
        self.logger.info(f"Created Trojan user: {email}")
        return new_user

    def list_users(self, protocol):
        return self._load_users(protocol)

    def delete_user(self, protocol, identifier):
        users = self._load_users(protocol)
        if protocol == 'ssh':
            users = [u for u in users if u['username'] != identifier]
        else:
            users = [u for u in users if u['email'] != identifier] #This line remains as email is still used for trojan users.
        self._save_users(protocol, users)
        self.logger.info(f"Deleted {protocol} user: {identifier}")