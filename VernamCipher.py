class vc:

    def __init__(self, text, key):
        self.text = text
        self.key = key

    def VernamCipher(self, text, key):
        result = ""
        ptr = 0
        for char in text:
            result = result + chr(ord(char) ^ ord(key[ptr]))
            ptr = ptr + 1
            if ptr == len(key):
                ptr = 0
        return result

