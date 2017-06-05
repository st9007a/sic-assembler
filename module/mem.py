class Memory:

    def __init__(self):
        self.memory = bytearray(32768) # 65536 hex

    def set_word(self, word, pos):
        self.memory[pos] = word >> 16
        self.memory[pos + 1] = word >> 8
        self.memory[pos + 2] = word

    def get_word(self, pos):
        return self.memory[pos] << 16 | self.memory[pos + 1] << 8 | self.memory[pos + 2]
