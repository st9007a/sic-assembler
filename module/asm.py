import os
from optab import OpTable

global op_table
op_table = OpTable()

class Code:

    def __init__(self, line):
        global op_table

        self.label = None
        self.op = None
        self.arg = None
        self.loc = None
        self.obj_code = None
        self.line = line.strip('\n')

        parse_line = self.line.split('\t')

        # parse code
        if len(parse_line) == 2:
            self.label = parse_line[0] if parse_line[0] != '' else None
            self.op = parse_line[1]

        elif len(parse_line) == 3:
            self.label = parse_line[0] if parse_line[0] != '' else None
            self.op = parse_line[1]
            self.arg = parse_line[2] if parse_line[2] != '' else None

        else:
            raise Exception('line: ' + line)

        # check op is exist
        if op_table.is_exist(self.op) == False:
            raise Exception('invalid op "' + self.op + '"')

        if self.label == None and self.op in ['RESW','RESB','WORD','BYTE']:
            raise Exception('label not found')

class Assembler:

    max_record_len = 30

    def __init__(self):
        global op_table
        self.optab = op_table
        self.asm_file_name = ''
        self.codes = []

        self.symtab= {}
        self.locctr = 0
        self.start_addr = 0
        self.program_len = 0
        self.program_name = ''

    def load(self, file_name):
        if file_name[-3:].lower() != 'asm':
            raise Exception('extension file name is not "asm"')

        self.asm_file_name = file_name
        with open(file_name) as f:
            content = [elem.rstrip('\n') for elem in f.readlines() if elem.rstrip('\n') != '']
            for line in content:
                if line.strip('\t').strip(' ')[0] == '.':
                    continue
                self.codes.append(Code(line))

    def get_op_addr(self, arg):
        if arg in self.symtab:
            return format(self.symtab[arg], '04x')
        elif arg[0] == '#':
            return format(int(arg[1:]), '04x')
        elif arg in ['A', 'S', 'X', 'T']:
            return OpTable.registers[arg]
        else:
            raise Exception('undefined symbol ' + arg)

    def write_list_file(self, line):
        with open(self.asm_file_name[:-4] + '.lst', 'a') as f:
            f.write(line.upper())

    def write_obj_file(self, line):
        with open(self.asm_file_name[:-4] + '.obj', 'a') as f:
            f.write(line.upper())

    def pass_1(self):
        global op_table

        if self.codes[0].op == 'START':
            self.locctr = int(self.codes[0].arg, 16)
            self.codes[0].loc = self.locctr
            self.program_name = self.codes[0].label

        self.start_addr = self.locctr

        for code in self.codes:
            if code.op == 'START':
                continue
            if code.op == 'END':
                break

            if code.label != None:
                if code.label in self.symtab != None:
                    raise Exception('duplicate symbol')
                else:
                    self.symtab[code.label] = self.locctr

            code.loc = self.locctr

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
                    raise Exception('invalid byte symbol: ' + code.arg[0])

                self.locctr = self.locctr + length

            else:
                raise Exception('invalid op code')

        self.program_len = self.locctr - self.start_addr

    def pass_2(self):
        global op_table

        if self.codes[0].op == 'START':
            self.write_list_file(hex(self.codes[0].loc)[2:] + '\t' + self.codes[0].line + '\n')

        self.write_obj_file('H^' + self.program_name.ljust(6) + '^' + format(self.start_addr, '06x') + '^' + format(self.program_len, '06x') + '\n')
        text_record_head = 'T' + '^' + format(self.start_addr, '06x')
        text_record_body = ''
        record_len = 0

        for code in self.codes:
            if code.op == 'START':
                continue
            if code.op == 'END':
                break
            if code.op in ['RESW', 'RESB']:
                self.write_list_file(hex(code.loc)[2:] + '\t' + code.line + '\n')
                continue

            if op_table.is_op_exist(code.op):
                op_addr = self.get_op_addr(code.arg) if code.arg != None else 0
                op_code = op_table.op_to_code[code.op]
                code.obj_code = op_code + op_addr
            elif code.op == 'BYTE':
                if code.arg[0] == 'C':
                    code.obj_code = code.arg[2:-1].encode('hex')
                elif code.arg[0] == 'X':
                    code.obj_code = code.arg[2:-1]
                else:
                    raise Exception('error arg: ' + code.arg)
            elif code.op == 'WORD':
                code.obj_code = format(int(code.arg), '06x')

            if record_len + len(code.obj_code) / 2 > Assembler.max_record_len:
                self.write_obj_file(text_record_head + '^' + format(record_len, '02x') + text_record_body + '\n')
                text_record_head = 'T' + '^' + format(code.loc, '06x')
                text_record_body = ''
                record_len = 0

            text_record_body = text_record_body + '^' +code.obj_code
            record_len = record_len + len(code.obj_code) / 2

            self.write_list_file(hex(code.loc)[2:] + '\t' + code.line + '\t' + code.obj_code + '\n')

        self.write_obj_file(text_record_head + '^' + format(record_len, '02x') + text_record_body + '\n')

        # write end record to obj file
        for code in self.codes:
            if op_table.is_pseudo_op_exist(code.op) and code.op != 'START':
                continue

            self.write_obj_file('E^' + format(code.loc, '06x'))
            break

        # write end to list file
        if self.codes[len(self.codes) - 1].op == 'END':
            self.write_list_file('\t' + self.codes[len(self.codes) - 1].line)


if __name__ == '__main__':
    if os.path.isfile('../test/test.lst'):
        os.remove('../test/test.lst')

    if os.path.isfile('../test/test.obj'):
        os.remove('../test/test.obj')

    asm = Assembler()
    asm.load('../test/test.asm')
    asm.pass_1()
    asm.pass_2()

