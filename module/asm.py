import optable


class Code:

    PSEUDO_OP = ['RESB', 'RESW', 'BYTE', 'WORD', 'START', 'END']

    def __init__(self, line, op_table):
        self.label = ''
        self.op = ''
        self.arg = ''
        self.x = ' '

        self.obj_code = None
        self.offset = -1
        self.code_size = 0
        self.line_num = 0
        self.is_pseudo = None

        tokens = line.split('\t')
        arg_idx = -1

        if op_table.op_to_code[tokens[0]] != None:
            self.op = tokens[0].strip()
            arg_idx = 1
        else:
            self.label = tokens[0].strip()
            self.op = tokens[1].strip()
            arg_idx = 2

        if arg_idx < len(tokens):
            arg_str = tokens[arg_idx]
            args = arg_str.split(',')
            self.arg = args[0].strip()

            if len(args) > 1 and args[1].strip() == 'X':
                x = 'X'

        self.obj_code = op_table.op_to_code[self.op]

        if self.obj_code is None:
            raise Exception('op: ' + self.op + ' not found!')
        if self.op == 'BYTE':
            if self.arg.split('')[0] == 'C':
                str = arg[2:-1]
                self.code_size = len(str)
                self.obj_code = ''

                for si in range(0, len(str) - 1, 1):
                    ch = str.split('')[si]
                    self.obj_code += '{%02X}'.format(ch)

                self.obj_code = self.obj_code.upper()

            elif self.arg.split('')[0] == 'X':
                str = arg[2:-1]
                self.obj_code = str
                self.code_size = len(str) / 2

            else:
                self.code_size = -1

        elif self.op == 'WORD':
            self.code_size = 3
            self.obj_code = '{%06X}'.format(self.arg)

        elif self.op == 'RESB':
            self.code_size = int(self.arg)

        elif self.op == 'RESW':
            self.code_sixe = int(self.arg) * 3

        elif self.op == 'START':
            self.offset = hex(int(self.arg, 16) + 0x200)[2:]

        elif self.op == 'END':
            self.code_size = 0

        else:
            self.code_size = 3

        self.is_pseudo = any(self.op in pop for pop in Code.PSEUDO_OP)

    def to_string(self):
        return string(self.line_num) + '\t' + '{%01X}'.format(self.offset) + '\t' + self.label + '\t' + self.op + '\t' + self.arg + '\t' + self.x + '\t' + self.obj_code

class Assembler:

    def __init__(self):
        self.op_table = OpTable()
        self.symbol_table = {}
        self.codes = []


if __name__ == '__main__':
