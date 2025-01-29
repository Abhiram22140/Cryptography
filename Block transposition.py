
def encrypt_columnar_transposition(text, keyword):
    n = len(keyword)
    sorted_keyword = sorted(list(keyword))
    col_order = [sorted_keyword.index(k) for k in keyword]
    
    
    grid = [''] * n
    for i, char in enumerate(text):
        grid[i % n] += char
    
    
    ciphertext = ''.join([grid[i] for i in col_order])
    return ciphertext

def decrypt_columnar_transposition(ciphertext, keyword):
    n = len(keyword)
    sorted_keyword = sorted(list(keyword))
    col_order = [sorted_keyword.index(k) for k in keyword]

    
    rows = len(ciphertext) // n
    extra_chars = len(ciphertext) % n
    

    grid = [''] * n
    start = 0
    
    for i in range(n-1):
         col_length = rows + (1 if i < extra_chars else 0)
         grid[col_order.index(i)] = ciphertext[start:start + col_length]
         start += col_length

    
    plaintext = ''
    for i in range(rows + 1):  
        for j in range(n):
            if i < len(grid[j]):
                plaintext += grid[j][i]
    
    return plaintext



ciphertext_part_a = "TNWACDHEEYILTAKTANEMLTAW"
keyword = "BATTLE"


ciphertext_part_b = encrypt_columnar_transposition(ciphertext_part_a, keyword)
print("Encrypted Message:", ciphertext_part_b)


decrypted_message_part_b = decrypt_columnar_transposition(ciphertext_part_b, keyword)
print("Decrypted Message:", decrypted_message_part_b)
