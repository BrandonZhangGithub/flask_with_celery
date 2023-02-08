#certifi==2022.5.18.1
#cffi==1.15.0
#cryptography==37.0.2
#pycparser==2.21
#pycrypto==2.6.1
#pycryptodome==3.14.1

import base64
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms

def pkcs7_padding(data):
    if not isinstance(data, bytes):
        data = data.encode()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    return padded_data


def aes_encryption(data, key='jkl;POIU1234++=='):
    data = pkcs7_padding(data)
    while len(data) % 16 != 0:  # 补足字符串长度为16的倍数
        data += (16 - len(data) % 16) * chr(16 - len(data) % 16)
    # data = str.encode(data)
    aes = AES.new(str.encode(key), AES.MODE_ECB)  # 初始化加密器
    return str(base64.encodebytes(aes.encrypt(data)), encoding='utf8').replace('\n', '')  # 加密


# 加解密
if __name__ == '__main__':
    res_1 = aes_encryption('admin', 'jkl;POIU1234++==')
    res_2 = aes_encryption('2Jt6@jKk', 'jkl;POIU1234++==')
    res_3 = aes_encryption('9900000000124466', 'jkl;POIU1234++==')
    res_4 = aes_encryption('mgjFRY1QVi', 'jkl;POIU1234++==')
    print(res_1 == "a5mdzRXIy9yN7Sak0gxy+g==")
    print(res_2 == "Ze/Z6bJ3pvs7LuW591RqLg==")
    print(res_3 == "Gyd2hkvzYxdx4ia0+Ej0604ZQnzrzRHGp5gBfgUV39I=")
    print(res_4 == "VL8oJjg6yZ02HqYx6l7SKw==")