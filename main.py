# main.py
import Encrypt
import Decrypt

def main():
    print("-------------------------------------------------")
    print("       DES ALGORITHM IMPLEMENTATION              ")
    print("-------------------------------------------------")
    
    # Test Vectors (from Rubric/Standard)
    plaintext = "123456ABCD132536"
    key       = "AABB09182736CCDD"
    
    print(f"INPUT Plaintext: {plaintext}")
    print(f"INPUT Key:       {key}")
    print("-------------------------------------------------")

    # 1. Encryption
    cipher = Encrypt.run_encrypt(plaintext, key)
    print(f"ENCRYPTION RESULT: {cipher}")

    # 2. Decryption
    decrypted = Decrypt.run_decrypt(cipher, key)
    print(f"DECRYPTION RESULT: {decrypted}")
    print("-------------------------------------------------")

    # 3. Verification
    if plaintext == decrypted:
        print("STATUS: SUCCESS - Decryption matches original.")
    else:
        print("STATUS: FAILURE - Mismatch detected.")
        
    print("-------------------------------------------------")

if __name__ == "__main__":
    main()