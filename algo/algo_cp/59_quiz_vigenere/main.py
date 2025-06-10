from vigenere import decrypt, encrypt, generate_key

if __name__ == "__main__":
    t = "ATTACK SILICON VALLEY"
    k = generate_key(t, "HELLO")
    e = encrypt(t, k)
    print(e)
    d = decrypt(e, k)
    print(d)
