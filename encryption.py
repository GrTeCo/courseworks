import hashlib as hsh

def MD5(passwd):
    #Шифрование паролей

    enc_pass = hsh.md5(passwd.encode('utf-8'))
    return enc_pass.hexdigest()