# KeyScheduling.py

# --- SHARED UTILITY FUNCTIONS ---
# These are used by all other files

def hex2bin(hex_val):
    """Converts Hex string to 64-bit binary string."""
    return bin(int(hex_val, 16))[2:].zfill(64)

def bin2hex(bin_val):
    """Converts binary string to Hex."""
    return hex(int(bin_val, 2))[2:].upper().zfill(16)

def permute(input_str, table):
    """Permutes the input string according to the given table."""
    output = ""
    for i in table:
        # Tables are 1-based, string index is 0-based
        output += input_str[i - 1] 
    return output

def shift_left(binary_str, n):
    """Circular left shift by n bits."""
    return binary_str[n:] + binary_str[:n]

# --- KEY SCHEDULE TABLES (PC1, PC2, SHIFTS) ---

PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# --- KEY GENERATION LOGIC ---

def generate_keys(key_hex):
    """
    Generates 16 subkeys from the main 64-bit key.
    1. Permute Key (PC1)
    2. Split into C and D
    3. Shift and Permute (PC2) for 16 rounds
    """
    keys = []
    
    # 1. Convert Key to Binary
    key_bin = hex2bin(key_hex)
    
    # 2. Initial Permutation (PC1) - Reduces 64 bits to 56 bits
    key_56 = permute(key_bin, PC1)
    
    # 3. Split into Left (C) and Right (D) halves (28 bits each)
    c = key_56[0:28]
    d = key_56[28:56]
    
    # 4. Generate 16 Subkeys
    for shift in SHIFTS:
        c = shift_left(c, shift)
        d = shift_left(d, shift)
        combined = c + d
        # PC2 permutation reduces 56 bits to 48 bits
        subkey = permute(combined, PC2)
        keys.append(subkey)
        
    return keys