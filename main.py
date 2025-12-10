import Encrypt
import Decrypt

# --- HELPER FUNCTIONS ---

def pkcs7_pad(text_bytes):
    """
    Adds standard PKCS#7 padding to make the text a multiple of 8 bytes.
    Example: 'HELLO' (5 bytes) -> Adds three bytes of value 3 (\x03\x03\x03).
    """
    padding_len = 8 - (len(text_bytes) % 8)
    padding = bytes([padding_len] * padding_len)
    return text_bytes + padding

def pkcs7_unpad(text_bytes):
    """
    Removes PKCS#7 padding with STRICT validation.
    If the padding is corrupt (wrong key or tampering), this raises a ValueError.
    """
    if not text_bytes:
        raise ValueError("Input is empty")
        
    padding_len = text_bytes[-1]
    
    # 1. Validation: Padding length must be reasonable (1-8 for DES)
    if not (1 <= padding_len <= 8):
        raise ValueError("Invalid padding length byte")
    
    # 2. Validation: Check that *all* padding bytes match the length
    # e.g. If last byte is 0x03, the last 3 bytes MUST be 0x03 0x03 0x03
    padding = text_bytes[-padding_len:]
    for b in padding:
        if b != padding_len:
            raise ValueError("Invalid padding bytes")
            
    return text_bytes[:-padding_len]

def get_key_input():
    """Gets the 64-bit Hex Key."""
    default_key = "0E329232EA6D0D73"
    while True:
        k = input(f"Enter 64-bit Hex Key [Default: {default_key}]: ").strip()
        if not k: return default_key
        
        if len(k) != 16:
            print("❌ Error: Key must be 16 Hex characters.")
            continue
        return k.upper()

# --- MAIN ENGINE FOR ANY SIZE TEXT ---

def encrypt_full_message(plaintext_str, key_hex, verbose=False):
    """
    Encrypts text of ANY size using ECB Mode (looping through blocks).
    """
    # 1. Convert to bytes
    data = plaintext_str.encode('utf-8')
    
    # 2. Pad the data (Must be multiple of 8 bytes)
    padded_data = pkcs7_pad(data)
    
    cipher_full_hex = ""
    
    # 3. Loop through 8-byte chunks
    if verbose: print(f"\n[INTERNAL] Processing {len(padded_data)} bytes in 8-byte blocks...")
    
    for i in range(0, len(padded_data), 8):
        # Extract 8 bytes
        block = padded_data[i : i+8]
        block_hex = block.hex().upper()
        
        # Encrypt this single block
        if verbose: print(f"  -> Encrypting Block {i//8 + 1}: {block_hex}")
        block_cipher = Encrypt.run_encrypt(block_hex, key_hex, verbose=False)
        
        # Append to full result
        cipher_full_hex += block_cipher
        
    return cipher_full_hex

def decrypt_full_message(cipher_full_hex, key_hex, verbose=False):
    """
    Decrypts a long Hex string back to text.
    """
    decrypted_bytes = b""
    
    # Loop through 16-char Hex chunks (which represent 8 bytes)
    for i in range(0, len(cipher_full_hex), 16):
        block_hex = cipher_full_hex[i : i+16]
        
        # Decrypt single block
        decrypted_block_hex = Decrypt.run_decrypt(block_hex, key_hex, verbose=False)
        decrypted_bytes += bytes.fromhex(decrypted_block_hex)
        
    # Remove padding with Error Handling
    try:
        unpadded_data = pkcs7_unpad(decrypted_bytes)
        return unpadded_data.decode('utf-8')
    except Exception as e:
        # This catches the ValueError from pkcs7_unpad
        return "[Error: Invalid Padding or Key]"

# --- MAIN PROGRAM ---

def main():
    print("=================================================")
    print("       DES ENCRYPTION (Unlimited Text Size)      ")
    print("=================================================")
    
    # 1. Get Key
    key_hex = get_key_input()
    
    # 2. Get Any Text
    default_text = "8787878787878787" # NIST test vector as string
    plaintext_str = input(f"\nEnter Message (Any length) [Default: {default_text}]: ").strip()
    if not plaintext_str: plaintext_str = default_text

    # 3. Verbose Option
    verbose = input("Show block processing? (y/n): ").lower().startswith('y')

    print("\n=================================================")
    print(f" PROCESSING: '{plaintext_str}'")
    print("=================================================")
    
    # Run Encryption (ECB Mode)
    print("\n[+] ENCRYPTING...")
    final_cipher = encrypt_full_message(plaintext_str, key_hex, verbose)
    print(f"\n--> FULL CIPHERTEXT (Hex):")
    print(final_cipher)

    # Run Decryption
    print("\n[+] DECRYPTING...")
    final_text = decrypt_full_message(final_cipher, key_hex)
    print(f"--> DECRYPTED TEXT:")
    print(final_text)

    print("\n=================================================")
    print(" FINAL VERIFICATION")
    print("=================================================")
    
    if plaintext_str == final_text:
        print("STATUS: SUCCESS ✅")
        print("Matches original input.")
    else:
        print("STATUS: FAILURE ❌")
        
    print("=================================================")

if __name__ == "__main__":
    main()