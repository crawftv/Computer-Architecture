"""CPU functionality."""

import sys

filename = sys.argv[1]


class CPU:
    """Main CPU class."""

    def __init__(self, filename):
        """Construct a new CPU."""
        self.ram = [None] * 256
        self.register = [None] * 7 + [0xf4]
        self.instruction_map = {
            0b0111: "PRN",
            0b0010: "LDI",
            0b0000: "CALL",
            0b0110: "POP",
            0b0101: "PUSH",
            0b0001: "RET",
            0b0100: "JMP"
        }
        self.alu_map = {
            0b0000: "ADD",
            0b0010: "MULT",
            0b0111: "CMP"
        }
        self.filename = filename

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        with open(self.filename) as f:
            for line in f:
                try:
                    l = line.split("#")[0].strip()
                    b = bin(int(l, base=2))
                except ValueError:
                    continue
                self.ram_write(address, b)
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def _num_operands(self, binary):
        operands = 0b1100000 & binary
        operands = operands >> 6
        return operands

    def _alu_operand(self, binary):
        binary = int(binary, base=2)
        alu = 0b00100000 & binary
        alu = alu >> 5
        return alu

    def _set_pc(self, binary):
        pc = 0b0001000 & binary
        pc = pc >> 4
        return pc

    def _instruction_identifier(self, binary):
        ii = 0b00001111 & binary
        return ii

    def _instruction_brancher(self, binary):
        if int(binary, base=2) == 0:
            instruction = "NOOP"
        elif int(binary, base=2) == 1:
            instruction = "HLT"
        elif int(binary, 2) == 0b01010101:
            instruction = "JEQ"
        elif int(binary, 2) == 0b01010110:
            instruction = "JNE"
        elif self._alu_operand(binary) == True:
            ii = int(binary, 2)
            ii = self._instruction_identifier(ii)
            instruction = self.alu_map[ii]
        else:
            ii = int(binary, 2)
            ii = self._instruction_identifier(ii)

            instruction = self.instruction_map[ii]

        return instruction

    def run(self):
        """Run the CPU."""
        self.load()
        program_counter = 0x00
        stack_pointer = self.register[-1]
        flag = None
        ii = None
        # import pdb
        # pdb.set_trace()
        while ii != "HLT":
            instruction = self.ram[program_counter]
            try:
                ii = self._instruction_brancher(instruction)
            except:
                import pdb
                pdb.set_trace()
            if ii == "MULT":
                reg_a = int(self.register[0], base=2)
                reg_b = int(self.register[1], base=2)
                self.register[0] = bin(reg_a*reg_b)
                program_counter += 3
            elif ii == "ADD":
                reg_a = int(self.register[0], base=2)
                reg_b = int(self.register[0], base=2)
                self.register[0] = bin(reg_a+reg_b)
                program_counter += 3
            elif ii == "CMP":
                reg_a = int(self.register[0], base=2)
                reg_b = int(self.register[1], base=2)
                if reg_a < reg_b:
                    flag = 0b0000100
                elif reg_a > reg_b:
                    flag = 0b00000010
                elif reg_a == reg_b:
                    flag = 0b00000001
                program_counter += 3

            elif ii == "JEQ":
                reg_r = int(self.ram[program_counter+1], base=2)
                jump_to_address = self.register[reg_r]
                if flag & 0b00000001:
                    program_counter = int(jump_to_address, 2)
                else:
                    program_counter += 2
            elif ii == "JNE":
                reg_r = int(self.ram[program_counter+1], base=2)
                jump_to_address = self.register[reg_r]
                if not flag & 0b0000001:
                    program_counter = int(jump_to_address, 2)
                else:
                    program_counter += 2

            elif ii == "JMP":
                reg_r = int(self.ram[program_counter+1], base=2)
                jump_to_address = self.register[reg_r]
                program_counter = int(jump_to_address, 2)
            elif ii == "LDI":
                register = int(self.ram[program_counter+1], base=2)
                immediate = self.ram[program_counter+2]

                self.register[register] = immediate
                program_counter += 3

            elif ii == "PRN":
                reg_num = self.ram_read(program_counter+1)
                register = self.register[int(reg_num, base=2)]
                print(int(register, base=2))
                program_counter += 2
            elif ii == "PUSH":
                self.register[-1] += -1
                reg_num = self.ram_read(program_counter+1)
                self.ram_write(
                    self.register[-1],
                    self.register[int(reg_num, base=2)]
                )
                program_counter += 2
            elif ii == "POP":

                stack_pointer = self.register[-1]
                reg_num = int(self.ram_read(program_counter+1), base=2)

                self.register[reg_num] = self.ram[stack_pointer]

                self.register[-1] += 1
                program_counter += 2
            elif ii == "CALL":

                address_at_register = int(self.register[int(
                    self.ram[program_counter+1], 2)
                ], 2)
                self.ram[stack_pointer] = program_counter+2
                program_counter = address_at_register
                self.register[-1] += -1
            elif ii == "RET":
                self.register[-1] += 1
                stack_pointer = self.register[-1]
                program_counter = self.ram[stack_pointer]
