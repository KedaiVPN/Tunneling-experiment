import sys
import os
import json
from pathlib import Path

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.user_management import UserManager
from utils.logger import Logger
from config import Config

def test_user_management():
    # Initialize components
    config = Config()
    logger = Logger()
    user_mgr = UserManager(config, logger)
    
    print("\nTesting User Management System")
    print("=" * 30)
    
    # Test 1: Verify data directory creation
    data_dir = Path("data/users")
    assert data_dir.exists(), "Data directory was not created"
    print("✓ Data directory exists")
    
    # Test 2: Create test users
    test_users = {
        'ssh': user_mgr.create_ssh_user("test_ssh", "test_password"),
        'vmess': user_mgr.create_vmess_user("test_vmess@example.com"),
        'vless': user_mgr.create_vless_user("test_vless@example.com"),
        'trojan': user_mgr.create_trojan_user("test_trojan@example.com")
    }
    
    # Test 3: Verify user creation
    for protocol, user in test_users.items():
        users = user_mgr.list_users(protocol)
        assert any(u['email' if protocol != 'ssh' else 'username'] == 
                  user['email' if protocol != 'ssh' else 'username'] for u in users), \
            f"{protocol.upper()} user was not created properly"
        print(f"✓ {protocol.upper()} user created and verified")
    
    # Test 4: Verify file storage
    for protocol in test_users.keys():
        file_path = data_dir / f"{protocol}_users.json"
        assert file_path.exists(), f"{protocol} users file not created"
        with open(file_path, 'r') as f:
            stored_users = json.load(f)
        assert len(stored_users) > 0, f"No users stored in {protocol} file"
        print(f"✓ {protocol.upper()} user data properly stored")
    
    # Clean up test data
    for protocol, user in test_users.items():
        identifier = user['email'] if protocol != 'ssh' else user['username']
        user_mgr.delete_user(protocol, identifier)
        print(f"✓ {protocol.upper()} test user cleaned up")
    
    print("\nAll user management tests passed successfully!")

if __name__ == "__main__":
    test_user_management()
