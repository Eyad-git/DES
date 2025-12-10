import main
import Encrypt
import Decrypt

def run_test(name, expected, actual):
    """Helper to print pass/fail status nicely."""
    if expected == actual:
        print(f"✅ {name}: PASS")
        return True
    else:
        print(f"❌ {name}: FAIL")
        print(f"   Expected: {expected}")
        print(f"   Actual:   {actual}")
        return False

def test_sanity_check():
    """Test 1: Does the basic DES logic work?"""
    print("\n--- TEST 1: SANITY CHECK (NIST VECTOR) ---")
    key = "0E329232EA6D0D73"
    plain = "8787878787878787" # Hex string for this low-level test
    expected_cipher = "0000000000000000"
    
    # We call the low-level engine directly to check core logic
    cipher = Encrypt.run_encrypt(plain, key)
    run_test("NIST Vector Encryption", expected_cipher, cipher)

def test_padding_and_ecb():
    """Test 2: Can we handle text of any length?"""
    print("\n--- TEST 2: PADDING & ECB MODE ---")
    key = "0E329232EA6D0D73"
    text = "University" # 10 chars (needs padding)
    
    print(f"Original Text: '{text}'")
    
    # Encrypt
    cipher = main.encrypt_full_message(text, key)
    # Decrypt
    decrypted_text = main.decrypt_full_message(cipher, key)
    
    print(f"Decrypted Text: '{decrypted_text}'")
    
    run_test("Variable Length Text", text, decrypted_text)

def test_error_handling_wrong_key():
    """
    Test 3: What happens if we decrypt with the WRONG key?
    The unpadding function should fail, and our error handler should catch it.
    """
    print("\n--- TEST 3: ERROR HANDLING (WRONG KEY) ---")
    text = "SecretMessage"
    correct_key = "0E329232EA6D0D73"
    wrong_key   = "FFFFFFFFFFFFFFFF"
    
    print(f"Original Text: '{text}'")
    
    # Encrypt with correct key
    cipher = main.encrypt_full_message(text, correct_key)
    
    # Try to decrypt with WRONG key
    result = main.decrypt_full_message(cipher, wrong_key)
    
    print(f"Decryption Result with Wrong Key: '{result}'")
    
    # We expect the specific error message defined in main.py
    expected_msg = "[Error: Invalid Padding or Key]"
    run_test("Wrong Key Detection", expected_msg, result)

def test_integrity_tampering():
    """
    Test 4: What happens if a hacker changes 1 bit of the ciphertext?
    """
    print("\n--- TEST 4: INTEGRITY CHECK (TAMPERING) ---")
    text = "BankTransfer"
    key = "0E329232EA6D0D73"
    
    cipher = main.encrypt_full_message(text, key)
    
    # Corrupt the ciphertext (change last character)
    tampered_cipher = cipher[:-1] + "0" 
    
    result = main.decrypt_full_message(tampered_cipher, key)
    
    print(f"Tampered Result: '{result}'")
    
    # Should either be garbage or trigger error
    # Since DES propagates errors, padding will likely be invalid
    is_error = result == "[Error: Invalid Padding or Key]"
    print(f"✅ Tampering Detected/Handled: {is_error}")

if __name__ == "__main__":
    print("========================================")
    print("    RUNNING DES AUTOMATED TEST SUITE    ")
    print("========================================")
    
    test_sanity_check()
    test_padding_and_ecb()
    test_error_handling_wrong_key()
    test_integrity_tampering()
    
    print("\n========================================")
    print("            TESTING COMPLETE            ")
    print("========================================")