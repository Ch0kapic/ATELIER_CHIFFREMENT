import os
import sys
import base64
from nacl.secret import SecretBox
from nacl.utils import random

def get_box():
    # Récupération de la clé (attendue en base64 pour plus de simplicité)
    b64_key = os.getenv('NACL_SECRET_KEY')
    
    if not b64_key:
        print("❌ Erreur : NACL_SECRET_KEY non définie.")
        sys.exit(1)
    
    try:
        key = base64.b64decode(b64_key)
        return SecretBox(key)
    except Exception as e:
        print(f"❌ Erreur de clé : {e}")
        sys.exit(1)

def run_crypto(action, input_path, output_path):
    box = get_box()
    
    try:
        with open(input_path, 'rb') as f:
            data = f.read()

        if action == 'encrypt':
            # SecretBox génère un 'nonce' (nombre unique) automatiquement
            processed_data = box.encrypt(data)
        else:
            processed_data = box.decrypt(data)

        with open(output_path, 'wb') as f:
            f.write(processed_data)
        
        print(f"✅ Opération {action} réussie sur {output_path}")

    except Exception as e:
        print(f"❌ Échec : {e}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python nacl_crypto.py [encrypt|decrypt] <source> <dest>")
    else:
        run_crypto(sys.argv[1], sys.argv[2], sys.argv[3])
