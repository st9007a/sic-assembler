class OpTable:

    op_codes = {
        'ADD': '18',
        'AND': '40',
        'COMP': '28',
        'DIV': '24',
        'J': '3c',
        'JEQ': '30',
        'JGT': '34',
        'JLT': '38',
        'JSUB': '48',
        'LDA': '00',
        'LDB': '68',
        'LDCH': '50',
        'LDF': '70',
        'LDL': '08',
        'LDS': '6c',
        'LDT': '74',
        'LDX': '04',
        'MUL': '20',
        'OR': '44',
        'RD': 'd8',
        'RSUB': '4c',
        'SHIFTL': 'a4',
        'SHIFTR': 'a8',
        'STA': '0c',
        'STB': '78',
        'STCH': '54',
        'STF': '80',
        'STI': 'd4',
        'STL': '14',
        'STS': '7c',
        'STSW': 'e8',
        'STT': '84',
        'STX': '10',
        'SUB': '1c',
        'TD': 'e0',
        'TIX': '2c',
        'WD': 'dc',

    }

    pseudo_op_codes = [ 'RESB', 'RESW', 'BYTE', 'WORD', 'START', 'END' ]

    def __init__(self):
        self.op_to_code = {}
        self.code_to_op = {}
        for elem in OpTable.op_codes:
            self.op_to_code[elem] = OpTable.op_codes[elem]
            self.code_to_op[OpTable.op_codes[elem]] = elem

    def is_exist(self, op):
        return True if op in OpTable.op_codes or op in OpTable.pseudo_op_codes else False

    def is_op_exist(self, op):
        return True if op in OpTable.op_codes else False

    def is_pseudo_op_exist(self, op):
        return True if op in OpTable.pseudo_op_codes else False

if __name__ == '__main__':
    op_table = OpTable()
