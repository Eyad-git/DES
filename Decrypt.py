# Decrypt.py
import KeySchedule
import Encrypt

def run_decrypt(ciphertext_hex, key_hex, verbose=False):
    """
    Decrypts a 64-bit block.
    Logic: Uses the exact same algorithm as encryption, 
    but applies the subkeys in REVERSE order.
    """
    # 1. Generate keys
    keys = KeySchedule.generate_keys(key_hex)
    
    # 2. REVERSE keys for decryption
    keys_reversed = keys[::-1]
    
    # 3. Run the shared DES engine
    return Encrypt.des_engine(ciphertext_hex, keys_reversed, verbose)