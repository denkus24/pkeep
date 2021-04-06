#-*-coding:utf8-*-
import csv
from Crypto.Cipher import AES
import hashlib

def encrypting_file(path,key):
    """Function for encrypting database"""
    key = hashlib.md5(bytes(key, 'utf8')).digest()

    with open(path,'r') as file:
        data = file.read()

    aes = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = aes.encrypt_and_digest(bytes(data, 'utf8'))
    with open(path, "wb") as file:
        for x in (aes.nonce, tag, ciphertext):
            file.write(x)

def decrypting_file(path,key):
    """Function for decrypting database"""
    key = hashlib.md5(bytes(key, 'utf8')).digest()
    file_in = open(path, "rb")
    nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]

    aes = AES.new(key, AES.MODE_EAX, nonce)
    data = aes.decrypt_and_verify(ciphertext, tag).decode('utf8')

    return data

def reading_file(path, key):
    """Function for reading and decrypting database"""
    res = []

    data = decrypting_file(path, key).split()


    reader = csv.reader(data)
    for row in reader:
        res.append((row[0], row[1], row[2], row[3]))
    return res

def add_element(path, name, login, password, link, key):
    """Function for adding element to database"""
    data = decrypting_file(path, key)

    res = data + "\n" + name + ',' + login + "," + password + "," + link
    with open(path,'w') as file:
        file.write(res)
    encrypting_file(path,key)


def delete_element(path, detectors, key):
    """Function for deleting element from database"""
    data = decrypting_file(path, key).split()
    reader = csv.reader(data, delimiter=",")
    rows = []
    for row in reader:
        if row != list(detectors) and len(row) != 0:
            rows.append(row)
    with open(path,'w') as file:
        writer = csv.writer(file, delimiter=',')
        for x in rows:
            writer.writerow(x)
    encrypting_file(path, key)

def edit_element(old_element,new_element,path,key):
    """Function for editing element from database"""
    data = decrypting_file(path, key).split()
    rows=[]
    for x in data:
        rows.append(x.split(','))

    for index,item in enumerate(rows):
        if item == list(old_element):
            rows[index] = list(new_element)

    with open(path,'w') as file:
        writer = csv.writer(file)
        for x in rows:
            writer.writerow(x)
    encrypting_file(path, key)