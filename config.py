import os
import json

class Config:
    def __init__(self):
        self.ssh_config = {
            'openssh_port': int(os.getenv('OPENSSH_PORT', 2222)),
            'dropbear_port': int(os.getenv('DROPBEAR_PORT', 2244)),
            'ws_port': int(os.getenv('SSH_WS_PORT', 8070)),  
            'udp_port': int(os.getenv('SSH_UDP_PORT', 1194)),
            'ssl_ws_port': int(os.getenv('SSH_SSL_WS_PORT', 8443))
        }

        self.v2ray_config = {
            'vmess_ws_tls_port': int(os.getenv('VMESS_WS_TLS_PORT', 8444)),
            'vmess_ws_port': int(os.getenv('VMESS_WS_PORT', 8071)),  
            'vless_ws_tls_port': int(os.getenv('VLESS_WS_TLS_PORT', 8445)),
            'vless_ws_port': int(os.getenv('VLESS_WS_PORT', 8072))  
        }

        self.trojan_config = {
            'ws_tls_port': int(os.getenv('TROJAN_WS_TLS_PORT', 8446)),
            'ws_port': int(os.getenv('TROJAN_WS_PORT', 8073)),  
            'grpc_port': int(os.getenv('TROJAN_GRPC_PORT', 8447))
        }

        # Updated to use local development certificates by default
        self.tls_config = {
            'cert_path': os.getenv('CERT_PATH', 'certs/cert.pem'),
            'key_path': os.getenv('KEY_PATH', 'certs/key.pem')
        }