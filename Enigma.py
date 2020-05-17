# The Enigma Machine Implementation
# Author: Saravana
# Date: 05-03-2020

from collections import namedtuple
from string import ascii_uppercase as uppercaseAlphabet  # For uppercase alpha https://docs.python.org/3/library/string.html?highlight=ascii_uppercase
from itertools import cycle # Iterators for efficient loop https://docs.python.org/3/library/itertools.html

class Enigma:
    alphaLength = len(uppercaseAlphabet);

    def __init__(self):
        
        self.State = namedtuple("State",["rotorPosition", "plugSwap", "rotorOrder"])
        startupState = self.State(              #Enigma Settings
            rotorPosition = 'ABC',              #Rotor Position
            plugSwap = [('A','B'),('T','G')],   #Plugboard setting
            rotorOrder =  ['I','II','III'],     # Rotor Order; I => Left; II => Middle; III => Right
        )
        self.rotorPosition = startupState.rotorPosition
        self.rotorOrder = startupState.rotorOrder
        self.rightRotor = Rotor(startupState.rotorOrder[2], startupState.rotorPosition[2])        
        self.middleRotor = Rotor(startupState.rotorOrder[1], startupState.rotorPosition[1],self.rightRotor)
        self.leftRotor = Rotor(startupState.rotorOrder[0], startupState.rotorPosition[0],self.middleRotor)
        #Reflector setting - UKW-B
        self.REFLECTOR = {
                'A':'Y', 'B':'R', 'C':'U', 'D':'H', 'E':'Q', 'F':'S', 'G':'L', 
                'H':'D','I':'P', 'J':'X', 'K':'N', 'L':'G', 'M':'O', 'N':'K', 
                'O':'M', 'P':'I','Q':'E', 'R':'B', 'S':'F', 'T':'Z', 'U': 'C', 
                'V':'W', 'W':'V', 'X':'J','Y':'A', 'Z':'T'
        }        
        self.plugBoard = startupState.plugSwap  
        self.middleRotor.prevRotor = self.leftRotor 
        self.rightRotor.prevRotor = self.middleRotor

    def convertMessage(self, message):
        cipherResponse = ''        
        for letter in message.upper():
            if letter not in uppercaseAlphabet:
                cipherResponse += letter      
            else:
                letter = self.applySwap(letter) #Plugboard Swap
                self.leftRotor.step()      # Left Rotor
                leftRotorOutput = self.leftRotor.encodeDecode(uppercaseAlphabet.index(letter))
                reflectorOutput = self.REFLECTOR[uppercaseAlphabet[leftRotorOutput % Enigma.alphaLength]]                
                convertedLetter = uppercaseAlphabet[self.rightRotor.encodeDecode(uppercaseAlphabet.index(reflectorOutput), forward = False)]
                convertedLetter = self.applySwap(convertedLetter)   #Plugboard Swap
                cipherResponse += convertedLetter
        return cipherResponse

    def applySwap(self, char):  # Plug board Swap letter
        for board in self.plugBoard:
            if char == board[0]: return board[1]
            if char == board[1]: return board[0]
        return char


class Rotor:
    alphaLength = len(uppercaseAlphabet);
    WIRING = {
        'I': {'forward':'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
                'backward':'UWYGADFPVZBECKMTHXSLRINQOJ'},
        'II':{'forward':'AJDKSIRUXBLHWTMCQGZNPYFVOE',
                'backward':'AJPCZWRLFBDKOTYUQGENHXMIVS'},
        'III':{'forward':'BDFHJLCPRTXVZNYEIWGAKMUSQO',
                'backward':'TAGBPCSDQEUFVNZHYIXJWLRKOM'}
    }
    #Visible letters in the window
    NOTCHES = {
        'I':'Q', # Rotor steps when I moves 
        'II':'E', # Rotor steps when II moves
        'III':'V', # Rotor steps when III moves
    }
    def __init__(self, num, letter, nextRotor=None, prevRotor=None):
        self.rotor_num = num
        self.wiring = Rotor.WIRING[num]
        self.notch = Rotor.NOTCHES[num]
        self.window = letter.upper()
        self.offset = uppercaseAlphabet.index(letter.upper())   
        self.nextRotor = nextRotor
        self.prevRotor = prevRotor

    def step(self):            
        #setup the rotor for the next step.              
        if self.nextRotor and self.window == self.notch:
            self.nextRotor.step()
        self.offset = (self.offset + 1) % Rotor.alphaLength
        self.window = uppercaseAlphabet[self.offset]
                
    def encodeDecode(self, index, forward=True):
        if forward:
            outputLetter = self.wiring['forward'][(index + self.offset) % Rotor.alphaLength]
        else:
            outputLetter = self.wiring['backward'][(index + self.offset) % Rotor.alphaLength]
        outputIndex = ( uppercaseAlphabet.index(outputLetter) - self.offset ) % Rotor.alphaLength
        if self.nextRotor and forward:
            return self.nextRotor.encodeDecode(outputIndex, forward)
        elif self.prevRotor and not forward:
            return self.prevRotor.encodeDecode(outputIndex, forward)
        else:
            return outputIndex
    
class TestMyCode:
    def defaultTest():
        inputText = 'This is Sample'
        encode = Enigma()
        response  = encode.convertMessage(inputText)
        print(f'Enigma Encode Settings:\n Rotor Position: {encode.rotorPosition}\n Rotor Order: {encode.rotorOrder}\n Plugboard setting: {encode.plugBoard}\n Reflector: UKW-B')
        print(f'Plaintext:      {inputText}')
        print(f'Encoded text:   {response}')
        decode = Enigma()
        response  = decode.convertMessage(response)
        print(f'Enigma Decode Settings:\n Rotor Position: {decode.rotorPosition}\n Rotor Order: {decode.rotorOrder}\n Plugboard setting: {decode.plugBoard}\n Reflector: UKW-B')
        print(f'Decoded text:   {response}')

    def test1():
        encode = Enigma()
        inputText = input('Enter text to Encode/Decode using Enigma machine...\n')
        response  = encode.convertMessage(inputText)
        print(f'Enigma Encode Settings:\n Rotor Position: {encode.rotorPosition}\n Rotor Order: {encode.rotorOrder}\n Plugboard setting: {encode.plugBoard}\n Reflector: UKW-B')
        print(f'Plaintext:      {inputText}')
        print(f'Encoded text:   {response}')
        decode = Enigma()
        response  = decode.convertMessage(response)
        print(f'Enigma Decode Settings:\n Rotor Position: {decode.rotorPosition}\n Rotor Order: {decode.rotorOrder}\n Plugboard setting: {decode.plugBoard}\n Reflector: UKW-B')
        print(f'Decoded text:   {response}')


if __name__ == '__main__':
    TestMyCode.defaultTest()