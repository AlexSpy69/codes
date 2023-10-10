class core_Substitution:
    def __init__(self):
        super(core_Substitution, self).__init__()
        self.type = 'core'
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.umlaute = {'AE': 'Ä', 'OE': 'Ö', 'UE': 'Ü'}
        self.umlaute2 = {y: x for x, y in self.umlaute.items()}
        self.numbers = '0123456789'
        self.symbols = ('`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '{', '[', '}',
                        '}', '|', '\\', ':', ';', '"', "'", '<', ',', '>', '.', '?', '/', ' ')

    def letter_not_in_alphabet(self, letter):
        if letter in self.numbers:
            return True
        elif letter in self.symbols:
            return True
        else:
            return False

    @staticmethod
    def umlaut_replace(string):
        string = string.replace('Ä', 'Ae')
        string = string.replace('Ö', 'Oe')
        string = string.replace('Ü', 'Ue')
        string = string.replace('ä', 'ae')
        string = string.replace('ö', 'oe')
        string = string.replace('ü', 'ue')
        return string

    @staticmethod
    def scharfs_replace(string):
        string = string.replace('ß', 'ss')
        string = string.replace('ẞ', 'ss')
        return string

    def scharfs_umlaut_replace(self, string):
        string = self.scharfs_replace(string)
        string = self.umlaut_replace(string)
        return string

    def insert_letter(self, old_letter, new_letter):
        insert = ''
        if self.numbers.count(old_letter) or self.symbols.count(old_letter):
            print(old_letter in self.numbers or self.symbols, old_letter)
            insert = old_letter
        elif old_letter in self.alphabet.upper():
            insert = new_letter.upper()
        elif old_letter in self.alphabet.lower():
            insert = new_letter.lower()
        return insert

    def change_alphabet(self, string, old_alphabet, new_alphabet):
        new_string = ''
        if not old_alphabet:
            old_alphabet = self.alphabet
        else:
            old_alphabet.upper()
        if not new_alphabet:
            new_alphabet = self.alphabet
        else:
            new_alphabet.upper()
        string = self.scharfs_umlaut_replace(string)
        for letter in string:
            try:
                new_letter = new_alphabet[old_alphabet.index(letter.upper())]
                new_string += self.insert_letter(letter, new_letter)
            except ValueError:
                new_string += letter
        return new_string

    def alphabet_list(self):
        return {'standard': self.alphabet,
                'atbash': self.alphabet[::-1],
                'tastatur_de': 'QWERTZUIOPASDFGHJKLYXCVBNM',
                'tastatur_us': 'QWERTYUIOPASDFGHJKLZXCVBNM'}
    
    @staticmethod
    def moved_alphabet(count, alphabet):
        new_alphabet = ''
        for i in range(0, len(alphabet)):
            try:
                new_alphabet += alphabet[i + count]
            except IndexError:
                new_alphabet += alphabet[i + count - len(alphabet)]
        return new_alphabet


class core_Keysquare:
    def __init__(self, elements='', sizex=0, sizey=0, keyword=False):
        if keyword:
            sizex = len(keyword)
            sizey = len(elements)//sizex
        else:
            pass
        super(core_Keysquare, self).__init__()
        self.type = 'core'
        if elements == '':
            elements = '' * (sizex*sizey)
        self.full_square = []
        for i in range(0, sizey):
            row = []
            for i2 in range(0, sizex):
                try:
                    row.append(elements[i2+(i*sizex)].upper())
                except IndexError:
                    row.append('')
            self.full_square.append(row)
        
        self.sizex = sizex
        self.sizey = sizey

    def element(self, x, y):
        return self.full_square[y][x]

    def insert(self, element, x, y):
        self.full_square[y][x] = element

    def show(self):
        print()
        for i in self.full_square:
            print(i)

    @staticmethod
    def index_adfgx(letter, number):
        letters = 'ADFGX'
        if letter != '':
            return letters.find(letter.upper())
        elif number != '':
            return letters[number]

    @staticmethod
    def index_adfgvx(letter, number):
        letters = 'ADFGX'
        if letter != '':
            return letters.find(letter.upper())
        elif number != '':
            return letters[number]

    @staticmethod    
    def letter_index(letter, number, letters):
        if letter != '':
            return letters.find(letter.upper())
        elif number != '':
            return letters[number]

    def column(self, num):
        column_ = ''
        i = 0
        while True:
            try:
                column_ += self.element(num, i)
                i += 1
            except IndexError:
                break
        return column_

    def row(self, num):
        row_ = ''
        i = 0
        while True:
            try:
                row_ += self.element(i, num)
                i += 1
            except IndexError:
                break
        return row_
    
    def find(self, element):
        for i in range(0, self.sizey):
            x_ = 0
            for item in self.row(i):
                if item == element:
                    thingtoreturn = {'x': x_, 'y': i}
                    return thingtoreturn
                x_ += 1
    
    def find_in_row(self, num, element):
        return self.row(num).find(element)
    
    def find_in_column(self, num, element):
        return self.column(num).find(element)
    
    @staticmethod
    def alt(elements, keyword=False, sizex=False, sizey=False):
        if keyword:
            sizex = len(keyword)
            sizey = len(elements)//sizex
        else:
            pass
        totallength = sizex*sizey
        placeholder = '' * totallength
        square = core_Keysquare(placeholder, sizex=sizex, sizey=sizey)
        letter_index = 0
        for i in range(0, sizex):
            for i2 in range(0, sizey):
                try:
                    square.insert(elements[letter_index], i, i2)
                except IndexError:
                    pass
                letter_index += 1
        return square
    
    @staticmethod
    def tabularecta():
        alphabet = core_Substitution().alphabet
        square = core_Keysquare('.' * len(alphabet) * len(alphabet), len(alphabet), len(alphabet))
        for i in range(0, len(square.row(0))):
            square.insert_row(i, core_Substitution().moved_alphabet(i, core_Substitution().alphabet))
        return square

    def insert_column(self, num, elements):
        for i in range(0, len(elements)):
            try:
                self.insert(elements[i], num, i)
            except IndexError:
                break
    
    def insert_row(self, num, elements):
        for i in range(0, len(elements)):
            try:
                self.insert(elements[i], i, num)
            except IndexError:
                break
    
    def to_string(self):
        string = ''
        for row in range(0, self.sizey):
            string += self.row(row)
        return string
    
    def to_string_alt(self):
        string = ''
        for column in range(0, self.sizex):
            string += self.column(column)
        return string


class core_Transposition:
    def __init__(self, key, filler=' ', sort=False, alt_direction=False):
        super(core_Transposition, self).__init__()
        self.type = 'core'
        self.keyword = "".join(dict.fromkeys(key.upper()))
        self.filler = filler
        self.sort = sort
        self.alt_direction = alt_direction
    
    def encrypt(self, plaintext, spaces=True):
        if not spaces:
            plaintext = plaintext.replace(' ', '')
        
        sizex = len(self.keyword)
        sizey = len(plaintext)//sizex+1
        totallength = sizex*sizey

        for i in range(0, totallength-len(plaintext)):
            plaintext += self.filler
        
        if not self.alt_direction:
            square = core_Keysquare(plaintext, sizex=sizex, sizey=sizey)
        else:
            square = core_Keysquare().alt(plaintext, sizex=sizex, sizey=sizey)
        column_dictionary = {}

        for letter in self.keyword:
            column_dictionary[letter] = square.column(self.keyword.index(letter))
        if self.sort:
            column_dictionary = {key: value for key, value in sorted(column_dictionary.items())}
        
        square.show()

        ciphertext = ''

        for column in column_dictionary:
            ciphertext += column_dictionary[column]

        return ciphertext
    
    def decrypt(self, ciphertext, filler_at_end=False):
        sizex = len(self.keyword)
        sizey = len(ciphertext)//sizex

        square = core_Keysquare().alt(ciphertext, keyword=self.keyword)

        list_keyword = list(self.keyword)
        keyword_sorted = list(self.keyword)
        if self.sort:
            keyword_sorted.sort()

        square_new = core_Keysquare(sizex=sizex, sizey=sizey)

        for i in range(0, len(self.keyword)):
            index_of_letter_in_other_list = list_keyword.index(keyword_sorted[i])
            square_new.insert_column(index_of_letter_in_other_list, square.column(i))

        if filler_at_end:
            return square_new.to_string()
        else:
            return square_new.to_string().rstrip(self.filler)
