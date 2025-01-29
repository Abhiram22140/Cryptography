def block_transposition_encrypt(text, block_size, permutation):
   
    blocks = [text[i:i+block_size] for i in range(0, len(text), block_size)]
    
    
    encrypted_blocks = []
    for block in blocks:
        encrypted_block = ''.join(block[i-1] for i in permutation if i-1 < len(block))
        encrypted_blocks.append(encrypted_block)
    

    return ''.join(encrypted_blocks)

def block_transposition_decrypt(ciphertext, block_size, permutation):

    inverse_permutation = sorted(range(1, len(permutation) + 1), key=lambda k: permutation[k-1])
    
    
    blocks = [ciphertext[i:i+block_size] for i in range(0, len(ciphertext), block_size)]
    
    
    decrypted_blocks = []
    for block in blocks:
        decrypted_block = ''.join(block[i-1] for i in inverse_permutation if i-1 < len(block))
        decrypted_blocks.append(decrypted_block)
    

    return ''.join(decrypted_blocks)


ciphertext_part_b = "NAAYETTWDLKTCLHIAKEMAWTNET"
block_size = 5
permutation = [2, 4, 1, 5, 3]


final_ciphertext = block_transposition_encrypt(ciphertext_part_b, block_size, permutation)
print("Final Encrypted Ciphertext:", final_ciphertext)


decrypted_message = block_transposition_decrypt(final_ciphertext, block_size, permutation)
print("Decrypted Message:", decrypted_message)
