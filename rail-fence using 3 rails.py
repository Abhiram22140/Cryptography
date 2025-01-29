def encrypt_q1(input_1, rails):
    rail = [''] * rails
    direction_down = False
    row = 0

    for char in input_1:
        rail[row] += char
        if row == 0 or row == rails - 1:
            direction_down = not direction_down
        row += 1 if direction_down else -1

    return ''.join(rail)

def decrypt_q1(cipher, rails):
    rail_len = [0] * rails
    direction_down = None
    row = 0

    for i in range(len(cipher)):
        rail_len[row] += 1
        if row == 0:
            direction_down = True
        elif row == rails - 1:
            direction_down = False
        row += 1 if direction_down else -1

    rail = [''] * rails
    index = 0

    for r in range(rails):
        rail[r] = cipher[index:index + rail_len[r]]
        index += rail_len[r]

    result = []
    row = 0
    for i in range(len(cipher)):
        result.append(rail[row][0])
        rail[row] = rail[row][1:]
        if row == 0:
            direction_down = True
        elif row == rails - 1:
            direction_down = False
        row += 1 if direction_down else -1

    return ''.join(result)

message = "THE ENEMY WILL ATTACK AT DAWN".replace(" ", "")


cipher = encrypt_q1(message, 3)
print("Encrypted Message:", cipher)


decrypted_message = decrypt_q1(cipher, 3)
print("Decrypted Message:", decrypted_message)
