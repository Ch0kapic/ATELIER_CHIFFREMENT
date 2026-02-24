import os
import sys
from cryptography.fernet import Fernet

def get_cipher():
    # Récupération de la clé depuis les variables d'environnement
    key = os.getenv('MY_FERNET_SECRET')
    
    if not key:
        print("❌ Erreur : La variable d'environnement 'MY_FERNET_SECRET' est absente.")
        sys.exit(1)
    
    return Fernet(key.encode())

def process_file(action, input_file, output_file):
    cipher = get_cipher()
    
    try:
        with open(input_file, 'rb') as f:
            data = f.read()
        
        if action == 'encrypt':
            result = cipher.encrypt(data)
            verb = "chiffré"
        else:
            result = cipher.decrypt(data)
            verb = "déchiffré"
            
        with open(output_file, 'wb') as f:
            f.write(result)
        
        print(f"✅ Succès : Fichier {verb} dans '{output_file}'")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'opération : {e}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python fernet_atelier1.py [encrypt|decrypt] <source> <destination>")
    else:
        process_file(sys.argv[1], sys.argv[2], sys.argv[3])
