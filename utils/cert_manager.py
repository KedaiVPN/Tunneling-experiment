import os
import ssl
from datetime import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from utils.colors import *

class CertificateManager:
    def __init__(self):
        self.cert_path = os.getenv('CERT_PATH', 'certs/cert.pem')
        self.key_path = os.getenv('KEY_PATH', 'certs/key.pem')

    def validate_certificates(self):
        """Validate that certificates exist and can be loaded into an SSL context"""
        try:
            if not os.path.exists(self.cert_path):
                print(f"{FAIL}Certificate file not found: {self.cert_path}{ENDC}")
                return False
            if not os.path.exists(self.key_path):
                print(f"{FAIL}Key file not found: {self.key_path}{ENDC}")
                return False

            # Try to create SSL context and load certificates
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(self.cert_path, self.key_path)

            # Load certificate for expiry check
            self.check_expiry()

            print(f"{OKGREEN}Certificates validated successfully{ENDC}")
            return True

        except Exception as e:
            print(f"{FAIL}Certificate validation failed: {str(e)}{ENDC}")
            return False

    def check_expiry(self):
        """Check certificate expiration date"""
        try:
            with open(self.cert_path, 'rb') as cert_file:
                cert_data = cert_file.read()
                cert = x509.load_pem_x509_certificate(cert_data, default_backend())
                expiry_date = cert.not_valid_after

                days_remaining = (expiry_date - datetime.now()).days
                if days_remaining < 30:
                    print(f"{WARNING}Certificate expires in {days_remaining} days{ENDC}")
                return days_remaining

        except Exception as e:
            print(f"{FAIL}Failed to check certificate expiry: {str(e)}{ENDC}")
            return None