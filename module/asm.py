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

        if self.obj_code is None
            raise Exception('op: ' + self.op + ' not found!')
        if self.op == 'BYTE':
            if self.arg.split('')[0] == 'C':
                str = arg[2:-1]
                self.code_size = len(str)

                for si in range(0, len(str) - 1, 1):
                    ch = str.split('')[si]
                    ch_int = int(ch)


class Assembler:

    def __init__(self):
        self.op_table = OpTable()
        self.symbol_table = {}
        self.codes = []


if __name__ == '__main__':

