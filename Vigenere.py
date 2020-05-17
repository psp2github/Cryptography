# Vigenere implementation
# Author: Saravana
# Date: 05-02-2020

from string import ascii_uppercase as uppercaseAlphabet  # For uppercase alpha https://docs.python.org/3/library/string.html?highlight=ascii_uppercase
from itertools import cycle # Iterators for efficient loop https://docs.python.org/3/library/itertools.html

class Vigenere():    
    alphaLength = len(uppercaseAlphabet);

    def setup(key):
        key = key.upper()   # Store key as Upper case
        return cycle(uppercaseAlphabet.index(c) for c in key)   #Return list of aphabet in order

    def EncryptText(plainText, key):        
        shifts = Vigenere.setup(key); 
        cipherResponse = ''
        for char in plainText.upper():
            if char not in uppercaseAlphabet:
                cipherResponse += char      
            else:           # Alpha [ ( Index (First Char of PlainText) + Index (First Char of Key) ) mod 26 ]
                cipherResponse += uppercaseAlphabet[(uppercaseAlphabet.index(char) + next(shifts)) % Vigenere.alphaLength]
        return cipherResponse;

    def DecryptText(cipherText, key):
        shifts = Vigenere.setup(key);
        plainResponse = ''
        for char in cipherText.upper():
            if char not in uppercaseAlphabet: 
                plainResponse += char;
            else:          # Alpha [ ( Index (First Char of CipherText) - Index (First Char of Key) ) mod 26 ]
                plainResponse += uppercaseAlphabet[(uppercaseAlphabet.index(char) - next(shifts)) % Vigenere.alphaLength]
        return plainResponse;

if __name__ == '__main__':
        inputText = input('Enter text to Encode/Decode using vigenere alogrithm...\n') #if god wanted us to fly he would have given us tickets.
        key = input('Enter Key...\n') #blue
        resCipher = Vigenere.EncryptText(inputText,key);        
        print(f"Plaintext:      {inputText}")
        print(f"Key:            {key}")
        print(f"Encrypted text: {resCipher}")        
        resDeCipher = Vigenere.DecryptText(resCipher,key);
        print(f"Decrypted text: {resDeCipher}")  
