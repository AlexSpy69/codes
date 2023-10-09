import random
import sys
from core import *

random.seed()

class Atbash:
    def __init__(self):
        super(Atbash, self).__init__()
        self.type = 'nokey'

    def encrypt(self, plaintext):
        return core_Substitution().change_alphabet(plaintext, core_Substitution().alphabet,
                                              core_Substitution().alphabet_list()['atbash'])

    def decrypt(self, ciphertext):
        return self.encrypt(ciphertext)


class SimpleSubstitution:
    def __init__(self, key='a'*25):
        super(SimpleSubstitution, self).__init__()
        self.type = 'strkey'
        self.key = key

    def encrypt(self, plaintext):
        return core_Substitution().change_alphabet(plaintext, core_Substitution().alphabet, self.key)

    def decrypt(self, ciphertext):
        return core_Substitution().change_alphabet(ciphertext, self.key, core_Substitution().alphabet)


class Caesar:
    def __init__(self, key=0):
        super(Caesar, self).__init__()
        self.type = 'intkey'
        if key != '':
            self.key = int(key)
        else:
            self.key = 0

    def encrypt(self, plaintext):
        return core_Substitution().change_alphabet(plaintext, core_Substitution().alphabet,
                                              core_Substitution().moved_alphabet(self.key, core_Substitution().alphabet))

    def decrypt(self, ciphertext):
        newkey = self.key * (-1)
        return Caesar(newkey).encrypt(ciphertext)


class Rot13:
    def __init__(self):
        super(Rot13, self).__init__()
        self.type = 'nokey'
        self.code = Caesar(13)

    def encrypt(self, plaintext):
        return self.code.encrypt(plaintext)

    def decrypt(self, ciphertext):
        return self.code.decrypt(ciphertext)


class Railfence:
    def __init__(self, key=0):
        super(Railfence, self).__init__()
        self.type = 'intkey'
        try:
            self.key = int(key)
        except ValueError:
            self.key = 0

    def encrypt(self, plaintext, spaces=True):
        if not spaces:
            plaintext = plaintext.replace(' ', '')

        x = len(plaintext)
        y = self.key

        element_placeholder = ''
        for i in range(0, x * y):
            element_placeholder += '.'

        rektangle = core_Keysquare(element_placeholder, x, y)

        yofletter = 0
        add = True
        for i in range(0, len(rektangle.row(0))):
            rektangle.insert(plaintext[i], i, yofletter)
            if add:
                yofletter += 1
            else:
                yofletter -= 1
            if yofletter == self.key - 1:
                add = not add
            elif yofletter == 0:
                add = not add

        ciphertext = ''
        for i in range(0, len(rektangle.column(0))):
            ciphertext += rektangle.row(i).replace('.', '')

        return ciphertext

    def decrypt(self, ciphertext):
        x = len(ciphertext)
        y = self.key

        element_placeholder = ''
        for i in range(0, x * y):
            element_placeholder += '.'

        rektangle = core_Keysquare(element_placeholder, x, y)

        yofletter = 0
        add = True
        for i in range(0, len(rektangle.row(0))):
            rektangle.insert('-', i, yofletter)
            if add:
                yofletter += 1
            else:
                yofletter -= 1
            if yofletter == self.key - 1:
                add = not add
            elif yofletter == 0:
                add = not add

        index = 0
        for row in rektangle.full_square:
            for element in row:
                if element == '-':
                    row[row.index(element)] = ciphertext[index]
                    index += 1

        plaintext = ''
        for i in range(0, len(rektangle.row(0))):
            for element_ in rektangle.column(i):
                if element_ != '.':
                    plaintext += element_

        return plaintext


class PolybiusSquare:
    def __init__(self, elements='abcdefghiklmnopqrstuvwxyz', letterindexes='ABCDE'):
        super(PolybiusSquare, self).__init__()
        self.type = 'keysquare_polybius'
        elements = elements.upper()
        self.size = len(letterindexes)
        self.square = core_Keysquare(elements, sizex=self.size, sizey=self.size)

        self.letterindexes = letterindexes

    def encrypt(self, plaintext):
        ciphertext = ''
        for letter in plaintext:
            letter = letter.upper()
            itemindex = self.square.find(letter)
            if itemindex is None:
                continue
            else:
                letters = self.square.letter_index('', itemindex['y'],
                                                   self.letterindexes) + self.square.letter_index('', itemindex['x'],
                                                                                                  self.letterindexes)
                ciphertext += letters + ' '
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = ''
        ciphertext = ciphertext.replace(' ', '')
        for i in range(0, len(ciphertext), 2):
            new_y = self.letterindexes.index(ciphertext[i])
            new_x = self.letterindexes.index(ciphertext[i + 1])
            plaintext += self.square.element(new_x, new_y)
        return plaintext


class ColumnarTransposition:
    def __init__(self, key='A'):
        super(ColumnarTransposition, self).__init__()
        self.type = 'strkey'
        self.code = core_Transposition(key, filler='X', sort=True)

    def encrypt(self, plaintext, spaces=True):
        return self.code.encrypt(plaintext, spaces=spaces)

    def decrypt(self, ciphertext, filler_at_end=False):
        return self.code.decrypt(ciphertext, filler_at_end=filler_at_end)


class HomophonicSubstitution:
    def __init__(self, dictionary=None):
        super(HomophonicSubstitution, self).__init__()
        if dictionary is None:
            dictionary = {'': ''}
        self.type = 'dictkey'
        self.dictionary = dictionary

    def encrypt(self, plaintext):
        ciphertext = ''
        for i in plaintext:
            i = i.upper()
            try:
                characterlist = self.dictionary[i]
                ciphertext += characterlist[random.randint(0, len(characterlist) - 1)]
            except KeyError:
                ciphertext += i
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = ''
        add = None
        for i in ciphertext:
            for listindex in self.dictionary:
                if str(i) in self.dictionary[listindex]:
                    add = listindex
                    break
                else:
                    add = str(i)
            plaintext += add
        return plaintext


class Autokey:
    def __init__(self, key='a'):
        super(Autokey, self).__init__()
        self.type = 'strkey'
        self.key = key.upper()
        self.tabularecta = core_Keysquare().tabularecta()

    def encrypt(self, plaintext):
        ciphertext = ''
        plaintext = plaintext.upper()
        index = 0
        new_key = self.key

        for letter in plaintext:
            if letter in core_Substitution().alphabet:
                new_key += letter

        for letter in plaintext:
            if letter in core_Substitution().alphabet:
                x = core_Substitution().alphabet.index(new_key[index])
                y = core_Substitution().alphabet.index(letter)
                cipher_letter = self.tabularecta.element(x, y)
                ciphertext += cipher_letter
                index += 1
            else:
                ciphertext += letter
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = ''
        ciphertext = ciphertext.upper()
        index = 0
        new_key = self.key
        for letter in ciphertext:
            if letter in core_Substitution().alphabet:
                plain_letter = self.tabularecta.column(core_Substitution().alphabet.index(new_key[index])).index(letter)
                new_key += core_Substitution().alphabet[plain_letter]

                plaintext += core_Substitution().alphabet[plain_letter]
                index += 1
            else:
                plaintext += letter
        return plaintext


class Vigenere:
    def __init__(self, key='a'):
        super(Vigenere, self).__init__()
        self.type = 'strkey'
        self.key = key.upper()
        self.tabularecta = core_Keysquare().tabularecta()

    def encrypt(self, plaintext):
        ciphertext = ''
        plaintext = plaintext.upper()
        plaintext_no_spaces = plaintext.replace(' ', '')

        new_key = str(self.key * (len(plaintext_no_spaces) // len(self.key) + 1))

        index = 0
        for letter in plaintext:
            if letter in core_Substitution().alphabet:
                x = core_Substitution().alphabet.index(new_key[index])
                y = core_Substitution().alphabet.index(letter)
                cipher_letter = self.tabularecta.element(x, y)
                ciphertext += cipher_letter
                index += 1
            else:
                ciphertext += letter
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = ''
        ciphertext = ciphertext.upper()
        ciphertext_no_spaces = ciphertext.replace(' ', '')

        new_key = str(self.key * (len(ciphertext_no_spaces) // len(self.key) + 1))

        index = 0
        for letter in ciphertext:
            if letter in core_Substitution().alphabet:
                plain_letter = self.tabularecta.column(core_Substitution().alphabet.index(new_key[index])).index(letter)
                plaintext += core_Substitution().alphabet[plain_letter]
                index += 1
            else:
                plaintext += letter
        return plaintext


class Beaufort:
    def __init__(self, key='a'):
        super(Beaufort, self).__init__()
        self.type = 'strkey'
        self.key = key.upper()
        self.tabularecta = core_Keysquare().tabularecta()

    def encrypt(self, plaintext):
        ciphertext = ''
        plaintext = plaintext.upper()
        plaintext_no_spaces = plaintext.replace(' ', '')

        new_key = str(self.key * (len(plaintext_no_spaces) // len(self.key) + 1))

        index = 0
        for letter in plaintext:
            if letter in core_Substitution().alphabet:
                cipher_letter = core_Substitution().alphabet[self.tabularecta.column(core_Substitution().alphabet.find(letter)).find(new_key[index])]
                ciphertext += cipher_letter
                index += 1
            else:
                ciphertext += letter
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = ''
        ciphertext = ciphertext.upper()
        ciphertext_no_spaces = ciphertext.replace(' ', '')

        new_key = str(self.key * (len(ciphertext_no_spaces) // len(self.key) + 1))

        index = 0
        for letter in ciphertext:
            if letter in core_Substitution().alphabet:
                plain_letter = core_Substitution().alphabet[self.tabularecta.row(core_Substitution().alphabet.find(letter)).find(new_key[index])]
                plaintext += plain_letter
                index += 1
            else:
                plaintext += letter
        return plaintext


class Foursquare:
    def __init__(self,
                sq1='abcdefghiklmnopqrstuvwxyz',
                sq2='zgptfoihmuwdrcnykeqaxvsbl',
                sq3='mfnbdcrhsaxyogvituewlqzkp',
                sq4='abcdefghiklmnopqrstuvwxyz',
                size=5):
        super(Foursquare, self).__init__()
        self.type = 'foursquare'
        self.square1 = core_Keysquare(elements=sq1, sizex=size, sizey=size)
        self.square2 = core_Keysquare(elements=sq2, sizex=size, sizey=size)
        self.square3 = core_Keysquare(elements=sq3, sizex=size, sizey=size)
        self.square4 = core_Keysquare(elements=sq4, sizex=size, sizey=size)
    
    def encrypt(self, plaintext):
        plaintext = plaintext.upper()
        np = ''
        for letter in plaintext:
            if letter in core_Substitution().alphabet:
                np += letter
            else:
                pass
        plaintext = np
        if len(plaintext)/2 != len(plaintext)//2:
            plaintext += 'X'

        ciphertext = ''
        for i in range(0, len(plaintext), 2):
            coordinate_pl1 = self.square1.find(plaintext[i])
            coordinate_pl2 = self.square4.find(plaintext[i+1])

            element_cl1 = self.square2.element(x=coordinate_pl2['x'], y=coordinate_pl1['y'])
            element_cl2 = self.square3.element(x=coordinate_pl1['x'], y=coordinate_pl2['y'])

            ciphertext += element_cl1 + element_cl2
        
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = ''
        for i in range(0, len(ciphertext), 2):
            coordinate_pl1 = self.square2.find(ciphertext[i])
            coordinate_pl2 = self.square3.find(ciphertext[i+1])

            element_cl1 = self.square1.element(x=coordinate_pl2['x'], y=coordinate_pl1['y'])
            element_cl2 = self.square4.element(x=coordinate_pl1['x'], y=coordinate_pl2['y'])

            plaintext += element_cl1 + element_cl2
        
        return plaintext

