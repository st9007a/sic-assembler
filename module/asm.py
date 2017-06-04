from optable import OpTable

global op_table
op_table = OpTable()

class Code:

    def __init__(self, line):
        global op_table

        self.label = None
        self.op = None
        self.arg = None
        self.line = line.strip('\t').strip('\n')

        parse_line = self.line.split('\t')

        # parse code
        if len(parse_line) == 1:
            self.op = parse_line[0]

        elif len(parse_line) == 2:
            self.op = parse_line[0]
            self.arg = parse_line[1]

        elif len(parse_line) == 3:
            self.label = parse_line[0]
            self.op = parse_line[1]
            self.arg = parse_line[2]

        else:
            raise Exception('Error line: ' + line)

        # check op is exist
        if op_table.is_exist(self.op) == False:
            raise Exception('Error op: ' + self.op)

        # check label with pseudo op
        if self.label != None and op_table.is_pseudo_op_exist(self.op) == False:
            raise Exception('Error line: ' + line)

        # check if mssing label when pseudo op
        if self.label == None and op_table.is_pseudo_op_exist(self.op):
            raise Exception('Error: label not found')


class Assembler:

    def __init__(self):
        global op_table
        self.optab = op_table
        self.asm_file_name = ''
        self.codes = []

        self.symtab= {}
        self.locctr = 0x0
        self.start_addr = 0
        self.program_len = 0

    def read_asm_file(self, file_name):
        self.asm_file_name = file_name
        with open(file_name) as f:
            content = [elem.rstrip('\n') for elem in f.readlines() if elem.rstrip('\n') != '']
            for line in content:
                self.codes.append(Code(line))

    def write_inter_file(self, line):
        print self.asm_file_name[:-4] + '.loc'
        with open(self.asm_file_name[:-4] + '.loc', 'a') as f:
            f.write(line)

    def pass_1(self):
        global op_table

        if self.codes[0].op == 'START':
            self.locctr = int(self.codes[0].arg, 16)
            self.write_inter_file(hex(self.locctr)[2:] + '\t' + self.codes[0].line + '\n')
            self.codes = self.codes[1:]

        self.start_addr = self.locctr

        for code in self.codes:
            if code.op == 'END':
                break

            #! check comment line

            if code.label != None:
                if code.label in self.symtab != None:
                    raise Exception('Error: duplicate symbol.')
                else:
                    self.symtab[code.label] = self.locctr

            if op_table.is_op_exist(code.op):
                self.locctr = self.locctr + 3
            elif code.op == 'WORD':
                self.locctr = self.locctr + 3
            elif code.op == 'RESW':
                self.locctr = self.locctr + 3 * int(code.arg)
            elif code.op == 'RESB':
                self.locctr = self.locctr + int(code.arg)
            elif code.op == 'BYTE':
                length = 0
                if code.arg[0] == 'C':
                    length = len(code.arg[2:-1])
                elif code.arg[0] == 'X':
                    length = len(code.arg[2:-1]) / 2
                else:
                    raise Exception('Error Byte Symbol: ' + code.arg[0])

                self.locctr = self.locctr + length

            else:
                raise Exception('Error: invalid op code')

            self.write_inter_file(hex(self.locctr)[2:] + '\t' + code.line + '\n')

        if self.codes[len(self.codes) - 1].op == 'END':
            self.write_inter_file(hex(self.locctr)[2:] + '\t' + self.codes[len(self.codes) - 1].line + '\n')

        self.program_len = self.locctr - self.start_addr


if __name__ == '__main__':
    asm = Assembler()
    asm.read_asm_file('../test/test.asm')
    asm.pass_1()

